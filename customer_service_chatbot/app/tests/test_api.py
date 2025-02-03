from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_sales_agent():
    """Test Sales Agent API"""
    response = client.post(
        "/conversation/sales",
        json={
            "conversation_id": "test_sales_123",  # ✅ Include conversation_id
            "user_input": "What are the latest product deals?"
        }
    )
    assert response.status_code == 200
    assert "agent" in response.json()
    assert response.json()["agent"] == "sales"
    assert "agent_response" in response.json()

def test_tech_support_agent():
    """Test Tech Support Agent API"""
    response = client.post(
        "/conversation/tech_support",
        json={
            "conversation_id": "test_tech_123",  # ✅ Include conversation_id
            "user_input": "How do I reset my password?"
        }
    )
    assert response.status_code == 200
    assert "agent" in response.json()
    assert response.json()["agent"] == "tech_support"
    assert "agent_response" in response.json()

def test_customer_support_agent():
    """Test Customer Support Agent API"""
    response = client.post(
        "/conversation/customer_support",
        json={
            "conversation_id": "test_cust_123",  # ✅ Include conversation_id
            "user_input": "Where is my order?"
        }
    )
    assert response.status_code == 200
    assert "agent" in response.json()
    assert response.json()["agent"] == "customer_support"
    assert "agent_response" in response.json()