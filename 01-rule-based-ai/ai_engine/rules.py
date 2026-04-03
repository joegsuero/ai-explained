"""Business rules definitions for the credit system"""


class Rule:
    """A single business rule in the system"""

    def __init__(self, name, condition, action, explanation_func,
                 failure_message=None, description=""):
        """
        Args:
            name:             Unique identifier for the rule
            condition:        Function(context) -> bool; determines if rule fires
            action:           Function(context) -> None; modifies context when rule fires
            explanation_func: Function(context) -> str; generates human-readable explanation
            failure_message:  str or Function(context) -> str; message when rule fails
            description:      Static human-readable description (used in rules info API)
        """
        self.name = name
        self.condition = condition
        self.action = action
        self.explanation_func = explanation_func
        self.failure_message = failure_message
        self.description = description

    def evaluate(self, context):
        """
        Evaluate this rule against the current context.

        Returns True if the rule fired (condition matched), False otherwise.
        All results — explanations and rejection reasons — are written into context.
        """
        try:
            if self.condition(context):
                self.action(context)
                explanation = self.explanation_func(context)
                context['executed_rules'].append(self.name)
                context['explanations'].append(explanation)
                return True
            else:
                if self.failure_message:
                    msg = (
                        self.failure_message(context)
                        if callable(self.failure_message)
                        else self.failure_message
                    )
                    context['rejection_reasons'].append(msg)
                return False
        except Exception as e:
            error_msg = f"Rule '{self.name}' error: {str(e)}"
            context['rejection_reasons'].append(error_msg)
            context['errors'].append(error_msg)
            return False

    # ------------------------------------------------------------------
    # Factory methods — one per business rule
    # ------------------------------------------------------------------

    @staticmethod
    def create_minimum_age_rule():
        """Rule 1: Applicant must be at least 18 years old"""
        return Rule(
            name="minimum_age",
            description="Applicant must be at least 18 years old",
            condition=lambda ctx: ctx['age'] >= 18,
            action=lambda ctx: ctx.update({'eligible': True}),
            explanation_func=lambda ctx: (
                f"Applicant age {ctx['age']} meets minimum requirement (18+)"
            ),
            failure_message=lambda ctx: (
                f"Age {ctx['age']} is below minimum requirement (18)"
            ),
        )

    @staticmethod
    def create_debt_to_income_rule():
        """Rule 2: Monthly debt must be less than 50% of monthly income"""
        return Rule(
            name="debt_to_income",
            description="Monthly debt must be less than 50% of monthly income (DTI < 50%)",
            condition=lambda ctx: (
                ctx['monthly_income'] > 0
                and (ctx['current_debt'] / ctx['monthly_income']) < 0.5
            ),
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
            ),
        )

    @staticmethod
    def create_credit_score_rule():
        """Rule 3: Minimum credit score of 600 required"""
        return Rule(
            name="minimum_credit_score",
            description="Credit score must be at least 600",
            condition=lambda ctx: ctx['credit_score'] >= 600,
            action=lambda ctx: ctx.update({'credit_score_ok': True}),
            explanation_func=lambda ctx: (
                f"Credit score {ctx['credit_score']} meets minimum (600+)"
            ),
            failure_message=lambda ctx: (
                f"Credit score {ctx['credit_score']} is below minimum (600)"
            ),
        )

    @staticmethod
    def create_employment_rule():
        """Rule 4: Stable employment history (>2 years) is required"""
        return Rule(
            name="employment_stability",
            description="Stable employment history of more than 2 years is required",
            condition=lambda ctx: ctx['stable_employment'],
            action=lambda ctx: ctx.update({'employment_ok': True}),
            explanation_func=lambda ctx: "Stable employment confirmed (>2 years)",
            failure_message="Employment history insufficient (<2 years or unstable)",
        )

    @staticmethod
    def create_interest_rate_rule():
        """
        Rule 5: Calculate interest rate based on risk profile.

        IMPORTANT: This rule must run AFTER the approval decision is set,
        because its condition checks ctx['approved']. The engine handles
        this by running this rule in a separate phase.
        """
        def calculate_interest(context):
            base_rate = 8.0

            # Credit score adjustments
            if context['credit_score'] >= 750:
                base_rate -= 2.5
            elif context['credit_score'] >= 650:
                base_rate -= 1.0

            # Employment stability adjustment
            if context['stable_employment']:
                base_rate -= 0.5

            # Debt ratio adjustment
            debt_ratio = context['current_debt'] / context['monthly_income']
            if debt_ratio < 0.3:
                base_rate -= 0.5

            context['interest_rate'] = max(5.0, base_rate)
            context['monthly_payment'] = _calculate_monthly_payment(
                context['loan_amount'],
                context['interest_rate'],
                context['loan_term'],
            )

        return Rule(
            name="calculate_interest_rate",
            description="Calculates interest rate and monthly payment based on applicant's risk profile",
            condition=lambda ctx: ctx.get('approved', False),
            action=calculate_interest,
            explanation_func=lambda ctx: (
                f"Interest rate calculated: {ctx.get('interest_rate', 0):.2f}% APR, "
                f"monthly payment: ${ctx.get('monthly_payment', 0):,.2f}"
            ),
            failure_message=None,
        )


def _calculate_monthly_payment(principal, annual_rate, months):
    """Standard amortization formula for monthly payment calculation"""
    monthly_rate = annual_rate / 100 / 12
    if monthly_rate == 0:
        return principal / months
    return (
        principal
        * (monthly_rate * (1 + monthly_rate) ** months)
        / ((1 + monthly_rate) ** months - 1)
    )