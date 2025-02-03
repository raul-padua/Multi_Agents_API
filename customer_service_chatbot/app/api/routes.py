from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.orm import Session
from app.agents.agent_factory import AgentFactory
from app.services.rag_service import RAGPolicyRetriever
from app.services.conversation_service import conversation_service
from app.models.database import SessionLocal 
from app.models.conversation import Conversation  
from typing import Optional

router = APIRouter()
rag_retriever = RAGPolicyRetriever()

# ✅ Request Models
class UserInput(BaseModel):
    conversation_id: str
    user_input: str

class PolicyQuery(BaseModel):
    query: str

# ✅ Dependency for Database Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/conversation/{agent_type}")
async def handle_conversation(agent_type: str, request_body: UserInput):
    """Routes user input to the appropriate agent and returns a structured response."""
    try:
        # ✅ Validate user input
        if not request_body.user_input.strip():
            raise HTTPException(status_code=400, detail="User input cannot be empty.")

        # ✅ Fetch correct agent & validate its existence
        try:
            agent = AgentFactory.get_agent(agent_type)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        # ✅ Retrieve last 5 messages from conversation history
        conversation_history = conversation_service.get_last_n_messages(request_body.conversation_id, n=5)

        # ✅ Format chat history into context
        history_context = "\n".join([f"{msg.sender}: {msg.content}" for msg in conversation_history]) if conversation_history else "No previous messages."

        # ✅ Retrieve relevant policies using RAG
        retrieved_policies = rag_retriever.retrieve_policy(request_body.user_input)
        policy_context = "\n".join(retrieved_policies) if retrieved_policies else "No relevant policy found."

        # ✅ Generate agent response (Handle OpenAI API failures)
        try:
            response_data = agent.handle_request(
                request_body.user_input, 
                context={"history": history_context, "policy": policy_context}
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Agent processing error: {str(e)}")

        # ✅ Ensure response is a string
        response_text = response_data.get("response", "No response provided.") if isinstance(response_data, dict) else str(response_data)

        # ✅ Store user message & bot response in conversation history
        conversation_service.add_message(request_body.conversation_id, "user", request_body.user_input, datetime.utcnow())
        conversation_service.add_message(request_body.conversation_id, "bot", response_text, datetime.utcnow())

        return {
            "conversation_id": request_body.conversation_id,
            "agent": agent_type,
            "agent_response": response_text,
            "retrieved_policies": retrieved_policies if retrieved_policies else ["No relevant policy found."],
            "history": conversation_service.get_last_n_messages(request_body.conversation_id, n=5)
        }

    except HTTPException:
        raise  # Re-raise handled FastAPI errors
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected Server Error: {str(e)}")

@router.post("/retrieve_policy")
async def retrieve_policy(request: PolicyQuery):
    """Retrieve the most relevant policy based on user query."""
    try:
        if not request.query.strip():
            raise HTTPException(status_code=400, detail="Policy query cannot be empty.")

        policies = rag_retriever.retrieve_policy(request.query)
        return {
            "query": request.query,
            "retrieved_policies": policies if policies else ["No relevant policy found."]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected Server Error: {str(e)}")

### 🔹 **New Endpoints Added Below**
@router.get("/conversation/latest")
async def get_latest_conversation(db: Session = Depends(get_db)):
    """Returns the latest full conversation."""
    latest_message = (
        db.query(Conversation.conversation_id)
        .order_by(Conversation.timestamp.desc())
        .first()
    )
    if not latest_message:
        return {"message": "No conversations found."}

    conversation_id = latest_message.conversation_id
    messages = (
        db.query(Conversation.sender, Conversation.content, Conversation.timestamp)
        .filter(Conversation.conversation_id == conversation_id)
        .order_by(Conversation.timestamp.asc())
        .all()
    )

    return {
        "conversation_id": conversation_id,
        "messages": [{"sender": msg[0], "content": msg[1], "timestamp": msg[2]} for msg in messages]
    }

@router.delete("/conversation/{conversation_id}")
async def delete_conversation(conversation_id: str, db: Session = Depends(get_db)):
    """Deletes all messages from a specific conversation."""
    deleted_rows = db.query(Conversation).filter(Conversation.conversation_id == conversation_id).delete()
    db.commit()
    if deleted_rows:
        return {"message": f"Conversation {conversation_id} deleted."}
    else:
        raise HTTPException(status_code=404, detail="Conversation not found.")

@router.get("/conversations/filter")
async def filter_conversations(agent_type: Optional[str] = Query(None), db: Session = Depends(get_db)):
    """Filters messages by agent type."""
    query = db.query(Conversation)

    if agent_type:
        query = query.filter(Conversation.sender == agent_type)

    messages = query.order_by(Conversation.timestamp.desc()).limit(10).all()

    return {"filtered_messages": [{"sender": msg.sender, "content": msg.content, "timestamp": msg.timestamp} for msg in messages]}