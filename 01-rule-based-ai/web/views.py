import json
from django.http import JsonResponse
from django.shortcuts import render
from ai_engine.engine import CreditRulesEngine
from .forms import CreditApplicationForm


def home_view(request):
    """Main view for the application form"""
    if request.method == 'POST':
        form_data = CreditApplicationForm.parse_form_data(request)

        engine = CreditRulesEngine()

        decision = engine.evaluate_application(form_data)

        context = {
            'decision': decision,
            'status_color': "#28a745" if decision['approved'] else "#dc3545",
            'status_icon': "✅" if decision['approved'] else "❌",
            'status_text': "APPROVED" if decision['approved'] else "REJECTED",
            'total_rules': len(engine.rules),
            'debt_ratio': (decision['current_debt'] / decision['monthly_income']) * 100,
            'total_cost': decision.get('monthly_payment', 0) * decision['loan_term'],
            'decision_requirements': "Minimum age 18, debt ratio < 50%, credit score ≥ 600"
        }

        return render(request, 'decision.html', context)

    return render(request, 'form.html')


def api_evaluate(request):
    """JSON API endpoint for programmatic access"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            engine = CreditRulesEngine()
            decision = engine.evaluate_application(data)
            return JsonResponse(decision)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'POST method required'}, status=405)


def api_rules_info(request):
    """API endpoint to get information about all rules"""
    engine = CreditRulesEngine()
    rules_info = engine.get_rules_info()
    return JsonResponse({'rules': rules_info})
