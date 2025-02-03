import re
from app.agents.base import BaseAgent
from app.services.llm_service import llm_service
from app.policies.enforcement.sales_policies import SalesPolicies

class SalesAgent(BaseAgent):
    """Handles sales inquiries while enforcing policies."""

    def __init__(self):
        super().__init__("sales")

    def extract_product_name(self, user_input: str) -> str:
        """Extracts product name dynamically based on predefined keywords."""
        product_keywords = {"Limited Edition Sneakers", "Premium Plan", "Rare Collectible Watch"}

        for product in product_keywords:
            if re.search(rf"\b{re.escape(product.lower())}\b", user_input.lower()):
                return product

        return "Unknown Product"

    def extract_quantity(self, user_input: str) -> int:
        """Extracts quantity from user input using regex. Defaults to 1 if none is found."""
        match = re.search(r"\b(\d+)\b", user_input)
        return int(match.group(1)) if match else 1  # Default to 1 if no number is detected

    def handle_request(self, user_input: str, context: dict = None):
        """Processes sales-related user requests with policy enforcement."""

        if not user_input.strip():
            return {"agent": self.name, "response": "I'm happy to assist! Could you clarify what product you're interested in?"}

        # 🔹 Extract product name & quantity
        product_name = self.extract_product_name(user_input)
        quantity = self.extract_quantity(user_input)

        # 🔹 Enforce product availability
        if product_name != "Unknown Product" and not SalesPolicies.is_product_available(product_name):
            return {"agent": self.name, "response": f"❌ {product_name} is currently unavailable."}

        # 🔹 Validate order creation
        if "order" in user_input.lower() and not SalesPolicies.can_create_order(product_name, quantity):
            return {"agent": self.name, "response": "❌ Cannot place this order. Ensure quantity is valid and product is in stock."}

        # ✅ Generate response using LLM service
        policy_context = context.get("policy", "No specific policies applied.")
        response_text = llm_service.generate_response(agent_type="sales", user_input=user_input, policy_context=policy_context)

        return {"agent": self.name, "response": response_text}