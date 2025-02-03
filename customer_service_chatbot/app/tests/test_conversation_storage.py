import pytest
from sqlalchemy import text
from app.models.database import SessionLocal
from app.services.conversation_service import conversation_service
from datetime import datetime

@pytest.fixture(scope="function")
def db_session():
    """Ensures each test starts with a clean database session."""
    session = SessionLocal()
    yield session  # Provide session for the test
    session.rollback()
    session.close()

def test_store_message(db_session):
    """Test storing a message in the database."""
    conversation_service.add_message("test_convo_1", "user", "Hello, world!", datetime.utcnow())

    db_session.commit()

    result = db_session.execute(text("SELECT * FROM conversations WHERE conversation_id='test_convo_1'")).fetchall()
    
    assert len(result) == 1, f"❌ Expected 1 message, but found {len(result)}"
    assert result[0][2] == "user"
    assert result[0][3] == "Hello, world!"

def test_database_persistence(db_session):
    """Test if messages persist after session is closed and reopened."""
    conversation_service.add_message("test_convo_3", "user", "Persistent message", datetime.utcnow())

    db_session.commit()

    new_session = SessionLocal()
    result = new_session.execute(text("SELECT * FROM conversations WHERE conversation_id='test_convo_3'")).fetchall()
    new_session.close()

    assert len(result) == 1, f"❌ Expected 1 message, but found {len(result)}"
    assert result[0][3] == "Persistent message"

def test_store_empty_message(db_session):
    """Test if empty messages are stored."""
    conversation_service.add_message("test_convo_4", "user", "", datetime.utcnow())

    db_session.commit()

    result = db_session.execute(text("SELECT * FROM conversations WHERE conversation_id='test_convo_4'")).fetchall()

    assert len(result) == 1, f"❌ Expected 1 message, but found {len(result)}"
    assert result[0][3] == ""