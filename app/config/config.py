import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATABASE_PATH = os.getenv('DATABASE_PATH', None)