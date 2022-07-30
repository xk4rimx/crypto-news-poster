import string
import datetime
import zoneinfo
import html
import dateutil.parser as dparser
import requests
import sorcery


def _preproccess_article_data(article: dict) -> tuple[str, str, float, str]:

    title = article["title"]
    subtitle = article["subtitle"]
    date = article["createdAt"]
    source_url = article["sourceUrl"]

    # Convert date from UTC to local time, and then into a timestamp.
    date = dparser.parse(date).astimezone(zoneinfo.ZoneInfo("localtime"))
    timestamp = datetime.datetime.timestamp(date)

    # Decode any HTML phrases.
    title = html.unescape(title)
    subtitle = html.unescape(subtitle)

    # Remove non ASCII characters.
    title = title.encode("ascii", errors="ignore").decode()
    subtitle = subtitle.encode("ascii", errors="ignore").decode()

    #######################

    # Remove any non necessary characters (e.g. white space)
    # before and after the title and the subtitle.

    printable_ascii_chars = tuple(
        string.ascii_letters + string.digits + string.punctuation
    )

    while not title.startswith(printable_ascii_chars) and title != "":
        title = title[1:]

    while not title.endswith(printable_ascii_chars) and title != "":
        title = title[:-1]

    while not subtitle.startswith(printable_ascii_chars) and subtitle != "":
        subtitle = subtitle[1:]

    while not subtitle.endswith(printable_ascii_chars) and subtitle != "":
        subtitle = subtitle[:-1]

    #######################

    # Preproccess the subtitle's ending.

    while not subtitle.endswith(".") and subtitle != "":
        subtitle = subtitle[:-1]

    if not subtitle.endswith("...") and subtitle != "":
        subtitle += ".."

    if subtitle.endswith(" ..."):
        subtitle = subtitle.replace(" ...", "...")

    #######################

    return title, subtitle, timestamp, source_url


def last_news_article(coin: str) -> dict:

    match coin:

        case "BTC":
            coin_id = 1

        case "ETH":
            coin_id = 2

        case _:
            raise ValueError(
                f"unsupported coin: {coin}",
            )

    headers = {
        "authority": "api.coinmarketcap.com",
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-GB,en;q=0.9",
        "platform": "web",
        "user-agent": "Firefox/47.0",
    }

    params = {
        "coins": coin_id,
        "page": "1",
        "size": "1",
    }

    response = requests.get(
        "https://api.coinmarketcap.com/content/v3/news",
        params=params,
        headers=headers,
    )

    response_data = response.json()["data"]
    last_article_data = response_data[0]["meta"]

    title, subtitle, timestamp, source_url = _preproccess_article_data(
        last_article_data
    )

    # Return a dict containing variables values. {"title": title, ...}
    return sorcery.dict_of(
        title,
        subtitle,
        timestamp,
        source_url,
    )
