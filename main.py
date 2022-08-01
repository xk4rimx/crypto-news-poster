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

    title = article["title"]
    subtitle = article["subtitle"]
    timestamp = article["timestamp"]
    source_url = article["source_url"]

    # If the article was published within the last 15 minutes.
    if timestamp >= (time.time() - 60 * 15):

        posts = helpers.channel_last_posts(
            TELEGRAM_CHANNEL_ID,
        )

        if not any(title in p for p in posts):

            text = TELEGRAM_ARTICLE_FORMAT.format(
                title=title,
                subtitle=subtitle,
                source_url=source_url,
            )

            helpers.send_telegram_msg(
                bot_token=TELEGRAM_BOT_TOKEN,
                username=TELEGRAM_CHANNEL_ID,
                text=text,
            )

        else:
            logger.info(
                "Last article was already published in the Telegram channel. ",
            )

    else:
        logger.info(
            "Last article was not published within the last fifteen minutes. "
            "It was published at %f",
            timestamp,
        )


if __name__ == "__main__":
    main()
