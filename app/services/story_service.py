from app.utils.llm_utils import get_llm_response

async def generate_story(prompt: str, style: str, length: str, narration: str):
    length_tokens = {"short": 500, "medium": 1000, "long": 1500}
    max_tokens = length_tokens.get(length.lower(), 1000)

    if narration == "grandma":
        system_message = f"""You are a loving grandmother telling a {length} story in a {style} style to your grandchildren. 
        Be imaginative, engaging, and use a warm, comforting tone. The story should have a clear beginning, middle, and end, 
        and include gentle life lessons. Use simple language and occasional endearing terms like 'dearie' or 'sweetie'."""
        user_message = "Please tell us a story, Grandma!"
    else:
        system_message = f"""You are a creative story writer. Your task is to write a {length} story in a {style} style 
        based on the following prompt: '{prompt}'. Be imaginative and engaging. The story should have 
        a clear beginning, middle, and end."""
        user_message = "Please write the story now."

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message}
    ]

    response = get_llm_response(messages, max_tokens=max_tokens)
    return response

async def generate_title(story: str):
    messages = [
        {"role": "system", "content": "You are a creative title generator. Create a short, engaging title for the given story."},
        {"role": "user", "content": f"Generate a title for this story:\n\n{story[:500]}..."}
    ]
    response = get_llm_response(messages, max_tokens=20)
    return response.strip()