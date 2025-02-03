from fastapi.testclient import TestClient
from app.main import app
from app.policies.enforcement.customer_support_policies import CustomerSupportPolicies
from app.policies.enforcement.sales_policies import SalesPolicies
from app.policies.enforcement.tech_support_policies import TechSupportPolicies

client = TestClient(app)

# 🟢 **Customer Support Policy Tests**
def test_customer_support_refund_requires_order():
    """Customer Support: Refund requests must include an order number."""
    assert CustomerSupportPolicies.requires_order_number("I want a refund") == True
    assert CustomerSupportPolicies.requires_order_number("Can I return my item?") == True
    assert CustomerSupportPolicies.requires_order_number("Just asking about refunds") == False

def test_customer_support_no_inappropriate_requests():
    """Customer Support: Rejects inappropriate or offensive messages."""
    assert CustomerSupportPolicies.is_request_appropriate("You're all scammers!") == False
    assert CustomerSupportPolicies.is_request_appropriate("I'd like help with my order") == True

# 🟢 **Sales Policy Tests**
def test_sales_product_availability():
    """Sales: Prevents purchase of unavailable products."""
    assert SalesPolicies.is_product_available("Premium Plan") == True  # Assuming it's available
    assert SalesPolicies.is_product_available("Limited Edition Sneakers") == False  # Assuming it's out of stock

def test_sales_order_restrictions():
    """Sales: Restricts invalid order quantities."""
    assert SalesPolicies.can_create_order("Premium Plan", 2) == True  # Allowed quantity
    assert SalesPolicies.can_create_order("Premium Plan", 500) == False  # Exceeds stock limit

# 🟢 **Tech Support Policy Tests**
def test_tech_support_requires_authentication():
    """Tech Support: Enforces authentication before password resets."""
    assert TechSupportPolicies.requires_authentication("I need to reset my password") == True
    assert TechSupportPolicies.requires_authentication("How do I change my email?") == True
    assert TechSupportPolicies.requires_authentication("My internet is slow") == False  # General tech issue

# 🟢 **API Integration Tests**
def test_policy_enforcement_in_api():
    """Tests API to ensure policy enforcement works end-to-end."""
    response = client.post(
        "/conversation/sales",
        json={"conversation_id": "test_enforcement_001", "user_input": "I want to buy Limited Edition Sneakers."}
    )
    assert response.status_code == 200
    assert "❌" in response.json()["agent_response"]  # Should indicate product unavailability

    response = client.post(
        "/conversation/tech_support",
        json={"conversation_id": "test_enforcement_002", "user_input": "Can you reset my password?"}
    )
    assert response.status_code == 200
    assert "❌" in response.json()["agent_response"]  # Should enforce authentication