import os  
from dotenv import load_dotenv  
  
load_dotenv()  

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")  
LOG_PATH = os.getenv("LOG_PATH", "./logs/app.log") 

HEALTH_CHECK = os.getenv("HEALTH_CHECK", "/health")

DEFAULT_COMPLETION_MODEL = os.getenv("DEFAULT_COMPLETION_MODEL", "gemini-1.5-flash")

BASE_API_URL = os.getenv("BASE_API_URL", "https://10.216.70.62/DEV/litellm/chat/completions")

BASE_API_KEY = os.getenv("BASE_API_KEY", 'sk-MpFcAnO34r2gg5d1KA_QAg')
BASE_API_HEADERS = {'x-goog-api-key': os.getenv("BASE_API_KEY", 'sk-MpFcAnO34r2gg5d1KA_QAg')}