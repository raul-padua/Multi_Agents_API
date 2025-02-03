class CustomerSupportPolicies:
    """Strictly enforced business rules for customer support inquiries."""

    @staticmethod
    def can_cancel_order(order_status: str) -> bool:
        """
        Order can only be canceled if the item has NOT been shipped.
        """
        if order_status.lower() in ["shipped", "delivered"]:
            return False
        return True

    @staticmethod
    def can_track_order(order_number: str) -> bool:
        """
        Orders must have a valid order number format (e.g., ORD1234).
        """
        return order_number.startswith("ORD") and order_number[3:].isdigit()

    @staticmethod
    def requires_order_number(user_input: str) -> bool:
        """Checks if a refund request explicitly requires an order number."""
        refund_keywords = ["i want a refund", "can i return", "exchange my product", "request a refund"]
        # Ensure it's a **request**, not just a mention
        return any(phrase in user_input.lower() for phrase in refund_keywords)

    @staticmethod
    def is_request_appropriate(user_input: str) -> bool:
        """Checks if a customer request is appropriate (no offensive language)."""
        offensive_keywords = ["scam", "fraud", "stupid", "idiot"]
        return not any(keyword in user_input.lower() for keyword in offensive_keywords)