# Rule-Based AI Credit Decision System

A demonstration of symbolic artificial intelligence using explicit business rules for transparent and explainable decision making. Built with Django as a microframework.

## Overview

This project implements a **rule-based expert system** - a classic form of symbolic AI that uses explicit IF-THEN rules to make decisions. Unlike machine learning approaches, every decision is fully explainable and based on human-defined business logic. For more details, see the accompanying blog post [here](https://medium.com/@joegsuero/filling-the-gaps-in-ai-part-2-rule-based-systems-02c32fea6747).

The system evaluates credit applications using a forward-chaining inference engine that applies business rules sequentially, building up facts about the application until a final decision is reached.

## Key Features

- **Transparent Decision Making**: Every decision is fully traceable to specific business rules
- **Forward-Chaining Inference Engine**: Rules are evaluated in sequence, with each rule potentially adding new facts to the context
- **REST API**: Programmatic access to the decision engine
- **Explainability**: Detailed explanations of which rules passed or failed
- **Configurable Rules**: Business rules are stored separately from the engine logic

## Architecture

### Core Components

```
├── ai_engine/                    # AI Engine Module
│   ├── engine.py                # Forward-chaining inference engine
│   └── rules.py                 # Business rule definitions
├── web/                         # Web Interface Module
│   ├── views.py                 # Request handlers and controllers
│   └── forms.py                 # Data parsing and validation
└── templates/                   # HTML templates
```

### Rule-Based AI Engine

The heart of the system is a forward-chaining inference engine that:

1. **Initializes Context**: Creates an evaluation context with application data
2. **Applies Rules Sequentially**: Each rule's condition is evaluated against the context
3. **Executes Actions**: When a rule's condition is true, its action modifies the context
4. **Builds Explanations**: Each rule generates an explanation of its evaluation
5. **Reaches Conclusion**: Final decision is based on accumulated facts

### Business Rules

The system implements five core business rules:

1. **Minimum Age Rule**: Applicant must be at least 18 years old
2. **Debt-to-Income Ratio Rule**: Monthly debt must be less than 50% of monthly income
3. **Credit Score Rule**: Minimum credit score of 600 required
4. **Employment Stability Rule**: Stable employment history improves approval chances
5. **Risk-Based Pricing Rule**: Calculates interest rate based on risk factors

## How It Works: Rule-Based AI Explained

### What is Rule-Based AI?

Rule-based AI (also known as expert systems or symbolic AI) uses explicit, human-readable rules to make decisions. Each rule follows the pattern:

```
IF (condition is true)
THEN (take action or infer new fact)
```

### Forward-Chaining Inference

This system uses **forward-chaining inference**, which means:

1. The engine starts with initial facts (application data)
2. Rules are evaluated against these facts
3. When a rule's condition matches, its action adds new facts to the context
4. The process continues until no more rules can be applied
5. The final decision is based on the accumulated facts

---
![Engine Flowchart](/01-rule-based-ai/assets/engine-flowchart.png)

### Example Rule Evaluation

```python
# Rule Definition
Rule(
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
```

### Benefits Over Simple If-Else Logic

1. **Separation of Concerns**: Rules are stored separately from the engine logic
2. **Maintainability**: Business rules can be modified without changing engine code
3. **Explainability**: Each rule generates its own explanation
4. **Extensibility**: New rules can be added without affecting existing ones
5. **Transparency**: Decision process is fully visible and auditable

## Technical Implementation

### Django as Microframework

This project uses Django in a microframework pattern based on Carlton Gibson's DjangoCon presentation. Key aspects:

- Minimal Django configuration
- No Django admin or built-in apps
- Direct URL routing in `app.py`
- Manual template and static file handling
- Lightweight request/response cycle

### Installation & Setup

```bash
git clone https://github.com/joegsuero/ai-explained.git
cd ai-explained/01-rule-based-ai

pip install -r requirements.txt

python app.py runserver
```

## Use Cases

This type of rule-based AI system is ideal for:

- **Financial Services**: Loan approvals, credit scoring, risk assessment
- **Healthcare**: Diagnostic systems, treatment recommendations
- **Insurance**: Policy underwriting, claim processing
- **Compliance**: Regulatory rule checking, audit systems
- **Business Process Automation**: Approval workflows, eligibility checks

## Comparison with Other AI Approaches

| Aspect             | Rule-Based AI             | Machine Learning           |
| ------------------ | ------------------------- | -------------------------- |
| **Transparency**   | Fully transparent         | Often opaque ("black box") |
| **Training Data**  | None required             | Large datasets needed      |
| **Explainability** | Rule-by-rule explanations | Limited explainability     |
| **Maintenance**    | Manual rule updates       | Retraining with new data   |
| **Edge Cases**     | Handled explicitly        | May fail unpredictably     |
| **Development**    | Domain expert driven      | Data scientist driven      |

## Extending the System

### Adding New Rules

```python
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
```

## Limitations and Considerations

1. **Rule Complexity**: As rules multiply, conflicts may arise
2. **Maintenance Overhead**: Rules must be kept current with business changes
3. **Limited Learning**: System doesn't improve automatically with data
4. **Expert Dependency**: Requires domain experts to define and maintain rules
