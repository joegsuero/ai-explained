import json
from django.http import JsonResponse
from django.shortcuts import render
from ai_engine.engine import CreditRulesEngine
from .forms import CreditApplicationForm, ValidationError


def home_view(request):
    """Main view — renders application form (GET) or evaluates it (POST)"""
    if request.method == 'POST':
        try:
            form_data = CreditApplicationForm.parse_form_data(request)
        except ValidationError as e:
            # Return to form with validation error message
            return render(request, 'form.html', {'error': str(e)})

        engine = CreditRulesEngine()
        decision = engine.evaluate_application(form_data)

        context = {
            'decision': decision,
            'status_color': "#28a745" if decision['approved'] else "#dc3545",
            'total_rules': len(engine.rules) + 1,  # +1 for interest rate rule
            'debt_ratio': (
                (decision['current_debt'] / decision['monthly_income']) * 100
                if decision['monthly_income'] > 0 else 0
            ),
            'total_cost': decision.get('monthly_payment', 0) * decision['loan_term'],
        }

        return render(request, 'decision.html', context)

    return render(request, 'form.html')


def api_evaluate(request):
    """
    JSON API — programmatic access to the rules engine.

    POST body (JSON):
        age, monthly_income, current_debt, credit_score,
        stable_employment, loan_amount, loan_term
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON body'}, status=400)

    try:
        engine = CreditRulesEngine()
        decision = engine.evaluate_application(data)
        return JsonResponse(decision)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


def api_rules_info(request):
    """JSON API — returns static info about all loaded rules"""
    engine = CreditRulesEngine()
    return JsonResponse({'rules': engine.get_rules_info()})