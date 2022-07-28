import datetime
import zoneinfo
import dateutil.parser as dparser
import requests
import sorcery


def last_news_article(coin: str) -> dict:

    match coin:

        case "BTC":
            coin_id = 1

        case "ETH":
            coin_id = 2

        case _:
            raise ValueError(f"unsupported coin: {coin}")

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

    title = last_article_data["title"]
    subtitle = last_article_data["subtitle"]
    date = last_article_data["createdAt"]
    source_url = last_article_data["sourceUrl"]

    subtitle = subtitle.replace(" ...", "...")  # Sometimes ending be "xxx ..."
    subtitle = subtitle.replace("\n", " ")
    subtitle = subtitle.replace(" " * 2, " ")

    date = dparser.parse(date).astimezone(zoneinfo.ZoneInfo("localtime"))
    timestamp = datetime.datetime.timestamp(date)

    # Return a dict containing variables values. {"title": title, ...}
    return sorcery.dict_of(
        title,
        subtitle,
        timestamp,
        source_url,
    )
