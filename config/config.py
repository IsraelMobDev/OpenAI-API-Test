from dotenv import load_dotenv
import os

load_dotenv()
token_todo = os.getenv("TOKEN")
URL_TODO = "https://api.openai.com/v1/"
HEADERS_TODO = {
    "Authorization": f"Bearer {token_todo}",
    "OpenAI-Beta": "assistants=v1"
}