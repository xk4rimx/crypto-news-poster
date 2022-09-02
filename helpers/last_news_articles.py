import time
import functools
import requests
import requests_random_user_agent
import summarie


def last_news_articles(period: int = 86400) -> list[dict]:

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

        article_id = article["id"]
        article_link = article["sharingLink"]

        get_article_text = functools.partial(
            summarie.from_url,
            article_link,
        )

        articles.append(
            {
                "id": str(article_id),
                "get_article_text": get_article_text,
            },
        )

    return articles
