import time
import requests
import summarie


def _scrape_last_articles(period: int) -> list:

    response = requests.get(
        "https://cnews24.ru/m-api/news/v4/articles/",
        params={
            "rubricId": 0,
            "locale": "en",
        },
    )

    response.raise_for_status()
    articles = response.json()["items"]

    for article in articles.copy():

        if (
            article["type"] == "article"
            and article["sponsored"] is False
            and article["inMain"] is True
            and article["hasContent"] is True
            and article["publication"] >= (time.time() - period)
        ):
            continue

        articles.remove(article)

    return articles


def _preproccess_raw_article(article: dict) -> tuple[str, str]:

    title = article["title"]
    title = title.replace(".", "")

    source_url = article["sharingLink"]
    source_url = source_url.split("?")[0]

    get_summary = lambda: summarie.from_url(source_url)  # noqa: E731
    return title, get_summary


def last_news_articles(period: int) -> dict:

    raw_articles = _scrape_last_articles(period)
    articles = []

    for article in raw_articles:

        title, get_summary = _preproccess_raw_article(article)
        articles.append(
            {
                "title": title,
                "get_summary": get_summary,
            },
        )

    return articles
