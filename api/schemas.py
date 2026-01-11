
from pydantic import BaseModel, Field
from typing import Optional


class ChatMessageCreate(BaseModel):
    """
    Schema for a user's incoming message.
    """
    content: str = Field(..., example="What are your business hours?")


class ChatRequest(BaseModel):
    """
    Schema for a chat request from any channel.
    """
    session_id: str = Field(..., example="user123_session456")
    message: ChatMessageCreate


class AIResponse(BaseModel):
    """
    Schema for the AI's response content.
    """
    response_text: str = Field(..., example="Our business hours are 9 AM to 5 PM, Monday to Friday.")
    confidence_score: Optional[float] = Field(None, example=0.95)
    
class ChatResponse(BaseModel):
    """
    Full response payload sent back to the client.
    """
    ai_response: AIResponse
    is_escalated: bool = Field(False, example=False)
    escalation_message: Optional[str] = Field(None, example="I am connecting you to a human agent.")
    session_id: str = Field(..., example="user123_session456")

