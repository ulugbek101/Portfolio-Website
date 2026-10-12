import logging
from html import escape

import requests
from django.conf import settings

logger = logging.getLogger(__name__)

API_URL = "https://api.telegram.org/bot{token}/sendMessage"


def admin_ids():
    ids = []
    for raw in settings.FIRA_ADMINS_LIST:
        raw = str(raw).strip()
        if raw.lstrip("-").isdigit():
            ids.append(int(raw))
        elif raw:
            logger.warning("FIRA_ADMINS_LIST: ignoring non-numeric value %r", raw)
    return ids


def send_callback_request(name, phone, lang, submitted_at):
    """Send a challenge-page callback request to every admin in Telegram.

    One admin failing (typically because they never pressed /start in the bot,
    or blocked it) never prevents the others from receiving the message.
    """
    token = settings.FIRA_BOT_TOKEN
    ids = admin_ids()
    if not token or not ids:
        logger.error("Callback request not sent: FIRA_BOT_TOKEN or FIRA_ADMINS_LIST is not configured")
        return {"sent": 0, "failed": 0}

    text = (
        "\U0001F4DE <b>Новая заявка на обратный звонок</b>\n"
        "Челлендж: Stylist Challenge\n\n"
        f"<b>Имя:</b> {escape(name)}\n"
        f"<b>Телефон:</b> {escape(phone)}\n"
        f"<b>Язык страницы:</b> {'узбекский' if lang == 'uz' else 'русский'}\n"
        f"<b>Время:</b> {escape(submitted_at)}"
    )

    sent = failed = 0
    for chat_id in ids:
        try:
            resp = requests.post(
                API_URL.format(token=token),
                json={"chat_id": chat_id, "text": text, "parse_mode": "HTML"},
                timeout=5,
            )
            if resp.ok:
                sent += 1
            else:
                failed += 1
                # 403 = admin has not sent /start to the bot yet (or blocked it).
                logger.warning(
                    "Callback request not delivered to admin %s: HTTP %s %s",
                    chat_id, resp.status_code, resp.text[:200],
                )
        except Exception:
            failed += 1
            logger.exception("Callback request failed for admin %s", chat_id)
    return {"sent": sent, "failed": failed}
