from app.utils.llm_utils import get_llm_response

def generate_image_prompt(scene: str):
    messages = [
        {
            "role": "system",
            "content": """You are an image prompt creator. Your task is to create a detailed image prompt based on 
            the given scene. The prompt should describe the key visual elements, mood, and composition 
            that would best represent the scene in an illustration. Be specific and vivid in your description."""
        },
        {
            "role": "user",
            "content": f"Please create an image prompt for this scene:\n\n{scene}"
        }
    ]

    response = get_llm_response(messages, max_tokens=200)
    return response