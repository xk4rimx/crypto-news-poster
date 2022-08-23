import time
import functools
import requests
import summarie


def _scrape_last_articles(period: int) -> list[dict]:

    response = requests.get(
        "https://cnews24.ru/m-api/news/v4/articles/",
        params={
            "rubricId": 0,
            "locale": "en",
        },
    )

    response.raise_for_status()

    raw_articles = response.json()["items"]
    min_publication_ts = time.time() - period

    articles = []

    for article in raw_articles:

        if (
            article["type"] != "article"
            or article["sponsored"] is True
            or article["inMain"] is False
            or article["hasContent"] is False
            or article["publication"] < min_publication_ts
        ):
            continue

        title = article["title"]
        link = article["sharingLink"]

        get_body = functools.partial(summarie.from_url, link)

        articles.append(
            {
                "title": title,
                "get_body": get_body,
            },
        )

    return articles


def last_news_articles(period: int = 86400) -> list[dict]:
    return _scrape_last_articles(period)
