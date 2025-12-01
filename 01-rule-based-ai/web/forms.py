class CreditApplicationForm:
    """Form data parsing without HTML rendering"""

    @staticmethod
    def parse_form_data(request):
        """Parse and validate form data from POST request"""
        data = {
            'age': int(request.POST.get('age', 0)),
            'monthly_income': float(request.POST.get('monthly_income', 0)),
            'current_debt': float(request.POST.get('current_debt', 0)),
            'credit_score': int(request.POST.get('credit_score', 300)),
            'stable_employment': request.POST.get('stable_employment') == 'true',
            'loan_amount': float(request.POST.get('loan_amount', 0)),
            'loan_term': int(request.POST.get('loan_term', 12))
        }
        return data
