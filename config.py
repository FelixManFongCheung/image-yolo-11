import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SUPABASE_URL = os.environ.get("SUPABASE_URL")
    SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
    SUPABASE_DB_URL = os.environ.get("SUPABASE_DB_URL")
    MODEL_PATH = "yolo11n.pt"
    DEBUG = True