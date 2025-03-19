import requests
from app.config import STABILITY_API_KEY, API_KEY
from app.utils.llm_utils import get_llm_response

async def generate_image_prompt(scene: str):
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
    return response.strip()

async def generate_image(scene: str):
    if not STABILITY_API_KEY:
        return None

    # Generate the image prompt
    image_prompt = generate_image_prompt(scene)

    url = "https://api.stability.ai/v1/generation/stable-diffusion-v1-5/text-to-image"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {STABILITY_API_KEY}"
    }
    payload = {
        "text_prompts": [{"text": image_prompt}],
        "cfg_scale": 7,
        "clip_guidance_preset": "FAST_BLUE",
        "height": 512,
        "width": 512,
        "samples": 1,
        "steps": 30,
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        image_url = data["artifacts"][0]["base64"]
        return f"data:image/png;base64,{image_url}"
    else:
        raise Exception(f"Image generation failed: {response.text}")