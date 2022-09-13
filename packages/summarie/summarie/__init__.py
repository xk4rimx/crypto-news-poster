from . import helpers

import re
import newspaper
import cleantext


def _clean_summary(text: str) -> str:

    # Clean the text in a general way.
    text = cleantext.clean(
        text=text,
        lower=False,
        keep_two_line_breaks=True,
    )

    replacements = [
        (" , ", ", "),
        (" . ", ". "),
        (" - ", " – "),
        (" -- ", " – "),
    ]

    for old, new in replacements:
        text = text.replace(old, new)

    # Remove text between brackets.
    text = re.sub(r"\([^()]*\)", "", text)

    # Clean the text again due to the above replacements.
    text = cleantext.clean(
        text=text,
        to_ascii=False,
        lower=False,
        keep_two_line_breaks=True,
    )

    return text


def from_text(text: str) -> str:

    """Generates a summary from the given text."""

    response_data = helpers.facebook_bart_api(inputs=text)

    summary = response_data[0]["summary_text"]
    summary = _clean_summary(summary)

    return summary


def from_url(url: str) -> str:

    """Generates a summary from the given article link."""

    article = newspaper.Article(url)

    article.download()
    article.parse()

    text = f"{article.title}\n\n{article.text}"
    return from_text(text)
