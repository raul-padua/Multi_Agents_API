from app.agents.sales_agent import SalesAgent
from app.agents.tech_support_agent import TechSupportAgent
from app.agents.customer_support_agent import CustomerSupportAgent

class AgentFactory:
    """Factory class to create appropriate agent instances."""

    AGENT_MAPPING = {
        "sales": SalesAgent,
        "tech_support": TechSupportAgent,
        "customer_support": CustomerSupportAgent
    }

    @staticmethod
    def get_agent(agent_type: str):
        """Returns an agent instance based on the given type."""
        normalized_type = agent_type.lower().replace(" ", "_")
        agent_class = AgentFactory.AGENT_MAPPING.get(normalized_type)
        
        if not agent_class:
            raise ValueError(f"Unknown agent type: {agent_type}. Valid types: {list(AgentFactory.AGENT_MAPPING.keys())}")
        
        return agent_class()