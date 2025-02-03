from app.agents.base import BaseAgent
from app.services.llm_service import llm_service
from app.policies.enforcement.tech_support_policies import TechSupportPolicies

class TechSupportAgent(BaseAgent):
    """Handles tech support inquiries while enforcing authentication policies."""

    def __init__(self):
        super().__init__("tech_support")

    def handle_request(self, user_input: str, context: dict = None):
        """Processes tech support-related user requests with policy enforcement."""

        if not user_input.strip():
            return {"agent": self.name, "response": "I'm happy to assist! Could you clarify your technical issue?"}

        # 🔹 Enforce authentication before password resets
        if "reset my password" in user_input.lower() and TechSupportPolicies.requires_authentication(user_input):
            return {"agent": self.name, "response": "❌ Authentication is required before resetting a password. Please verify your identity first."}

        # ✅ Generate response using LLM service
        policy_context = context.get("policy", "No specific policies applied.")
        response_text = llm_service.generate_response(agent_type="tech_support", user_input=user_input, policy_context=policy_context)

        return {"agent": self.name, "response": response_text}