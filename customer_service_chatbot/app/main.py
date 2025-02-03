from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.api.routes import router
from app.models.database import SessionLocal, init_db  # ✅ Import init_db
from app.models.conversation import Conversation

app = FastAPI(
    title="Customer Service Chatbot API",
    description="API for handling customer service requests with specialized agents.",
    version="1.0.0"
)

# ✅ Initialize Database on Startup
@app.on_event("startup")
def startup_event():
    """Ensure the database tables are created before the app starts."""
    init_db()

app.include_router(router)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", tags=["Conversations"])
async def root(db: Session = Depends(get_db)):
    """Returns the 5 latest conversations with messages."""

    # ✅ Fetch latest 5 distinct conversations
    latest_conversation_ids = (
        db.query(Conversation.conversation_id)
        .distinct(Conversation.conversation_id)
        .order_by(Conversation.conversation_id, desc(Conversation.timestamp))
        .limit(5)
        .all()
    )

    conversation_ids = [row[0] for row in latest_conversation_ids]

    # ✅ Fetch all messages for these conversations
    conversations = []
    for conversation_id in conversation_ids:
        messages = (
            db.query(Conversation.sender, Conversation.content, Conversation.timestamp)
            .filter(Conversation.conversation_id == conversation_id)
            .order_by(Conversation.timestamp.asc())  # Chronological order
            .all()
        )

        conversations.append({
            "conversation_id": conversation_id,
            "latest_timestamp": messages[-1][2] if messages else None,
            "messages": [{"sender": msg[0], "content": msg[1], "timestamp": msg[2]} for msg in messages]
        })

    # ✅ Sort conversations by latest message timestamp (descending)
    sorted_conversations = sorted(conversations, key=lambda x: x["latest_timestamp"], reverse=True)

    return {"latest_conversations": sorted_conversations}