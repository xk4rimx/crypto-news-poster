from . import helpers
import newspaper


def from_text(text: str) -> str:

    """Generates a summary from the given text"""

    results = helpers.fb_bart_api(inputs=text)
    summary = results[0]["summary_text"]

    return summary


def from_url(url: str) -> str:

    """Generates a summary from the given article link"""

    article = newspaper.Article(url)

    article.download()
    article.parse()

    text = article.text
    return from_text(text=text)
