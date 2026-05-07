from dotenv import load_dotenv
import os

load_dotenv()

LOCAL = os.getenv("LOCAL", "False").lower() == "true"

# Keep DATABASE_URL as final usable URL
if LOCAL:
    DATABASE_URL = os.getenv("DATABASE_URL_EXTERNAL")  # external
else:
    DATABASE_URL = os.getenv("DATABASE_URL_INTERNAL")  # internal

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
REDIS_URL = os.getenv("REDIS_URL")
