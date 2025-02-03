from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import config

Base = declarative_base()
engine = create_engine(config.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ Ensure DB Initialization at Startup
def init_db():
    """Creates all database tables if they don’t exist."""
    from app.models.conversation import Conversation  # Import models before creation
    Base.metadata.create_all(bind=engine)