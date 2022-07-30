# This script supposes that you executed it every 10 minutes.

import os
import time
import logging
import dotenv
import helpers

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

dotenv.load_dotenv()

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHANNEL_ID = "@btc_newsletter"
TELEGRAM_ARTICLE_FORMAT = "\n*{title}*\n\n{subtitle} [Read more]({source_url})\nㅤ"


def main():

    article = helpers.last_news_article("BTC")
    required_words = [
        "btc",
        "bitcoin",
    ]

    article_title = article["title"]
    article_subtitle = article["subtitle"]
    article_timestamp = article["timestamp"]

    if not any(w in article_title.lower() for w in required_words):

        logger.info(
            "Last article does not contain any of the required keywords. "
            "Last article title: %s",
            article_title,
        )

        return None

    if article_title == "" or article_subtitle == "":

        logger.info(
            "Last article's title or subtitle is empty. Last article title: %s",
            article_title,
        )

        return None

    # If the article was not published within the last 15 minutes.
    if not article_timestamp >= (time.time() - 60 * 15):

        logger.info(
            "Last article was not published within the last fifteen minutes. "
            "It was published at %f",
            article_timestamp,
        )

        return None

    posts = helpers.channel_last_posts(
        TELEGRAM_CHANNEL_ID,
    )

    if any(article_title in p for p in posts):

        logger.info(
            "Last article was already published in the Telegram channel. "
            "Number of duplicates: %d",
            [article_title in p for p in posts].count(True),
        )

        return None

    text = TELEGRAM_ARTICLE_FORMAT.format(
        title=article["title"],
        subtitle=article["subtitle"],
        source_url=article["source_url"],
    )

    helpers.send_telegram_msg(
        bot_token=TELEGRAM_BOT_TOKEN,
        chat_id=TELEGRAM_CHANNEL_ID,
        text=text,
    )


if __name__ == "__main__":
    main()
