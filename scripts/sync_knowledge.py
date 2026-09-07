#!/usr/bin/env python3
"""
Sync knowledge base DAN service catalog dari API Helpdesk ITK ke file Markdown.

Skrip ini mengambil dua sumber dari API external helpdesk lalu menuliskannya ke
file Markdown yang di-mount ke container Hermes. Hermes membacanya via
`context_files` di config.yaml, jadi skrip cukup dijalankan berkala (cron).

Sumber:
  1. Knowledge base -> knowledges/synced/knowledge-base.md
  2. Service catalog -> knowledges/synced/service-catalog.md

Autentikasi: header X-API-Key dan X-API-Secret (+ Accept: application/json).

Environment variable:
  KNOWLEDGE_API_KEY       Nilai header X-API-Key    (WAJIB)
  KNOWLEDGE_API_SECRET    Nilai header X-API-Secret (WAJIB)
  KNOWLEDGE_API_URL       Endpoint knowledge base
                          (default: https://helpdesk.itk.ac.id/api/external/knowledge-bases)
  SERVICE_CATALOG_API_URL Endpoint service catalog
                          (default: https://helpdesk.itk.ac.id/api/external/service-catalog)
  KNOWLEDGE_OUTPUT_DIR    Folder output (default: <repo>/knowledges/synced)
  KNOWLEDGE_HTTP_TIMEOUT  Timeout HTTP dalam detik (default: 15)

Hanya memakai pustaka standar Python 3 (urllib), tanpa dependency tambahan.
Jika sebuah sumber gagal/kosong, file lama sumber itu TIDAK ditimpa, sehingga
data valid terakhir tetap tersedia untuk Hermes.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_KB_URL = "https://helpdesk.itk.ac.id/api/external/knowledge-bases"
DEFAULT_CATALOG_URL = "https://helpdesk.itk.ac.id/api/external/service-catalog"


def log(msg: str) -> None:
    ts = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S %z")
    print(f"[{ts}] {msg}", flush=True)


def fetch(url: str, key: str, secret: str, timeout: int) -> object:
    """Ambil JSON dari endpoint. Raise RuntimeError kalau gagal."""
    req = urllib.request.Request(url, method="GET")
    req.add_header("X-API-Key", key)
    req.add_header("X-API-Secret", secret)
    req.add_header("Accept", "application/json")
    req.add_header("User-Agent", "hermes-knowledge-sync/2.0")

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        body = ""
        try:
            body = e.read().decode("utf-8", errors="replace")[:500]
        except Exception:
            pass
        raise RuntimeError(f"HTTP {e.code} dari {url}. Body: {body}")
    except urllib.error.URLError as e:
        raise RuntimeError(f"Gagal menghubungi {url}: {e.reason}")

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        raise RuntimeError(f"Response {url} bukan JSON valid. Awal: {raw[:300]}")


def extract_items(payload: object) -> list[dict]:
    """Ambil daftar entri dari berbagai kemungkinan bentuk response.

    Menangani list langsung, {"data": [...]}, paginasi Laravel
    {"data": {"data": [...]}}, dan pembungkus umum lain.
    """
    if isinstance(payload, list):
        return [x for x in payload if isinstance(x, dict)]

    if isinstance(payload, dict):
        for key in ("data", "knowledge_bases", "services", "items", "results", "catalog"):
            if key in payload:
                inner = payload[key]
                if isinstance(inner, list):
                    return [x for x in inner if isinstance(x, dict)]
                if isinstance(inner, dict) and isinstance(inner.get("data"), list):
                    return [x for x in inner["data"] if isinstance(x, dict)]
        return [payload]

    return []


def pick(item: dict, *keys: str, default: str = "") -> str:
    for k in keys:
        v = item.get(k)
        if v not in (None, ""):
            return str(v)
    return default


def kb_section(item: dict) -> str:
    """Format satu entri knowledge base menjadi section Markdown."""
    title = pick(item, "title", "name", "judul", default="Untitled")
    category = pick(item, "category", "kategori", "type", "group")
    content = pick(
        item, "content", "body", "isi", "description", "deskripsi", "answer", "jawaban"
    )

    lines = [f"## {title}", ""]
    if category:
        lines += [f"**Kategori:** {category}", ""]
    if content:
        lines.append(content)
    else:
        for k, v in item.items():
            if isinstance(v, (dict, list)):
                v = json.dumps(v, ensure_ascii=False)
            lines.append(f"- **{k}:** {v}")
    lines.append("")
    return "\n".join(lines)


def catalog_section(item: dict) -> str:
    """Format satu entri service catalog menjadi section Markdown."""
    name = pick(item, "name", "title", "service_name", "nama", "judul", default="Untitled")
    category = pick(item, "category", "kategori", "group", "type")
    desc = pick(item, "description", "deskripsi", "content", "body", "isi")
    sla = pick(item, "sla", "sla_hours", "target_sla", "waktu_penyelesaian")
    owner = pick(item, "owner", "unit", "pengelola", "team", "penanggung_jawab")
    how = pick(item, "how_to_request", "cara_request", "cara_pengajuan", "procedure", "prosedur")

    lines = [f"## {name}", ""]
    if category:
        lines += [f"**Kategori:** {category}", ""]
    if desc:
        lines += [desc, ""]
    if owner:
        lines.append(f"- **Pengelola:** {owner}")
    if sla:
        lines.append(f"- **SLA:** {sla}")
    if how:
        lines.append(f"- **Cara pengajuan:** {how}")
    # Kalau semua field dikenal kosong, tampilkan seluruh field agar tak ada
    # informasi yang hilang.
    if not (desc or owner or sla or how):
        for k, v in item.items():
            if isinstance(v, (dict, list)):
                v = json.dumps(v, ensure_ascii=False)
            lines.append(f"- **{k}:** {v}")
    lines.append("")
    return "\n".join(lines)


def write_atomic(out_file: Path, text: str) -> None:
    out_file.parent.mkdir(parents=True, exist_ok=True)
    tmp = out_file.with_suffix(out_file.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(out_file)


def sync_source(
    label: str,
    url: str,
    heading: str,
    section_fn,
    out_file: Path,
    key: str,
    secret: str,
    timeout: int,
) -> bool:
    """Ambil satu sumber dan tulis ke file. Return True jika sukses."""
    log(f"[{label}] Mengambil dari {url}")
    try:
        payload = fetch(url, key, secret, timeout)
    except RuntimeError as e:
        log(f"[{label}] GAGAL: {e} (file lama dipertahankan)")
        return False

    items = extract_items(payload)
    if not items:
        log(f"[{label}] Kosong / bentuk tak dikenal; file lama dipertahankan.")
        return False

    generated = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S %z")
    parts = [
        f"# {heading}",
        "",
        f"<!-- Disinkronkan otomatis dari API pada {generated}. "
        "Jangan edit manual; ubah di sumber lalu jalankan scripts/sync_knowledge.py. -->",
        "",
        f"Total entri: {len(items)}",
        "",
    ]
    parts += [section_fn(it) for it in items]
    write_atomic(out_file, "\n".join(parts))
    log(f"[{label}] Selesai. {len(items)} entri -> {out_file}")
    return True


def main() -> None:
    key = os.environ.get("KNOWLEDGE_API_KEY", "").strip()
    secret = os.environ.get("KNOWLEDGE_API_SECRET", "").strip()
    timeout = int(os.environ.get("KNOWLEDGE_HTTP_TIMEOUT", "15"))

    kb_url = os.environ.get("KNOWLEDGE_API_URL", DEFAULT_KB_URL).strip()
    catalog_url = os.environ.get("SERVICE_CATALOG_API_URL", DEFAULT_CATALOG_URL).strip()

    repo_root = Path(__file__).resolve().parent.parent
    out_dir = Path(os.environ.get("KNOWLEDGE_OUTPUT_DIR", str(repo_root / "knowledges" / "synced")))

    if not key or not secret:
        log("ERROR: KNOWLEDGE_API_KEY dan KNOWLEDGE_API_SECRET wajib di-set.")
        sys.exit(1)

    ok_kb = sync_source(
        "knowledge-base", kb_url, "Knowledge Base Helpdesk UPA TIK ITK",
        kb_section, out_dir / "knowledge-base.md", key, secret, timeout,
    )
    ok_catalog = sync_source(
        "service-catalog", catalog_url, "Katalog Layanan (Service Catalog) UPA TIK ITK",
        catalog_section, out_dir / "service-catalog.md", key, secret, timeout,
    )

    # Keluar dengan error kalau KEDUANYA gagal, supaya cron/monitoring tahu.
    if not ok_kb and not ok_catalog:
        sys.exit(1)


if __name__ == "__main__":
    main()
