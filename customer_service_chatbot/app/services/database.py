import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from app.models.database import Base, Conversation
from config import DATABASE_URL

# Setup logging
logging.basicConfig(level=logging.INFO, format="🔹 %(message)s")
logger = logging.getLogger(__name__)

# Initialize Database Connection
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 🚀 Ensure all tables exist in the container
Base.metadata.create_all(bind=engine)

def store_message(conversation_id: str, sender: str, content: str, timestamp: str):
    """Stores a message in the database and logs it in real-time."""
    session = SessionLocal()
    try:
        message = Conversation(
            conversation_id=conversation_id,
            sender=sender,
            content=content,
            timestamp=timestamp
        )
        session.add(message)
        session.commit()
        session.refresh(message)

        logger.info(f"[{message.timestamp}] {message.sender} (Convo {message.conversation_id}): {message.content}")
    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"❌ Error storing message: {e}")
    finally:
        session.close()