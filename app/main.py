# requestor/app/main.py

from fastapi import FastAPI, HTTPException, Header, Depends
from .models import NotificationRequest
from .sqs_client import send_message_to_queue
import logging
import sys
import boto3
import os
from typing import Optional

app = FastAPI()

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s"
)

# DynamoDB setup - assumes APPLICATIONS_TABLE env var is set
dynamodb = boto3.resource('dynamodb')
APPLICATIONS_TABLE = os.getenv('APPLICATIONS_TABLE', 'Applications')

def get_jwt_token(authorization: Optional[str] = Header(None)) -> Optional[str]:
    """Extract JWT token from Authorization header"""
    if not authorization:
        return None
    if not authorization.startswith('Bearer '):
        return None
    return authorization[7:]  # Remove 'Bearer ' prefix

def verify_jwt_in_dynamodb(token: str) -> bool:
    """Check if JWT token exists in DynamoDB applications table"""
    try:
        table = dynamodb.Table(APPLICATIONS_TABLE)
        # Query assuming 'jwt_token' is partition key or GSI attribute
        response = table.get_item(Key={'jwt_token': token})
        return 'Item' in response
    except Exception as e:
        logging.error(f"DynamoDB JWT check failed: {str(e)}")
        return False

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/request")
def notify(
    req: NotificationRequest,
    token: Optional[str] = Depends(get_jwt_token)
):
    # Check for JWT token in Authorization header
    if not token:
        raise HTTPException(
            status_code=401, 
            detail="JWT token required. Provide Authorization: Bearer <token> header."
        )
    
    # Verify token exists in DynamoDB
    if not verify_jwt_in_dynamodb(token):
        raise HTTPException(
            status_code=401, 
            detail="Invalid or missing JWT token in database."
        )
    
    try:
        response = send_message_to_queue(req.dict())
        logging.info(f"NotificationRequest payload: {response}")
        logging.info(f"NotificationRequest payload: {req.dict()}")
        return {
            "message_id": response.get("MessageId"),
            "status": "queued"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
 