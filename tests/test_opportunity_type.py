from app.collectors.opportunity_type import detect_opportunity_type

def test_detect_opportunity_type_freelance():
    assert detect_opportunity_type("Mindrift: Freelance Full-Stack Web App Developer", "") == "freelance"

def test_detect_opportunity_type_contract_regression():
    assert detect_opportunity_type("Senior Software Engineer", "This is a 6-month contract position") == "remote_job"

def test_detect_opportunity_type_default():
    assert detect_opportunity_type("Regular Job Title", "") == "remote_job"

def test_detect_opportunity_type_empty():
    assert detect_opportunity_type("", "") == "remote_job"
