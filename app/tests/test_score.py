from app.features.score.similarity_scorer import SimilarityScorer
from app.models.match_feature import MatchFeature


def main() -> None:
    scorer = SimilarityScorer()

    match_feature = MatchFeature(
        feature_type="skill",
        cv_text="Developed REST APIs using FastAPI and PostgreSQL.",
        jd_text="Experience building backend services with Python.",
    )

    similarity = scorer.score(match_feature)

    print(f"Similarity score: {similarity:.4f}")


if __name__ == "__main__":
    main()