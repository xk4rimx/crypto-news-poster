import requests


def send_telegram_msg(bot_token: str, username: str, text: str) -> None:

    if not username.startswith("@"):
        username = "@" + username

    response = requests.post(
        f"https://api.telegram.org/bot{bot_token}/sendMessage",
        json={
            "chat_id": username,
            "text": text,
            "parse_mode": "Markdown",
        },
    )

    response.raise_for_status()
