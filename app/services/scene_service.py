from app.utils.llm_utils import get_llm_response

def break_into_scenes(story: str):
    messages = [
        {
            "role": "system",
            "content": """You are a story analyst. Your task is to break down the given story into distinct scenes. 
            Each scene should represent a significant moment or change in the story. Provide a brief 
            description for each scene. Number each scene and separate them with newlines."""
        },
        {
            "role": "user",
            "content": f"Please break this story into scenes:\n\n{story}"
        }
    ]

    response = get_llm_response(messages, max_tokens=1000)
    return response