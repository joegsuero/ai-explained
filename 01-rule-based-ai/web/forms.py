"""Form parsing and validation for credit applications"""


class ValidationError(Exception):
    """Raised when form data fails validation"""
    pass


class CreditApplicationForm:
    """Parses and validates POST form data for a credit application"""

    @staticmethod
    def parse_form_data(request):
        """
        Parse and validate form data from a POST request.

        Returns a clean dict ready for the rules engine.
        Raises ValidationError with a human-readable message if any field is invalid.
        """
        errors = []

        age = CreditApplicationForm._parse_int(
            request.POST.get('age'), 'Age', min_val=0, max_val=120, errors=errors
        )
        monthly_income = CreditApplicationForm._parse_float(
            request.POST.get('monthly_income'), 'Monthly Income', min_val=0, errors=errors
        )
        current_debt = CreditApplicationForm._parse_float(
            request.POST.get('current_debt'), 'Monthly Debt', min_val=0, errors=errors
        )
        credit_score = CreditApplicationForm._parse_int(
            request.POST.get('credit_score'), 'Credit Score', min_val=300, max_val=850, errors=errors
        )
        loan_amount = CreditApplicationForm._parse_float(
            request.POST.get('loan_amount'), 'Loan Amount', min_val=1, errors=errors
        )
        loan_term = CreditApplicationForm._parse_int(
            request.POST.get('loan_term'), 'Loan Term', min_val=1, errors=errors
        )
        stable_employment = request.POST.get('stable_employment') == 'true'

        if errors:
            raise ValidationError("; ".join(errors))

        return {
            'age': age,
            'monthly_income': monthly_income,
            'current_debt': current_debt,
            'credit_score': credit_score,
            'stable_employment': stable_employment,
            'loan_amount': loan_amount,
            'loan_term': loan_term,
        }

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _parse_int(value, field_name, min_val=None, max_val=None, errors=None):
        try:
            parsed = int(value)
        except (TypeError, ValueError):
            if errors is not None:
                errors.append(f"'{field_name}' must be a whole number")
            return 0

        if min_val is not None and parsed < min_val:
            if errors is not None:
                errors.append(f"'{field_name}' must be at least {min_val}")
        if max_val is not None and parsed > max_val:
            if errors is not None:
                errors.append(f"'{field_name}' must be at most {max_val}")

        return parsed

    @staticmethod
    def _parse_float(value, field_name, min_val=None, errors=None):
        try:
            parsed = float(value)
        except (TypeError, ValueError):
            if errors is not None:
                errors.append(f"'{field_name}' must be a number")
            return 0.0

        if min_val is not None and parsed < min_val:
            if errors is not None:
                errors.append(f"'{field_name}' must be at least {min_val}")

        return parsed