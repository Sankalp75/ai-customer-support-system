
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.schemas import ChatRequest, ChatResponse, AIResponse
from services.chat_orchestrator import chat_orchestrator
from storage.database import get_db
from storage.models import ChannelEnum

router = APIRouter()

@router.post("/chat/web", response_model=ChatResponse)
async def chat_with_bot(
    chat_request: ChatRequest, db: Session = Depends(get_db)
):
    """
    Endpoint for the website chatbot.
    """
    # Process the message using the chat orchestrator
    orchestrator_response = chat_orchestrator.process_message(
        db=db,
        session_id=chat_request.session_id,
        message_text=chat_request.message.content,
        channel=ChannelEnum.WEB,
    )

    # Create the AI response
    ai_response = AIResponse(
        response_text=orchestrator_response.get("answer"),
        # We will add confidence scoring later
        confidence_score=None,
    )
    
    # Create the full chat response
    response = ChatResponse(
        ai_response=ai_response,
        is_escalated=orchestrator_response.get("is_escalated"),
        escalation_message=orchestrator_response.get("escalation_message"),
        session_id=chat_request.session_id,
    )

    return response
