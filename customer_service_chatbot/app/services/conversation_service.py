import logging
from sqlalchemy.orm import Session
from app.models.database import SessionLocal
from app.models.conversation import Conversation
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO, format="🔹 %(message)s")
logger = logging.getLogger(__name__)

class ConversationService:
    """Service for managing conversations in the database."""

    def __init__(self, session: Session = None):
        self.session = session or SessionLocal()

    def add_message(self, conversation_id: str, sender: str, content: str, timestamp: datetime):
        """Stores a new message in the database."""
        try:
            logger.info(f"🟢 Storing message -> [{sender}]: {content}")
            new_message = Conversation(
                conversation_id=conversation_id,
                sender=sender,
                content=content,
                timestamp=timestamp
            )
            self.session.add(new_message)
            self.session.commit()
            self.session.refresh(new_message)
            logger.info(f"✅ Stored message successfully: {new_message.content}")
        except Exception as e:
            self.session.rollback()
            logger.error(f"❌ ERROR: Failed to store message: {e}")
        finally:
            self.session.close()

    def get_last_n_messages(self, conversation_id: str, n: int = 5):
        """Retrieves the last N messages from a conversation."""
        try:
            messages = (
                self.session.query(Conversation)
                .filter(Conversation.conversation_id == conversation_id)
                .order_by(Conversation.timestamp.desc())
                .limit(n)
                .all()
            )
            logger.info(f"🟡 Retrieved {len(messages)} messages from history")
            return messages[::-1]  # Return messages in chronological order
        except Exception as e:
            logger.error(f"❌ ERROR: Failed to retrieve messages: {e}")
            return []
        finally:
            self.session.close()

conversation_service = ConversationService()