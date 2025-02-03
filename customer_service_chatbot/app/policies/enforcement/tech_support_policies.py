class TechSupportPolicies:
    """Strictly enforced business rules for technical support inquiries."""

    @staticmethod
    def is_valid_email(email: str) -> bool:
        """
        Validate email format.
        """
        return "@" in email and "." in email.split("@")[-1]

    @staticmethod
    def can_schedule_technician(issue_type: str) -> bool:
        """
        Only allow scheduling for predefined issue types.
        """
        allowed_issues = {"internet installation", "router issue", "slow speed"}
        return issue_type.lower() in allowed_issues

    @staticmethod
    def requires_authentication(user_input: str) -> bool:
        """Checks if an authentication step is required for a tech support request."""
        sensitive_requests = ["reset my password", "change my email", "account recovery"]
        return any(keyword in user_input.lower() for keyword in sensitive_requests)