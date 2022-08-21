import time
import requests
import cleantext
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

    articles = response.json()["items"]
    min_publication_ts = time.time() - period

    for article in articles.copy():

        if (
            article["type"] != "article"
            or article["sponsored"] is True
            or article["inMain"] is False
            or article["hasContent"] is False
            or article["publication"] < min_publication_ts
        ):
            articles.remove(article)

    return articles


def _preprocess_raw_article(article: dict) -> dict:

    title = article["title"]
    article_url = article["sharingLink"]

    # Clean the article's title.
    title = title.strip(".")
    title = cleantext.clean(title, lower=False)

    get_body = lambda: summarie.from_url(article_url)  # noqa: E731

    return {
        "title": title,
        "get_body": get_body,
    }


def last_news_articles(period: int) -> list[dict]:

    raw_articles = _scrape_last_articles(period)
    articles = [_preprocess_raw_article(article) for article in raw_articles]

    return articles
