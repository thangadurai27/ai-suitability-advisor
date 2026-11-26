"""Initialize the database and add sample data."""
import sys
import os
sys.path.insert(0, 'C:\\TechMahindra\\Day1\\ai-suitability-advisor\\backend')

from app.database import engine, SessionLocal, Base
from app.models import User, Requirement
from app.core.decision_engine import RequirementSchema, decide_ai_suitability


# Create tables
Base.metadata.create_all(bind=engine)
print('Tables created')

# Create session
db = SessionLocal()

# Create a default user
hashed_password = 'demo1234'
default_user = User(
    email='demo@ai-suitability-advisor.com',
    hashed_password=hashed_password,
    is_active=True,
    is_superuser=False,
)
db.add(default_user)
db.commit()
print('User created')

# Sample requirements data
samples = [
    {
        'id': 'pan_validation',
        'title': 'Validate PAN number format',
        'description': 'Validate PAN card format',
        'fixed_rules_possible': True,
        'needs_learning_from_data': False,
        'unstructured_input': False,
        'requires_content_generation': False,
        'data_available': False,
        'domain': 'Finance',
    },
    {
        'id': 'customer_cancellation',
        'title': 'Predict customer cancellation',
        'description': 'Identify customers at risk of churning',
        'fixed_rules_possible': False,
        'needs_learning_from_data': True,
        'unstructured_input': False,
        'requires_content_generation': False,
        'data_available': True,
        'domain': 'Marketing',
    },
    {
        'id': 'support_email_summarisation',
        'title': 'Summarise support emails',
        'description': 'Create email summaries',
        'fixed_rules_possible': False,
        'needs_learning_from_data': False,
        'unstructured_input': True,
        'requires_content_generation': True,
        'data_available': True,
        'domain': 'Customer Support',
    },
    {
        'id': 'product_defect_detection',
        'title': 'Detect product defects',
        'description': 'Identify defects in product images',
        'fixed_rules_possible': False,
        'needs_learning_from_data': True,
        'unstructured_input': True,
        'requires_content_generation': False,
        'data_available': True,
        'domain': 'Manufacturing',
    },
    {
        'id': 'gst_calculation',
        'title': 'Calculate GST',
        'description': 'Calculate GST on invoices',
        'fixed_rules_possible': True,
        'needs_learning_from_data': False,
        'unstructured_input': False,
        'requires_content_generation': False,
        'data_available': False,
        'domain': 'Finance',
    },
    {
        'id': 'demand_forecasting',
        'title': 'Forecast weekly product demand',
        'description': 'Predict weekly demand',
        'fixed_rules_possible': False,
        'needs_learning_from_data': True,
        'unstructured_input': False,
        'requires_content_generation': False,
        'data_available': True,
        'domain': 'Operations',
    },
    {
        'id': 'hr_policy_qa',
        'title': 'Answer HR policy questions',
        'description': 'QA from HR policy PDF',
        'fixed_rules_possible': False,
        'needs_learning_from_data': False,
        'unstructured_input': True,
        'requires_content_generation': True,
        'data_available': True,
        'domain': 'HR',
    },
    {
        'id': 'invoice_sorting',
        'title': 'Sort invoices by amount',
        'description': 'Sort invoices by amount',
        'fixed_rules_possible': True,
        'needs_learning_from_data': False,
        'unstructured_input': False,
        'requires_content_generation': False,
        'data_available': False,
        'domain': 'Finance',
    },
    {
        'id': 'fraud_detection',
        'title': 'Detect fraudulent transactions',
        'description': 'Detect fraud',
        'fixed_rules_possible': False,
        'needs_learning_from_data': True,
        'unstructured_input': False,
        'requires_content_generation': False,
        'data_available': True,
        'domain': 'Finance',
    },
    {
        'id': 'customer_feedback',
        'title': 'Classify customer feedback',
        'description': 'Classify feedback',
        'fixed_rules_possible': False,
        'needs_learning_from_data': True,
        'unstructured_input': True,
        'requires_content_generation': False,
        'data_available': True,
        'domain': 'Customer Success',
    },
]

for s in samples:
    # Validate with decision engine
    req_schema = RequirementSchema(
        id=s['id'],
        title=s['title'],
        description=s['description'],
        fixed_rules_possible=s['fixed_rules_possible'],
        needs_learning_from_data=s['needs_learning_from_data'],
        unstructured_input=s['unstructured_input'],
        requires_content_generation=s['requires_content_generation'],
        data_available=s['data_available'],
        domain=s['domain'],
    )
    
    result = decide_ai_suitability(req_schema)
    
    req = Requirement(
        id=s['id'],
        title=s['title'],
        description=s['description'],
        fixed_rules_possible=s['fixed_rules_possible'],
        needs_learning_from_data=s['needs_learning_from_data'],
        unstructured_input=s['unstructured_input'],
        requires_content_generation=s['requires_content_generation'],
        data_available=s['data_available'],
        domain=s['domain'],
        owner_id=None,
    )
    db.add(req)
    print(f'Created: {s["id"]} -> {result.decision.value}')

db.commit()
db.close()
print('All seed data created successfully!')