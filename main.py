# This script supposes that you executed it every hour.

import os
import logging
import dotenv
import helpers

logging.basicConfig(level=logging.DEBUG)
dotenv.load_dotenv()

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHANNEL_ID = os.environ["TELEGRAM_CHANNEL_ID"]
TELEGRAM_ARTICLE_FORMAT = os.environ["TELEGRAM_ARTICLE_FORMAT"]


def main():

    articles = helpers.last_news_articles(
        period=12 * (60 * 60),
    )

    if articles:
        posts = helpers.telegram_last_posts(
            TELEGRAM_CHANNEL_ID,
        )

    for article in articles:

        title = article["title"]
        gen_summary_func = article["gen_summary_func"]

        if not any(title in p for p in posts):

            # Generate the article's summary.
            summary = gen_summary_func()

            text = TELEGRAM_ARTICLE_FORMAT.format(
                title=title,
                summary=summary,
            )

            helpers.send_telegram_msg(
                bot_token=TELEGRAM_BOT_TOKEN,
                username=TELEGRAM_CHANNEL_ID,
                text=text,
            )


if __name__ == "__main__":
    main()
