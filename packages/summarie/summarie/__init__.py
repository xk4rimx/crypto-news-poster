from . import helpers

import re
import newspaper
import cleantext


def _clean_text(text: str) -> str:

    text = cleantext.clean(
        text=text,
        lower=False,
        keep_two_line_breaks=True,
    )

    # Remove spaces before punctuation
    re.sub(r"\s+([^\w\s])", r"\1", text)

    return text


def from_text(text: str) -> str:

    """Generates a summary from the given text."""

    text = _clean_text(text)
    summary = helpers.bart_summarize(text)
    summary = _clean_text(summary)

    return summary


def from_url(url: str) -> str:

    """Generates a summary from the given article link."""

    article = newspaper.Article(url)

    article.download()
    article.parse()

    text = f"{article.title}\n\n{article.text}"
    return from_text(text)
