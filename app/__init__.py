from flask import Flask
from config import Config
from .model import ModelSingleton
from supabase import create_client, Client
import os

# Global variable for Supabase client
supabase_client = None

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize model singleton
    ModelSingleton.get_instance()
    
    # Initialize Supabase client
    global supabase_client
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    supabase_client = create_client(url, key)
    
    # Register blueprints
    from .routes import main
    app.register_blueprint(main)
    
    return app