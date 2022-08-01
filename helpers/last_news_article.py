import datetime
import zoneinfo
import dateutil.parser as dparser
import bs4
import requests
import fastpunct

fp = fastpunct.FastPunct(
    checkpoint_local_path=".fastpunct/",
)


def _get_last_articles(coin: str) -> dict:

    sess = requests.Session()

    html = sess.get("https://cryptonews-api.com/").text
    soup = bs4.BeautifulSoup(html, "lxml")

    csrf_element = soup.find("meta", {"name": "csrf-token"})
    csrf_token = csrf_element["content"]

    data = {
        "token": "demo",
        "tickers": coin,
        "_token": csrf_token,
    }

    response = sess.post(
        "https://cryptonews-api.com/demo/index",
        headers={"content-type": "application/x-www-form-urlencoded"},
        data=data,
    )

    response.raise_for_status()
    return response.json()["data"]


def _preproccess_article_data(article: dict) -> tuple[str, str, float, str]:

    title = article["title"]
    subtitle = article["text"]
    date = article["date"]
    source_url = article["news_url"]

    # Fix punctuation issues in the subtitle.
    subtitle = fp.punct(subtitle)

    # Convert date from UTC to local time, and then into a timestamp.
    date = dparser.parse(date).astimezone(zoneinfo.ZoneInfo("localtime"))
    timestamp = datetime.datetime.timestamp(date)

    return title, subtitle, timestamp, source_url


def last_news_article(coin: str) -> dict:

    articles = _get_last_articles(coin)
    articles = [article for article in articles if len(article["tickers"]) == 1]

    last_article = articles[0]
    title, subtitle, timestamp, source_url = _preproccess_article_data(
        last_article,
    )

    return {
        "title": title,
        "subtitle": subtitle,
        "timestamp": timestamp,
        "source_url": source_url,
    }
