# This script is supposed to be executed once every hour.

import os
import logging
import dotenv
import helpers

logging.basicConfig(level=logging.DEBUG)
dotenv.load_dotenv()

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_LOGS_CHANNEL_USERNAME = os.environ["TELEGRAM_LOGS_CHANNEL_USERNAME"]
TELEGRAM_NEWS_CHANNEL_USERNAME = os.environ["TELEGRAM_NEWS_CHANNEL_USERNAME"]


def main():

    articles = helpers.last_news_articles()

    if not articles:
        return

    logs = helpers.telegram_last_posts(
        TELEGRAM_LOGS_CHANNEL_USERNAME,
    )

    for article in articles:

        article_id = article["id"]
        get_article_text = article["get_article_text"]

        if article_id in logs:
            continue

        # We get the article text before sending logs so that the article
        # doesn't get marked as posted when an exception occurs
        # and the script stops.

        text = get_article_text()

        helpers.send_telegram_msg(
            bot_token=TELEGRAM_BOT_TOKEN,
            username=TELEGRAM_LOGS_CHANNEL_USERNAME,
            text=article_id,
        )

        helpers.send_telegram_msg(
            bot_token=TELEGRAM_BOT_TOKEN,
            username=TELEGRAM_NEWS_CHANNEL_USERNAME,
            text=text,
        )


if __name__ == "__main__":
    main()
