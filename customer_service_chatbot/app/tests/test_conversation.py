from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_conversation_flow():
    """Test basic conversation memory."""
    conversation_id = "test123"

    # Step 1: User asks about discounts
    response = client.post(
        f"/conversation/sales",
        json={"conversation_id": conversation_id, "user_input": "Do you have discounts?"}
    )
    assert response.status_code == 200
    json_data = response.json()
    assert "agent_response" in json_data

    # Step 2: User asks about order cancellation (should retain memory)
    response = client.post(
        f"/conversation/sales",
        json={"conversation_id": conversation_id, "user_input": "Can I cancel my order?"}
    )
    assert response.status_code == 200
    json_data = response.json()
    assert "agent_response" in json_data
    assert len(json_data["history"]) > 1  # ✅ Ensures conversation memory works