# This script is supposed to be executed once every hour.

import os
import logging
import dotenv
import helpers

logging.basicConfig(level=logging.DEBUG)
dotenv.load_dotenv()

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_NEWS_CHANNEL_USERNAME = os.environ["TELEGRAM_NEWS_CHANNEL_USERNAME"]
TELEGRAM_NEWS_ARTICLE_FORMAT = os.environ["TELEGRAM_NEWS_ARTICLE_FORMAT"]


def main():

    articles = helpers.last_news_articles()

    if articles:
        posts = helpers.telegram_last_posts(
            TELEGRAM_NEWS_CHANNEL_USERNAME,
        )

    for article in articles:

        title = article["title"]
        get_body = article["get_body"]

        if not any(title in p for p in posts):

            # Generate the article's body.
            body = get_body()

            text = TELEGRAM_NEWS_ARTICLE_FORMAT.format(
                title=title,
                body=body,
            )

            helpers.send_telegram_msg(
                bot_token=TELEGRAM_BOT_TOKEN,
                username=TELEGRAM_NEWS_CHANNEL_USERNAME,
                text=text,
            )


if __name__ == "__main__":
    main()
