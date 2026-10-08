"""Redact kebocoran identitas sistem dari jawaban model.

Memakai hook transform_llm_output: jika teks jawaban mengandung kata/frasa
terlarang (nama sistem, model, vendor, teknologi AI), seluruh jawaban diganti
dengan kalimat baku. Tidak bergantung pada kepatuhan model terhadap system
prompt, dan berlaku untuk SEMUA sesi (lama maupun baru) serta lintas bahasa.
"""

import logging
import re

logger = logging.getLogger("plugins.redact-identity")

# Kalimat baku pengganti bila terdeteksi kebocoran identitas.
REPLACEMENT = "Saya adalah AI Agent UPA TIK untuk membantu kebutuhan pengguna."

# Kata/frasa terlarang (dicocokkan case-insensitive). Tambah/kurangi sesuai
# kebutuhan. Hindari kata yang terlalu umum agar tidak salah sensor.
BANNED = [
    "hermes",
    "groq",
    "llama",
    "gpt-oss",
    "gpt oss",
    "openai",
    "chatgpt",
    "gemini",
    "anthropic",
    "claude",
    "nous research",
    "nousresearch",
    "large language model",
    "run commands, read files",
    "reusable skills",
]

_BANNED_RE = re.compile("|".join(re.escape(w) for w in BANNED), re.IGNORECASE)


def _transform_llm_output(response_text=None, session_id=None, model=None,
                          platform=None, **kwargs):
    """Ganti seluruh jawaban bila ada kata terlarang; None jika aman."""
    try:
        if not response_text:
            return None
        if _BANNED_RE.search(response_text):
            logger.info(
                "redact-identity: identitas disensor (platform=%s session=%s)",
                platform, session_id,
            )
            return REPLACEMENT
        return None
    except Exception as e:  # noqa: BLE001
        # Fail-safe: jangan sampai error memblokir jawaban normal.
        logger.warning("redact-identity: error, teruskan apa adanya: %s", e)
        return None


def register(ctx):
    ctx.register_hook("transform_llm_output", _transform_llm_output)
    logger.info("redact-identity: hook transform_llm_output terpasang")
