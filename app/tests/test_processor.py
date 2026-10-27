from app.features.processor.processor import Processor
from app.models.infor_extracted import InforExtractedJD, InforExtractedResume


def main() -> None:
    processor = Processor()

    cv_data = InforExtractedResume(
        skill=[
            "Developed REST APIs using FastAPI and PostgreSQL.",
            "Implemented authentication and authorization using JWT.",
            "Used Docker to containerize backend applications.",
            "Worked with MongoDB for data storage.",
            "Built frontend interfaces using React and JavaScript.",
        ],
        education=[
            "Bachelor's degree in Software Engineering at Ton Duc Thang University."
        ],
        experience=[
            "Backend Developer Intern at ABC Company.",
            "Developed REST APIs using Python and FastAPI.",
            "Designed PostgreSQL database schemas and optimized SQL queries.",
            "Implemented automated tests using Pytest.",
        ],
        certificate=[
            "AWS Certified Cloud Practitioner."
        ],
        project=[
            "Developed a recruitment assistant using FastAPI, PostgreSQL, and Docker.",
            "Built a news recommendation system using NLP and Transformer models.",
        ],
    )

    jd_data = InforExtractedJD(
        skill=[
            "Experience building backend services with Python.",
            "Proficiency in SQL and PostgreSQL database design.",
            "Experience with Redis for caching.",
            "Knowledge of Docker and containerized deployments.",
            "Experience with Java and Spring Boot.",
        ],
        education=[
            "Bachelor's degree in Computer Science, Software Engineering, or a related field."
        ],
        experience=[
            "At least one year of experience developing backend applications.",
            "Experience designing and maintaining RESTful APIs.",
            "Experience writing unit tests and integration tests.",
        ],
        certificate=[
            "AWS certification is preferred."
        ],
        responsibilities=[
            "Design, develop, and maintain backend REST APIs.",
            "Optimize database queries and application performance.",
            "Implement caching mechanisms using Redis.",
            "Collaborate with frontend developers to integrate APIs.",
        ],
    )

    result = processor.compare(cv_data, jd_data)

    print(f"Total score: {result.total_score:.4f}")
    print("LLM recommendations:")
    for feature, commend in result.list_commend.items():
        print(f"{feature}: {commend.model_dump_json()}")


if __name__ == "__main__":
    main()
