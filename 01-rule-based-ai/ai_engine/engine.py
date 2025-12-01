from .rules import Rule


class CreditRulesEngine:
    """Forward-chaining rule engine for credit decisions"""

    def __init__(self):
        self.rules = []
        self._load_rules()

    def _load_rules(self):
        """Load all business rules - this is our 'AI knowledge base'"""
        self.rules = [
            Rule.create_minimum_age_rule(),
            Rule.create_debt_to_income_rule(),
            Rule.create_credit_score_rule(),
            Rule.create_employment_rule(),
            Rule.create_interest_rate_rule()
        ]

    def evaluate_application(self, application_data):
        """
        Main inference method: evaluates credit application using all rules
        Returns: Decision with full explanation
        """
        # Initialize evaluation context with default values
        context = {
            **application_data,
            'executed_rules': [],
            'rejection_reasons': [],
            'explanations': [],
            'errors': [],
            'approved': False,
            'final_decision': "REJECTED",
            'interest_rate': 0.0,      # Default value
            'monthly_payment': 0.0,    # Default value
            'decision_explanation': ""
        }

        for rule in self.rules:
            rule.evaluate(context)

        required_rules = ['minimum_age',
                          'debt_to_income', 'minimum_credit_score']
        required_passed = all(
            r in context['executed_rules'] for r in required_rules)

        if len(context['executed_rules']) >= 3 and required_passed:
            context['approved'] = True
            context['final_decision'] = "APPROVED"
            context['decision_explanation'] = "Application meets all key requirements"
        else:
            context['decision_explanation'] = "Application does not meet minimum requirements"

        if not context['rejection_reasons']:
            context.pop('rejection_reasons', None)
        if not context['errors']:
            context.pop('errors', None)

        return context

    def get_rules_info(self):
        """Get information about all loaded rules"""
        return [
            {
                'name': rule.name,
                'description': rule.explanation_func({'dummy': 'data'}) if hasattr(rule.explanation_func, '__call__') else str(rule.explanation_func)
            }
            for rule in self.rules
        ]
