
from sqlalchemy.orm import Session
from rag.retrieval import RAGChain
from storage.models import Conversation, Message, ChannelEnum, SenderEnum
from services.escalation_manager import escalation_manager

class ChatOrchestrator:
    """
    Orchestrates the chat flow, including RAG retrieval, history, and escalation.
    """

    def __init__(self):
        self.rag_chain = RAGChain()

    def _get_or_create_conversation(self, db: Session, session_id: str, channel: ChannelEnum) -> Conversation:
        """
        Retrieves a conversation from the database or creates it if it doesn't exist.
        """
        conversation = db.query(Conversation).filter(Conversation.session_id == session_id).first()
        if not conversation:
            conversation = Conversation(session_id=session_id, channel=channel)
            db.add(conversation)
            db.commit()
            db.refresh(conversation)
        return conversation

    def process_message(self, db: Session, session_id: str, message_text: str, channel: ChannelEnum):
        """
        Process a user's message, log it, check for escalation, get an AI response, and log that too.
        """
        conversation = self._get_or_create_conversation(db, session_id, channel)

        # Log the user's message
        user_message = Message(
            conversation_id=conversation.id,
            sender=SenderEnum.USER,
            content=message_text,
        )
        db.add(user_message)
        db.commit()

        # Check if conversation is already escalated
        if conversation.is_escalated:
            return {
                "answer": "You are already in the queue to speak with a human agent. Please be patient.",
                "is_escalated": True,
                "escalation_message": "You are already in the queue to speak with a human agent. Please be patient.",
            }

        # Check for escalation triggers
        if escalation_manager.check_for_escalation(message_text):
            conversation.is_escalated = True
            db.commit()
            
            # Trigger notification to human agents
            escalation_manager.send_escalation_notification(session_id, message_text)
            
            escalation_message = "I understand you'd like to speak with a human. I have escalated your request and an agent will be with you shortly."
            return {
                "answer": escalation_message,
                "is_escalated": True,
                "escalation_message": escalation_message,
            }

        # If no escalation, get AI response
        rag_response = self.rag_chain.invoke(message_text)
        ai_answer = rag_response.get("answer")

        # Log the AI's message
        ai_message = Message(
            conversation_id=conversation.id,
            sender=SenderEnum.AI,
            content=ai_answer,
            confidence_score=None, # TODO: Add confidence scoring
        )
        db.add(ai_message)
        db.commit()

        return {
            "answer": ai_answer,
            "is_escalated": False,
            "escalation_message": None,
        }

# A single instance of the orchestrator to be used by the API routers
chat_orchestrator = ChatOrchestrator()
