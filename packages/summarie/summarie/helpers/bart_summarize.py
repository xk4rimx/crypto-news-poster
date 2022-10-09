import requests


def bart_summarize(text: str, huggingface_key: str = None) -> str:

    headers = None
    if huggingface_key is not None:
        headers = {"Authorization": f"Bearer {huggingface_key}"}

    response = requests.post(
        "https://api-inference.huggingface.co/models/facebook/bart-large-cnn",
        headers=headers,
        json={
            "inputs": text,
            "options": {"wait_for_model": True},
        },
    )

    response.raise_for_status()

    data = response.json()
    summary = data[0]["summary_text"]

    return summary
