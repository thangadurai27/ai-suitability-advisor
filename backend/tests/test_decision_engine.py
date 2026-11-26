"""Tests for the AI Suitability Advisor decision engine.

Tests verify that the decision engine correctly classifies business requirements
into the appropriate technology categories."""
import sys
sys.path.insert(0, 'C:\\TechMahindra\\Day1\\ai-suitability-advisor\\backend')

from app.core.decision_engine import decide_ai_suitability, RequirementSchema


def test_pan_validation_no_ai():
    """PAN validation should be classified as No AI."""
    req = RequirementSchema(
        id='1', title='Validate PAN number format', description='',
        fixed_rules_possible=True, needs_learning_from_data=False,
        unstructured_input=False, requires_content_generation=False,
        data_available=False, domain='Finance')
    result = decide_ai_suitability(req)
    assert result.decision.value == 'No AI', f"Expected No AI, got {result.decision.value}"


def test_gst_calculation_no_ai():
    """GST calculation should be classified as No AI."""
    req = RequirementSchema(
        id='2', title='Calculate GST on an invoice', description='',
        fixed_rules_possible=True, needs_learning_from_data=False,
        unstructured_input=False, requires_content_generation=False,
        data_available=False, domain='Finance')
    result = decide_ai_suitability(req)
    assert result.decision.value == 'No AI', f"Expected No AI, got {result.decision.value}"


def test_invoice_sorting_no_ai():
    """Invoice sorting should be classified as No AI."""
    req = RequirementSchema(
        id='3', title='Sort invoices by amount', description='',
        fixed_rules_possible=True, needs_learning_from_data=False,
        unstructured_input=False, requires_content_generation=False,
        data_available=False, domain='Finance')
    result = decide_ai_suitability(req)
    assert result.decision.value == 'No AI', f"Expected No AI, got {result.decision.value}"


def test_customer_cancellation_classical_ml():
    """Customer cancellation prediction should be classified as Classical ML."""
    req = RequirementSchema(
        id='4', title='Predict which customers will cancel next month', description='',
        fixed_rules_possible=False, needs_learning_from_data=True,
        unstructured_input=False, requires_content_generation=False,
        data_available=True, domain='Marketing')
    result = decide_ai_suitability(req)
    assert result.decision.value == 'Classical ML', f"Expected Classical ML, got {result.decision.value}"


def test_product_defect_detection_deep_learning():
    """Product defect detection should be classified as Deep Learning."""
    req = RequirementSchema(
        id='5', title='Detect defects in product photos', description='',
        fixed_rules_possible=False, needs_learning_from_data=True,
        unstructured_input=True, requires_content_generation=False,
        data_available=True, domain='Manufacturing')
    result = decide_ai_suitability(req)
    assert result.decision.value == 'Deep Learning', f"Expected Deep Learning, got {result.decision.value}"


def test_support_email_summarisation_generative_ai():
    """Support email summarisation should be classified as Generative AI."""
    req = RequirementSchema(
        id='6', title='Summarise long support emails', description='',
        fixed_rules_possible=False, needs_learning_from_data=False,
        unstructured_input=True, requires_content_generation=True,
        data_available=True, domain='Customer Support')
    result = decide_ai_suitability(req)
    assert result.decision.value == 'Generative AI', f"Expected Generative AI, got {result.decision.value}"


def test_demand_forecasting_analytics_bi():
    """Weekly demand forecasting should be classified as Analytics / BI."""
    req = RequirementSchema(
        id='7', title='Forecast weekly product demand', description='',
        fixed_rules_possible=False, needs_learning_from_data=True,
        unstructured_input=False, requires_content_generation=False,
        data_available=True, domain='Operations')
    result = decide_ai_suitability(req)
    assert result.decision.value == 'Analytics / BI', f"Expected Analytics / BI, got {result.decision.value}"


def test_hr_policy_qa_generative_ai():
    """HR policy question answering should be classified as Generative AI."""
    req = RequirementSchema(
        id='8', title='Answer employee questions from an HR policy PDF', description='',
        fixed_rules_possible=False, needs_learning_from_data=False,
        unstructured_input=True, requires_content_generation=True,
        data_available=True, domain='HR')
    result = decide_ai_suitability(req)
    assert result.decision.value == 'Generative AI', f"Expected Generative AI, got {result.decision.value}"


def test_fraud_detection_classical_ml():
    """Fraudulent transaction detection should be classified as Classical ML."""
    req = RequirementSchema(
        id='9', title='Detect fraudulent transactions', description='',
        fixed_rules_possible=False, needs_learning_from_data=True,
        unstructured_input=False, requires_content_generation=False,
        data_available=True, domain='Finance')
    result = decide_ai_suitability(req)
    assert result.decision.value == 'Classical ML', f"Expected Classical ML, got {result.decision.value}"


