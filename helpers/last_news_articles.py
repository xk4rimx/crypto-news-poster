import time
import subprocess
import requests

SUMMY_ALGORITHMS = [
    "luhn",
    "edmundson",
    "lsa",
    "text-rank",
    "lex-rank",
    "sum-basic",
    "kl",
]


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
    title = title.strip(".")

    source_url = article["sharingLink"]
    source_url = source_url.split("?")[0]

    summaries = []

    for algo in SUMMY_ALGORITHMS:

        try:
            summary = subprocess.run(
                ["sumy", algo, "--length=1", f"--url={source_url}"],
                capture_output=True,
                check=True,
            )
        except subprocess.CalledProcessError:
            continue

        summary = summary.stdout
        summary = summary.decode().strip("\n")

        summaries.append(summary)

    summary = max(set(summaries), key=summaries.count)  # most freq
    return title, summary


def last_news_articles(period: int) -> dict:

    raw_articles = _scrape_last_articles(period)
    articles = []

    for article in raw_articles:

        title, summary = _preproccess_raw_article(article)
        articles.append(
            {
                "title": title,
                "summary": summary,
            },
        )

    return articles
