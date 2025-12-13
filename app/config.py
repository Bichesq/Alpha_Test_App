import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
    SQS_QUEUE_URL = os.getenv("SQS_QUEUE_URL")

settings = Settings()
