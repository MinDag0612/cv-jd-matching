from app.features.commender.commender import Commender
from app.models.match_feature import MatchFeature


def main() -> None:
    commender = Commender()

    match_feature = MatchFeature(
        feature_type="skill",
        cv_text="Developed REST APIs using FastAPI and PostgreSQL.",
        jd_text="Experience building backend services with Python.",
    )

    response = commender.commend(match_feature)

    print("LLM response:")
    print(response)


if __name__ == "__main__":
    main()