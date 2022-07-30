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

    if response.status_code != 200:
        raise ValueError(response.json())
