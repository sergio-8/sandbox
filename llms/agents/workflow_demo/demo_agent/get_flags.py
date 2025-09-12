import os
import dotenv

dotenv.load_dotenv(override=True)

PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT", "ucs-ga-fishfood-1")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
ENGINE_ID = os.getenv("ENGINE_ID", "cloudia-search-app_1747840893036")
MODEL = os.getenv("MODEL", "gemini-2.0-flash-001")

