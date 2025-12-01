"""Business rules definitions for the credit system"""


class Rule:
    """A single business rule in the system"""

    def __init__(self, name, condition, action, explanation_func, failure_message=None):
        """
        Args:
            name: Unique identifier for the rule
            condition: Function that takes context and returns bool
            action: Function that modifies context if condition is True
            explanation_func: Function that generates explanation text from context
            failure_message: Message if rule fails (static or function)
        """
        self.name = name
        self.condition = condition
        self.action = action
        self.explanation_func = explanation_func
        self.failure_message = failure_message

    def evaluate(self, context):
        """Evaluate this rule against the current context"""
        try:
            if self.condition(context):
                # Execute action
                self.action(context)
                # Generate explanation
                explanation = self.explanation_func(context)
                context['executed_rules'].append(self.name)
                context['explanations'].append(explanation)
                return True
            else:
                # Rule failed
                if self.failure_message:
                    if callable(self.failure_message):
                        msg = self.failure_message(context)
                    else:
                        msg = self.failure_message
                    context['rejection_reasons'].append(msg)
                return False
        except Exception as e:
            error_msg = f"Rule {self.name} error: {str(e)}"
            context['rejection_reasons'].append(error_msg)
            context['errors'].append(error_msg)
            return False

    @staticmethod
    def create_minimum_age_rule():
        """Rule 1: Minimum age requirement"""
        return Rule(
            name="minimum_age",
            condition=lambda ctx: ctx['age'] >= 18,
            action=lambda ctx: ctx.update({'eligible': True}),
            explanation_func=lambda ctx: f"Applicant age {ctx['age']} meets minimum requirement (18+)",
            failure_message=lambda ctx: f"Age {ctx['age']} below minimum requirement (18)"
        )

    @staticmethod
    def create_debt_to_income_rule():
        """Rule 2: Debt-to-income ratio"""
        return Rule(
            name="debt_to_income",
            condition=lambda ctx: ctx['monthly_income'] > 0 and
            (ctx['current_debt'] / ctx['monthly_income']) < 0.5,
            action=lambda ctx: ctx.update({'debt_ratio_ok': True}),
            explanation_func=lambda ctx: (
                f"Debt ratio acceptable: "
                f"${ctx['current_debt']:,.2f} / ${ctx['monthly_income']:,.2f} = "
                f"{(ctx['current_debt'] / ctx['monthly_income']):.1%}"
            ),
            failure_message=lambda ctx: (
                f"Debt ratio too high: "
                f"${ctx['current_debt']:,.2f} / ${ctx['monthly_income']:,.2f} = "
                f"{(ctx['current_debt'] / ctx['monthly_income']):.1%} (max 50%)"
            )
        )

    @staticmethod
    def create_credit_score_rule():
        """Rule 3: Minimum credit score"""
        return Rule(
            name="minimum_credit_score",
            condition=lambda ctx: ctx['credit_score'] >= 600,
            action=lambda ctx: ctx.update({'credit_score_ok': True}),
            explanation_func=lambda ctx: f"Credit score {ctx['credit_score']} meets minimum (600+)",
            failure_message=lambda ctx: f"Credit score {ctx['credit_score']} below minimum (600)"
        )

    @staticmethod
    def create_employment_rule():
        """Rule 4: Employment stability"""
        return Rule(
            name="employment_stability",
            condition=lambda ctx: ctx['stable_employment'],
            action=lambda ctx: ctx.update({'employment_ok': True}),
            explanation_func=lambda ctx: "Stable employment confirmed (>2 years)",
            failure_message="Employment history insufficient (<2 years or unstable)"
        )

    @staticmethod
    def create_interest_rate_rule():
        """Rule 5: Calculate interest rate"""
        def calculate_interest(context):
            """Calculate interest rate based on risk factors"""
            base_rate = 8.0

            if context['credit_score'] >= 750:
                base_rate -= 2.5
            elif context['credit_score'] >= 650:
                base_rate -= 1.0

            if context['stable_employment']:
                base_rate -= 0.5

            debt_ratio = context['current_debt'] / context['monthly_income']
            if debt_ratio < 0.3:
                base_rate -= 0.5

            context['interest_rate'] = max(5.0, base_rate)
            context['monthly_payment'] = calculate_monthly_payment(
                context['loan_amount'],
                context['interest_rate'],
                context['loan_term']
            )

        def calculate_monthly_payment(principal, annual_rate, months):
            """Calculate monthly payment using amortization formula"""
            monthly_rate = annual_rate / 100 / 12
            if monthly_rate == 0:
                return principal / months

            return principal * (monthly_rate * (1 + monthly_rate) ** months) / ((1 + monthly_rate) ** months - 1)

        return Rule(
            name="calculate_interest_rate",
            condition=lambda ctx: ctx.get('approved', False),
            action=calculate_interest,
            explanation_func=lambda ctx: (
                f"Interest rate calculated: {ctx.get('interest_rate', 0):.2f}% APR, "
                f"monthly payment: ${ctx.get('monthly_payment', 0):,.2f}"
            ),
            failure_message=None
        )
