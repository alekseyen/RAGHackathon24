import os
from dotenv import load_dotenv

load_dotenv("../../.env")

API_TOKEN = os.getenv("API_YANDEX_CLOUD_TOKEN")
CATALOG_NUMBER = os.getenv("CATALOG_NUMBER")
CUSTOM_MODEL_YRL = "gpt://{CATALOG_NUMBER}/yandexgpt/latest"
