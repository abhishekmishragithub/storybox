from app.utils.llm_utils import get_llm_response

def generate_story(prompt: str, style: str, length: str):
    length_tokens = {"short": 500, "medium": 1000, "long": 1500}
    max_tokens = length_tokens.get(length.lower(), 1000)

    messages = [
        {
            "role": "system",
            "content": f"You are a creative story writer. Your task is to write a {length} story in a {style} style based on the following prompt: '{prompt}'. Be imaginative and engaging. The story should have a clear beginning, middle, and end."
        },
        {
            "role": "user",
            "content": "Please write the story now."
        }
    ]

    response = get_llm_response(messages, max_tokens=max_tokens)
    return response