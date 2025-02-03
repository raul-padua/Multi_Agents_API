from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, func, create_engine
from app.models.database import Base, engine

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, autoincrement=True)  
    conversation_id = Column(String(255), nullable=False, index=True) 
    sender = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(TIMESTAMP, default=func.now(), nullable=False)

# ✅ Initialize DB here as this is where `Conversation` is defined)
def init_db():
    Base.metadata.create_all(bind=engine)