from .rules import Rule


class CreditRulesEngine:
    """Forward-chaining rule engine for credit decisions"""

    # Rules that MUST pass for approval
    REQUIRED_RULES = ['minimum_age', 'debt_to_income', 'minimum_credit_score']

    def __init__(self):
        self.rules = []
        self._load_rules()

    def _load_rules(self):
        """Load all business rules - this is our 'AI knowledge base'"""
        # Note: interest rate rule is handled separately after approval decision
        self.rules = [
            Rule.create_minimum_age_rule(),
            Rule.create_debt_to_income_rule(),
            Rule.create_credit_score_rule(),
            Rule.create_employment_rule(),
        ]
        self.interest_rate_rule = Rule.create_interest_rate_rule()

    def evaluate_application(self, application_data):
        """
        Main inference method: evaluates credit application using all rules.

        Process:
          1. Run sequential rules (age, DTI, credit score, employment)
          2. Determine approval based on required rules
          3. If approved, run interest rate calculation (needs approved=True in context)

        Returns: Decision context dict with full explanation
        """
        context = {
            **application_data,
            'executed_rules': [],
            'rejection_reasons': [],
            'explanations': [],
            'errors': [],
            'approved': False,
            'final_decision': "REJECTED",
            'interest_rate': 0.0,
            'monthly_payment': 0.0,
            'decision_explanation': "",
        }

        # --- Phase 1: Evaluate sequential business rules ---
        for rule in self.rules:
            rule.evaluate(context)

        # --- Phase 2: Determine approval ---
        required_passed = all(
            r in context['executed_rules'] for r in self.REQUIRED_RULES
        )

        if required_passed:
            context['approved'] = True
            context['final_decision'] = "APPROVED"
            context['decision_explanation'] = "Application meets all key requirements"
        else:
            context['decision_explanation'] = "Application does not meet minimum requirements"

        # --- Phase 3: Calculate interest rate only if approved ---
        # This must run AFTER approved is set to True in the context,
        # because the rule's condition checks ctx['approved'].
        if context['approved']:
            self.interest_rate_rule.evaluate(context)

        return context

    def get_rules_info(self):
        """Get static descriptions of all loaded rules (safe, no context needed)"""
        all_rules = self.rules + [self.interest_rate_rule]
        return [
            {
                'name': rule.name,
                'description': rule.description,
            }
            for rule in all_rules
        ]