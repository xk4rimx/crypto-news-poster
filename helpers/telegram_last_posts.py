import requests
import bs4


def telegram_last_posts(username: str) -> list[str]:

    username = username.strip("@")

    response = requests.get(f"https://t.me/s/{username}")
    response.raise_for_status()

    html = response.text
    soup = bs4.BeautifulSoup(html, "lxml")

    results = soup.find_all(
        "div", {"class": "tgme_widget_message_text js-message_text"}
    )

    posts = [result.text for result in results]
    return posts
