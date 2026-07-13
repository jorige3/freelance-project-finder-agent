from app.database.models import FreelanceProject
from app.proposal.generator import is_tech_job

def test_is_tech_job_positive():
    p_python = FreelanceProject(
        title="Python Developer",
        description="Write some code",
        skills=""
    )
    p_fastapi = FreelanceProject(
        title="Web Developer",
        description="Build something",
        skills="fastapi"
    )
    assert is_tech_job(p_python) is True
    assert is_tech_job(p_fastapi) is True

def test_is_tech_job_negative():
    p_houseperson = FreelanceProject(
        title="Houseperson",
        description="Clean rooms and carry bags",
        skills=""
    )
    p_barista = FreelanceProject(
        title="Barista",
        description="Serve coffee at local shop",
        skills=""
    )
    assert is_tech_job(p_houseperson) is False
    assert is_tech_job(p_barista) is False

def test_is_tech_job_word_boundary():
    p_substring = FreelanceProject(
        title="myjavatest",
        description="Non-tech description",
        skills=""
    )
    assert is_tech_job(p_substring) is False

    p_exact = FreelanceProject(
        title="Java Developer",
        description="",
        skills=""
    )
    assert is_tech_job(p_exact) is True
