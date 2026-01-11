
import logging
import smtplib
from email.mime.text import MIMEText
from core.config import settings

logger = logging.getLogger(__name__)

class EscalationManager:
    """
    Manages the logic for escalating a conversation to a human agent.
    """

    def __init__(self):
        self.escalation_keywords = [
            "human",
            "agent",
            "person",
            "representative",
            "talk to someone",
            "speak to someone",
        ]

    def check_for_escalation(self, message_text: str) -> bool:
        """
        Checks if a user's message triggers an escalation.
        
        For now, this is a simple keyword match.
        """
        lower_message = message_text.lower()
        for keyword in self.escalation_keywords:
            if keyword in lower_message:
                logger.info(f"Escalation triggered by keyword: '{keyword}'")
                return True
        return False

    def send_escalation_notification(self, session_id: str, message_text: str):
        """
        Sends an email notification to the human agent.
        """
        subject = f"Human Escalation Request - Session: {session_id}"
        body = f"""
        A user has requested to speak with a human agent.

        Session ID: {session_id}
        Triggering Message: "{message_text}"

        Please follow up with the user in the appropriate channel.
        """
        
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = settings.SMTP_USERNAME
        msg['To'] = settings.NOTIFICATION_EMAIL_TO

        try:
            with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
                server.starttls()
                server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
                server.send_message(msg)
                logger.info(f"Escalation email sent to {settings.NOTIFICATION_EMAIL_TO}")
        except Exception as e:
            logger.error(f"Failed to send escalation email: {e}")


# A single instance of the escalation manager
escalation_manager = EscalationManager()
