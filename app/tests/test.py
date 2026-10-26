from app.features.extractor.ollama_model import OLLAMAModel
from app.models.infor_extracted import InforExtractedResume, InforExtractedJD


def test_resume(model: OLLAMAModel):
    resume_text = """
    Nguyen Van An
    Backend Developer

    Skills:
    Python, FastAPI, PostgreSQL, Docker, Git

    Education:
    Bachelor's degree in Software Engineering at Ton Duc Thang University.

    Experience:
    Backend Developer Intern at ABC Company from 2025 to 2026.
    Developed REST APIs using FastAPI and PostgreSQL.
    Used Docker to containerize backend services.

    Projects:
    AI Recruitment Assistant built with FastAPI, PostgreSQL,
    Docker, and an LLM for extracting information from resumes.

    Certificates:
    AWS Certified Cloud Practitioner.
    """
    
    # resume_text = """
    # Nguyen Van An

    # Certificates:
    # AWS Certified Cloud Practitioner.
    # """

    result = model.extract(
        parsed_text=resume_text,
        is_resume=True,
    )

    assert isinstance(result, InforExtractedResume)

    print("\n========== RESUME RESULT ==========")
    print(result.model_dump_json(indent=2))


def test_jd(model: OLLAMAModel):
    jd_text = """
    Job Title: Python Backend Developer

    Requirements:
    - At least 1 year of experience in Python development.
    - Proficiency in FastAPI and REST API design.
    - Experience with PostgreSQL and SQL.
    - Familiarity with Docker and Git.
    - Bachelor's degree in Computer Science or Software Engineering.

    Responsibilities:
    - Develop and maintain backend APIs.
    - Design and optimize database queries.
    - Collaborate with frontend developers.
    - Write clean, maintainable, and testable code.

    Preferred Qualifications:
    - Experience with CI/CD pipelines.
    - AWS certification is a plus.
    """

    result = model.extract(
        parsed_text=jd_text,
        is_resume=False,
    )

    assert isinstance(result, InforExtractedJD)

    print("\n========== JOB DESCRIPTION RESULT ==========")
    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    model = OLLAMAModel()

    try:
        test_resume(model)
        test_jd(model)
    finally:
        model.client.close()
