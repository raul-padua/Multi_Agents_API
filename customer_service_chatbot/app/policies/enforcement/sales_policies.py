class SalesPolicies:
    """Strictly enforced business rules for sales inquiries."""
    UNAVAILABLE_PRODUCTS = {"Limited Edition Sneakers", "Rare Collectible Watch"}

    @staticmethod
    def is_product_available(product_name: str) -> bool:
        """Returns False if the product is in the unavailable list."""
        return product_name not in SalesPolicies.UNAVAILABLE_PRODUCTS

    @staticmethod
    def can_create_order(product_name: str, quantity: int) -> bool:
        """
        Orders must be for at least 1 unit and not exceed max stock (e.g., 10).
        """
        return SalesPolicies.is_product_available(product_name) and (1 <= quantity <= 10)

    @staticmethod
    def is_product_available(product_name: str) -> bool:
        """Returns False if the product is in the unavailable list."""
        return product_name not in SalesPolicies.UNAVAILABLE_PRODUCTS

    @staticmethod
    def can_create_order(product_name: str, quantity: int) -> bool:
        """Checks if the order quantity is valid."""
        max_order_limit = 10  # Example threshold
        return SalesPolicies.is_product_available(product_name) and quantity <= max_order_limit