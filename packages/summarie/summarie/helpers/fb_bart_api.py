import requests


def fb_bart_api(inputs: str) -> str:

    response = requests.post(
        "https://api-inference.huggingface.co/models/facebook/bart-large-cnn",
        json={
            "inputs": inputs,
            "parameters": {"temperature": 0},
            "options": {"wait_for_model": True},
        },
    )

    response.raise_for_status()
    return response.json()
