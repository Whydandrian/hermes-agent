"""Blokir slash command dari pengguna WhatsApp non-admin.

Plugin ini memasang hook `pre_gateway_dispatch` yang berjalan SEBELUM gateway
memproses pesan (termasuk sebelum slash command diproses). Kalau pesan diawali
'/' dan pengirimnya bukan admin, plugin:
  1. Membalas dengan pesan manusiawi ("Saya tidak paham ...").
  2. Mengembalikan {"action": "skip"} sehingga Hermes TIDAK memproses command.

Admin (nomor yang terhubung langsung ke Hermes) tetap bisa memakai semua command.
"""

import logging

logger = logging.getLogger("plugins.block-commands")

# Nomor admin (tanpa tanda +). Hanya nomor ini yang boleh memakai slash command.
ADMIN_IDS = {"628219710713"}

# Balasan untuk pengguna non-admin yang mencoba memakai command.
REPLY_TEXT = "Saya tidak paham dengan yang Anda maksud."

# Hanya berlaku untuk platform ini. Kosongkan (None) untuk semua platform.
TARGET_PLATFORMS = {"whatsapp"}


def _norm_id(value: str) -> str:
    """Normalkan user id WhatsApp agar bisa dibandingkan dengan ADMIN_IDS.

    Contoh input yang mungkin: '628219710713', '628219710713@s.whatsapp.net',
    '58914133541011@lid', '+628219710713'. Kita ambil bagian digit sebelum '@'.
    """
    if not value:
        return ""
    v = str(value).strip()
    v = v.split("@", 1)[0]          # buang suffix @s.whatsapp.net / @lid
    v = v.split(":", 1)[0]          # buang suffix device id kalau ada
    v = v.lstrip("+")               # buang tanda +
    return "".join(ch for ch in v if ch.isdigit())


def _extract(event):
    """Ambil (text, platform, user_id) dari objek event secara defensif."""
    text = getattr(event, "text", None) or ""
    platform = ""
    user_id = ""

    source = getattr(event, "source", None)
    if source is not None:
        platform = getattr(source, "platform", "") or ""
        # user_id bisa bernama beda antar versi; coba beberapa atribut.
        for attr in ("user_id", "sender_id", "sender", "user"):
            val = getattr(source, attr, None)
            if val:
                user_id = val
                break

    # Fallback kalau atribut ada langsung di event.
    if not platform:
        platform = getattr(event, "platform", "") or ""
    if not user_id:
        for attr in ("user_id", "sender_id"):
            val = getattr(event, attr, None)
            if val:
                user_id = val
                break

    return str(text), str(platform), str(user_id)


def _try_send_reply(gateway, event, platform, text):
    """Coba kirim balasan lewat adapter gateway secara defensif.

    Nama/method adapter bisa berbeda antar versi Hermes, jadi kita coba
    beberapa kemungkinan dan menelan error. Kalau semua gagal, pesan tetap
    di-skip (command tidak bocor) — hanya balasannya yang tidak terkirim.
    """
    try:
        adapters = getattr(gateway, "adapters", None)
        if not adapters:
            return
        adapter = None
        try:
            adapter = adapters.get(platform)
        except AttributeError:
            adapter = adapters[platform] if platform in adapters else None
        if adapter is None:
            return

        source = getattr(event, "source", None)
        chat_id = getattr(source, "chat_id", None) if source else None

        # Coba beberapa signature method 'send' yang umum.
        import asyncio

        async def _send():
            for method_name in ("send", "send_message", "send_text"):
                method = getattr(adapter, method_name, None)
                if method is None:
                    continue
                try:
                    if chat_id is not None:
                        res = method(chat_id, text)
                    else:
                        res = method(text)
                    if asyncio.iscoroutine(res):
                        await res
                    return True
                except TypeError:
                    # Signature beda; coba kirim via keyword.
                    try:
                        res = method(chat_id=chat_id, text=text)
                        if asyncio.iscoroutine(res):
                            await res
                        return True
                    except Exception:
                        continue
                except Exception:
                    continue
            return False

        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.create_task(_send())
            else:
                loop.run_until_complete(_send())
        except RuntimeError:
            # Tidak ada event loop aktif; jalankan sinkron.
            asyncio.run(_send())
    except Exception as e:  # noqa: BLE001
        logger.warning("block-commands: gagal mengirim balasan: %s", e)


def _pre_gateway_dispatch(event, gateway=None, session_store=None, **kwargs):
    """Cegat pesan sebelum diproses gateway.

    Return:
      {"action": "skip", ...} -> buang pesan (tidak diproses sebagai command)
      None                    -> lanjut normal
    """
    try:
        text, platform, user_id = _extract(event)

        # LOG DIAGNOSTIK: catat setiap pesan yang lewat hook ini.
        logger.info(
            "block-commands: HOOK DIPANGGIL platform=%s user=%s text=%r",
            platform, user_id, text[:60],
        )

        # Batasi ke platform target (default: whatsapp).
        if TARGET_PLATFORMS and platform and platform not in TARGET_PLATFORMS:
            return None

        stripped = text.lstrip()
        # Hanya tangani pesan yang berupa slash command.
        if not stripped.startswith("/"):
            return None

        # Admin boleh semua command.
        if _norm_id(user_id) in ADMIN_IDS:
            return None

        # Non-admin: balas manusiawi lalu skip.
        logger.info(
            "block-commands: memblokir command dari non-admin user=%s platform=%s cmd=%s",
            user_id, platform, stripped.split()[0] if stripped.split() else stripped,
        )
        _try_send_reply(gateway, event, platform, REPLY_TEXT)
        return {"action": "skip", "reason": "non-admin-command-blocked"}
    except Exception as e:  # noqa: BLE001
        # Fail-safe: kalau ada error tak terduga, jangan sampai memblokir
        # pesan normal. Biarkan lanjut seperti biasa.
        logger.warning("block-commands: error di hook, meneruskan pesan: %s", e)
        return None


def register(ctx):
    ctx.register_hook("pre_gateway_dispatch", _pre_gateway_dispatch)
    logger.info("block-commands: hook pre_gateway_dispatch terpasang (admin=%s)", ADMIN_IDS)
