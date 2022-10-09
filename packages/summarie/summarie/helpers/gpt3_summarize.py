import openai


def gpt3_summarize(text: str, openai_key: str) -> str:

    openai.api_key = openai_key
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=f"Summarize this for a second-grade student:\n\n{text}",
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    summary = response.choices[0].text
    return summary
