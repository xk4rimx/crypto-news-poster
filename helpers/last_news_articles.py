import time
import datetime
import zoneinfo
import dateutil.parser as dparser
import bs4
import requests
import faker
import fastpunct

fp = fastpunct.FastPunct()
fake = faker.Faker()


def _get_last_articles() -> dict:

    sess = requests.Session()
    sess.headers.update = {
        "user-agent": fake.user_agent(),
    }

    html = sess.get("https://cryptonews-api.com/").text
    soup = bs4.BeautifulSoup(html, "lxml")

    csrf_element = soup.find("meta", {"name": "csrf-token"})
    csrf_token = csrf_element["content"]

    data = {
        "token": "demo",
        "_token": csrf_token,
    }

    response = sess.post(
        "https://cryptonews-api.com/demo/trending-headlines",
        data=data,
    )

    response.raise_for_status()
    return response.json()["data"]


def _preproccess_article_data(article: dict) -> tuple[str, str, float, str]:

    title = article["headline"]
    description = article["text"]
    date = article["date"]

    # Fix punctuation issues in the description.
    description = fp.punct(description)

    # Convert date from UTC to local time, and then into a timestamp.
    date = dparser.parse(date).astimezone(zoneinfo.ZoneInfo("localtime"))
    timestamp = datetime.datetime.timestamp(date)

    return title, description, timestamp


def last_news_articles(period: int) -> dict:

    raw_articles = _get_last_articles()
    articles = []

    for article in raw_articles:

        title, description, timestamp = _preproccess_article_data(
            article,
        )

        if timestamp >= (time.time() - period):
            articles.append(
                {
                    "title": title,
                    "description": description,
                },
            )

    return articles
