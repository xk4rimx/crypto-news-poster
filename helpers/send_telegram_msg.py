import requests


def send_telegram_msg(bot_token: str, chat_id: int, text: str) -> None:

    response = requests.post(
        f"https://api.telegram.org/bot{bot_token}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "Markdown",
        },
    )

    if response.status_code != 200:
        raise ValueError(response.json())
