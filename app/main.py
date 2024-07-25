import logging
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.services.story_service import generate_story
from app.services.scene_service import break_into_scenes
from app.services.image_service import generate_image_prompt

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/generate", response_class=HTMLResponse)
async def generate(request: Request, prompt: str = Form(...), style: str = Form(...), length: str = Form(...)):
    try:
        logger.info(f"Generating story with prompt: {prompt}, style: {style}, length: {length}")

        # Generate the story
        story = generate_story(prompt, style, length)
        logger.info(f"Generated story: {story[:100]}...")  # Log first 100 characters

        # Break the story into scenes
        scenes = break_into_scenes(story)
        logger.info(f"Generated scenes: {scenes[:100]}...")  # Log first 100 characters

        # Generate image prompts for each scene
        image_prompts = [generate_image_prompt(scene) for scene in scenes.split("\n") if scene.strip()]
        logger.info(f"Generated {len(image_prompts)} image prompts")

        return templates.TemplateResponse("index.html", {
            "request": request,
            "story": story,
            "scenes": scenes,
            "image_prompts": image_prompts
        })
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": str(e)
        }, status_code=500)


@app.get("/health")
async def health_check():
    return {"status": "ok"}