def test_customer_feedback_classical_ml():
    """Customer feedback classification should be classified as Classical ML."""
    req = RequirementSchema(
        id='10', title='Classify customer feedback', description='',
        fixed_rules_possible=False, needs_learning_from_data=True,
        unstructured_input=True, requires_content_generation=False,
        data_available=True, domain='Customer Success')
    result = decide_ai_suitability(req)
    assert result.decision.value == 'Classical ML', f"Expected Classical ML, got {result.decision.value}"


def test_decision_engine_has_five_lifecycle_stages_for_ai_suitable():
    """AI-suitable requirements should have lifecycle with five stages."""
    req = RequirementSchema(
        id='1', title='Test requirement', description='',
        fixed_rules_possible=False, needs_learning_from_data=True,
        unstructured_input=False, requires_content_generation=False,
        data_available=True, domain='Finance')
    result = decide_ai_suitability(req)
    assert len(result.lifecycle) == 5, f"Expected 5 lifecycle stages, got {len(result.lifecycle)}"
    assert set(result.lifecycle) == {
        'Problem Framing', 'Data Collection and Preparation',
        'Model Development', 'Deployment', 'Monitoring and Improvement'
    }, f"Lifecycle stages incorrect: {result.lifecycle}"


def test_decision_engine_contains_rule_ids():
    """Decision results should contain rule IDs."""
    req = RequirementSchema(
        id='1', title='Test requirement', description='',
        fixed_rules_possible=True, needs_learning_from_data=False,
        unstructured_input=False, requires_content_generation=False,
        data_available=False, domain='Finance')
    result = decide_ai_suitability(req)
    assert len(result.evidence.rule_ids) > 0, "Expected rule IDs in evidence"
    assert isinstance(result.evidence.rule_ids, list), "rule_ids should be a list"


def test_decision_has_reasons():
    """Decision results should have reasons."""
    req = RequirementSchema(
        id='1', title='Test requirement', description='',
        fixed_rules_possible=True, needs_learning_from_data=False,
        unstructured_input=False, requires_content_generation=False,
        data_available=False, domain='Finance')
    result = decide_ai_suitability(req)
    assert len(result.reasons) > 0, "Expected at least one reason"
    assert all(isinstance(r, str) and r.strip() for r in result.reasons), "All reasons should be non-empty strings"


def test_data_requirements_for_ai_suitable():
    """AI-suitable requirements should have data requirements."""
    req = RequirementSchema(
        id='1', title='Test requirement', description='',
        fixed_rules_possible=False, needs_learning_from_data=True,
        unstructured_input=False, requires_content_generation=False,
        data_available=True, domain='Finance')
    result = decide_ai_suitability(req)
    assert len(result.data_requirements) > 0, "Expected data requirements for AI-suitable requirements"


def test_alternative_approach_provided():
    """Every decision should have an alternative approach."""
    req = RequirementSchema(
        id='1', title='Test requirement', description='',
        fixed_rules_possible=True, needs_learning_from_data=False,
        unstructured_input=False, requires_content_generation=False,
        data_available=False, domain='Finance')
    result = decide_ai_suitability(req)
    assert result.alternative_approach, "Expected alternative approach"
    assert isinstance(result.alternative_approach, str) and result.alternative_approach.strip(), "alternative_approach should be a non-empty string"


def test_responsible_roles_provided():
    """Every decision should have responsible roles."""
    req = RequirementSchema(
        id='1', title='Test requirement', description='',
        fixed_rules_possible=True, needs_learning_from_data=False,
        unstructured_input=False, requires_content_generation=False,
        data_available=False, domain='Finance')
    result = decide_ai_suitability(req)
    assert len(result.responsible_roles) > 0, "Expected responsible roles"
    assert all(isinstance(r, str) and r.strip() for r in result.responsible_roles), "All roles should be non-empty strings"


# Run all tests
if __name__ == '__main__':
    tests = [
        test_pan_validation_no_ai,
        test_gst_calculation_no_ai,
        test_invoice_sorting_no_ai,
        test_customer_cancellation_classical_ml,
        test_product_defect_detection_deep_learning,
        test_support_email_summarisation_generative_ai,
        test_demand_forecasting_analytics_bi,
        test_hr_policy_qa_generative_ai,
        test_fraud_detection_classical_ml,
        test_customer_feedback_classical_ml,
        test_decision_engine_has_five_lifecycle_stages_for_ai_suitable,
        test_decision_engine_contains_rule_ids,
        test_decision_has_reasons,
        test_data_requirements_for_ai_suitable,
        test_alternative_approach_provided,
        test_responsible_roles_provided,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
            print(f'PASS: {test.__name__}')
        except Exception as e:
            failed += 1
            print(f'FAIL: {test.__name__} - {e}')
    
    print(f'\n{passed} passed, {failed} failed out of {len(tests)} tests')
    sys.exit(0 if failed == 0 else 1)