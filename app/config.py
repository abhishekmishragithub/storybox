import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TUNEAI_API_KEY")
ORG_ID = os.getenv("TUNEAI_ORG_ID")
STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")
