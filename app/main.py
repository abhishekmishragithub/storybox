import logging
from logging.handlers import RotatingFileHandler
import asyncio
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from app.services.story_service import generate_story, generate_title
from app.services.scene_service import break_into_scenes
from app.services.image_service import generate_image, generate_image_prompt
from app.utils.emoji_utils import add_emoji_to_title
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

file_handler = RotatingFileHandler('app.log', maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

app = FastAPI()
current_dir = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(current_dir, "templates"))
app.mount("/app/static", StaticFiles(directory=os.path.join(current_dir, "static")), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    logger.info("Rendering home page")
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate")
async def generate(
    request: Request,
    prompt: str = Form(None),
    style: str = Form(...),
    length: str = Form(...),
    narration: str = Form(...)
):
    logger.info(f"Starting story generation with parameters: prompt='{prompt}', style='{style}', length='{length}', narration='{narration}'")

    async def event_generator():
        try:
            # Generate the story
            logger.info("Generating story")
            yield "event: story_start\ndata: Generating story...\n\n"
            if narration == "grandma":
                story = await generate_story(None, style, length, narration)
            else:
                story = await generate_story(prompt, style, length, narration)
            logger.info("Story generated")
            yield f"event: story\ndata: {story}\n\n"

            # Generate title
            logger.info("Generating title")
            yield "event: title_start\ndata: Creating a title...\n\n"
            title = await generate_title(story)
            title_with_emoji = add_emoji_to_title(title)
            logger.info(f"Title generated: {title_with_emoji}")
            yield f"event: title\ndata: {title_with_emoji}\n\n"

            # Break the story into scenes
            logger.info("Breaking story into scenes")
            yield "event: scenes_start\ndata: Breaking story into scenes...\n\n"
            scenes = await break_into_scenes(story)
            logger.info(f"Generated {len(scenes.split())} scenes")
            yield f"event: scenes\ndata: {scenes}\n\n"

            # Generate images for each scene asynchronously
            async def generate_image_for_scene(scene, index):
                try:
                    image_prompt = await generate_image_prompt(scene)
                    logger.info(f"Generated image prompt for scene {index+1}")
                    image_url = await generate_image(image_prompt)
                    logger.info(f"Generated image for scene {index+1}")
                    return f"event: image\ndata: {{'scene': {index}, 'url': '{image_url}'}}\n\n"
                except Exception as e:
                    logger.error(f"Error generating image for scene {index+1}: {str(e)}")
                    return f"event: image_error\ndata: {{'scene': {index}, 'error': '{str(e)}'}}\n\n"

            image_tasks = [generate_image_for_scene(scene, i) for i, scene in enumerate(scenes.split("\n")) if scene.strip()]
            for completed_task in asyncio.as_completed(image_tasks):
                yield await completed_task

            logger.info("Story generation complete")
            yield "event: complete\ndata: Generation complete\n\n"
        except Exception as e:
            logger.error(f"Error during story generation: {str(e)}")
            yield f"event: error\ndata: {str(e)}\n\n"

    logger.info("Starting event stream")
    return StreamingResponse(event_generator(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting the application")
    uvicorn.run(app, host="0.0.0.0", port=8000)