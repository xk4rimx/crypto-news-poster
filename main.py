# This script supposes that you executed it every 30 minutes.

import os
import logging
import dotenv
import helpers

logging.basicConfig(level=logging.DEBUG)
dotenv.load_dotenv()

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHANNEL_ID = "@crypto_reports"
TELEGRAM_ARTICLE_FORMAT = "*{title}*\n\n{summary}"


def main():

    articles = helpers.last_news_articles(
        period=12 * (60 * 60),
    )

    if articles:
        posts = helpers.telegram_last_posts(
            TELEGRAM_CHANNEL_ID,
        )

    for article in articles:

        # get_summary: Computationally intensive function; only executed when needed.

        title = article["title"]
        get_summary = article["get_summary"]

        if not any(title in p for p in posts):

            text = TELEGRAM_ARTICLE_FORMAT.format(
                title=title,
                summary=get_summary(),
            )

            helpers.send_telegram_msg(
                bot_token=TELEGRAM_BOT_TOKEN,
                username=TELEGRAM_CHANNEL_ID,
                text=text,
            )


if __name__ == "__main__":
    main()
