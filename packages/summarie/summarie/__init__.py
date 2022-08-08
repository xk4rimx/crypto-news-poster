from . import helpers

import re
import newspaper
import cleantext


def _clean_text(text: str) -> str:

    text = cleantext.clean(text)  # replace non-ascii to closest ascii
    text = text.replace('"', "")  # remove quotes
    text = re.sub(r"\([^()]*\)", "", text)  # remove text between brackets
    text = cleantext.clean(text)  # general cleaning

    return text


def from_text(text: str) -> str:

    """Generates a summary from the given text"""

    text = _clean_text(text)

    results = helpers.fb_bart_api(inputs=text)
    summary = results[0]["summary_text"].lower()

    return summary


def from_url(url: str) -> str:

    """Generates a summary from the given article link"""

    article = newspaper.Article(url)

    article.download()
    article.parse()

    text = article.text
    return from_text(text=text)
