from app.agents.base import BaseAgent
from app.services.llm_service import llm_service
from app.policies.enforcement.customer_support_policies import CustomerSupportPolicies

class CustomerSupportAgent(BaseAgent):
    """Handles customer support requests while enforcing policies."""

    def __init__(self):
        super().__init__("customer_support")

    def handle_request(self, user_input: str, context: dict = None):
        """Processes customer support requests while enforcing policies."""

        if not user_input.strip():
            return {"agent": self.name, "response": "I'm here to assist! Could you provide more details?"}

        # 🔹 Enforce policy for order cancellation
        if "cancel order" in user_input.lower():
            order_status = "shipped"  # Mock example
            if not CustomerSupportPolicies.can_cancel_order(order_status):
                return {"agent": self.name, "response": "❌ Your order has already been shipped and cannot be canceled."}

        # 🔹 Enforce policy for order tracking
        if "track order" in user_input.lower():
            order_number = "ORD123"  # Mock input
            if not CustomerSupportPolicies.can_track_order(order_number):
                return {"agent": self.name, "response": "❌ Invalid order number format. Please check and try again."}

        # ✅ Use retrieved policies in LLM response
        policy_context = context.get("policy", "No specific policies applied.")
        response_text = llm_service.generate_response(agent_type="customer_support", user_input=user_input, policy_context=policy_context)

        return {"agent": self.name, "response": response_text}