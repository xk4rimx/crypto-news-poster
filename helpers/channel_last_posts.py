import requests
import bs4


def channel_last_posts(username: str) -> list:

    username = username.strip("@")

    response = requests.get(f"https://t.me/s/{username}")
    response.raise_for_status()

    html = response.text
    soup = bs4.BeautifulSoup(html, "lxml")

    results = soup.find_all(
        "div", {"class": "tgme_widget_message_text js-message_text"}
    )

    posts = [r.text for r in results]
    return posts
