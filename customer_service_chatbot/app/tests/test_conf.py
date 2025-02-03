import pytest
from sqlalchemy import text
from app.models.database import SessionLocal, init_db

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Initialize the database before running all tests."""
    init_db()

@pytest.fixture(scope="function")
def db_session():
    """Creates a fresh DB session for each test and clears the database."""
    session = SessionLocal()
    
    # ✅ Force delete all records before each test
    session.execute(text("TRUNCATE conversations RESTART IDENTITY CASCADE;"))  
    session.commit()
    
    yield session  # Provide session for the test
    session.rollback()
    session.close()