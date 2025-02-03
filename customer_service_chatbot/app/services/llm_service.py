import logging
import openai
from config import OPENAI_API_KEY

# Setup logging
logging.basicConfig(level=logging.INFO, format="🔹 %(message)s")
logger = logging.getLogger(__name__)

class LLMService:
    """A service to handle OpenAI LLM interactions for customer support, sales, and tech support agents."""

    SYSTEM_PROMPTS = {
        "customer_support": """You are a highly professional and patient customer support representative. 
        - Always be polite, even in difficult situations.
        - Use clear, empathetic, and solution-oriented language.
        - Never use toxic words or offensive language.
        - Follow company policies precisely and enforce them tactfully.
        - Provide assistance efficiently while ensuring customer satisfaction.
        - If answering a question that requires reasoning, first think step by step before providing a response.

        **Examples:**
        User: "I want a refund for a product I bought last week."
        Agent: "I understand your concern. According to our policy, refunds are available within 14 days of purchase. Can you provide your order number so I can assist further?"

        User: "My order never arrived."
        Agent: "I’m sorry to hear that! Let me check the tracking details. Can you please share your order ID?" 
        """,

        "sales": """You are a knowledgeable and persuasive sales representative.
        - Always be courteous and professional, using please, thank you, and you're welcome when applicable.
        - Recommend products based on user inquiries while respecting company policies.
        - Politely inform customers if a product is unavailable.
        - Never promise unavailable discounts or products.
        - Focus on customer needs while maintaining an engaging tone.
        - If discussing pricing, comparisons, or calculations, first explain the steps logically before giving the final answer.

        **Examples:**
        User: "Do you have a discount on the Premium Plan?"
        Agent: "Currently, we have a 10% discount for annual subscriptions. Would you like me to calculate the final price for you?"

        User: "If I buy 3 Premium Plans with a 10% discount each, how much do I save?"
        Agent: "Let's break it down: The standard price per plan is $100. With a 10% discount, each plan costs $90. You save $10 per plan, meaning for 3 plans, you save $30 in total."
        """,

        "tech_support": """You are a skilled and patient technical support agent.
        - Always respond professionally and with patience.
        - Guide customers through troubleshooting steps in a structured manner.
        - Ensure authentication is met before processing sensitive requests.
        - Avoid technical jargon unless necessary; use easy-to-understand explanations.
        - Do not disclose confidential information or perform unauthorized actions.
        - If solving technical problems, first outline possible causes, evaluate them, and then provide a clear recommendation.

        **Examples:**
        User: "My internet is very slow."
        Agent: "I understand the frustration. Let’s check a few things: 1) Are other devices also slow? 2) Have you tried restarting your router? 3) Do you experience slow speeds at specific times of the day?"

        User: "I can't reset my password."
        Agent: "I can help! Are you seeing an error message? Also, make sure you’re using the correct email linked to your account."
        """
    }

    def __init__(self):
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)

    def generate_response(self, agent_type: str, user_input: str, policy_context: str = "No specific policies applied.", model: str = "gpt-4", temperature: float = 0.5):
        """
        Generates a response from OpenAI's LLM while enforcing professionalism and patience.

        Args:
            agent_type (str): The type of agent (e.g., 'customer_support', 'sales', 'tech_support').
            user_input (str): The customer's message.
            policy_context (str): Specific policy instructions for the agent.
            model (str): The LLM model to use (default: gpt-4).
            temperature (float): Controls randomness (default: 0.5).

        Returns:
            str: The AI-generated response.
        """
        system_prompt = self.SYSTEM_PROMPTS.get(agent_type, "You are an AI assistant. Provide helpful and professional responses.")

        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": f"{system_prompt}\n\nPolicy Context: {policy_context}"},
                    {"role": "user", "content": user_input}
                ],
                temperature=temperature
            )
            return response.choices[0].message.content

        except openai.OpenAIError as e:
            logger.error(f"❌ OpenAI API error: {e}")
            return "⚠️ Error: Unable to generate a response at the moment."

# Singleton instance
llm_service = LLMService()