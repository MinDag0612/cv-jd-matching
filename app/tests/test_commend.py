from app.features.recommendation.service import RecommendationService
from app.models.match_feature import MatchFeature


def main() -> None:
    recommender = RecommendationService()

    match_feature = MatchFeature(
        feature_type="skill",
        cv_text="Developed REST APIs using FastAPI and PostgreSQL.",
        jd_text="Experience building backend services with Python.",
    )

    response = recommender.recommend(match_feature)

    print("LLM response:")
    print(response)


if __name__ == "__main__":
    main()