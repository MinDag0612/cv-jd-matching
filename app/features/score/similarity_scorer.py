from sentence_transformers import SentenceTransformer

from app.features.score.match_feature import MatchFeature


class SimilarityScorer:
    def __init__(self) -> None:
        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

    def score(self, match_feature: MatchFeature) -> float:
        embeddings = self.model.encode(
            [
                match_feature.cv_text,
                match_feature.jd_text,
            ],
            normalize_embeddings=True,
        )

        return float(embeddings[0] @ embeddings[1])