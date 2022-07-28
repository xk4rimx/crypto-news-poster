# This script supposes that you executed it every 10 minutes.

import os
import time
import dotenv
import helpers

dotenv.load_dotenv()

TELEGRAM_CHANNEL_ID = -1001575823286
TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_ARTICLE_FORMAT = "\n*{title}*\n\n{subtitle} [Read more]({source_url})\nㅤ"


def main():

    article = helpers.last_news_article("BTC")
    article_timestamp = article["timestamp"]

    # If the article was published within the last 10 minutes.
    if article_timestamp >= (time.time() - 600):

        helpers.send_telegram_msg(
            TELEGRAM_BOT_TOKEN,
            TELEGRAM_CHANNEL_ID,
            TELEGRAM_ARTICLE_FORMAT.format(
                title=article["title"],
                subtitle=article["subtitle"],
                source_url=article["source_url"],
            ),
        )


if __name__ == "__main__":
    main()
