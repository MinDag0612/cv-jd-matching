from sentence_transformers import SentenceTransformer

from app.models.match_feature import MatchFeature


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
            normalize_embeddings=True, # Chuản hóa về 1
        )

        return float(embeddings[0] @ embeddings[1]) * match_feature.weight # chuẩn hóa về 1, tích vô hướng =  cosine
    
    def score_total(self, all_match_feature: list[MatchFeature]) -> float:
        total_score = 0.0
        for pair in all_match_feature:
            embeddings = self.model.encode(
                [
                    pair.cv_text,
                    pair.jd_text,
                ],
                normalize_embeddings=True,
            )
            
            score = float(embeddings[0] @ embeddings[1]) * pair.weight
            
            total_score += score

        return total_score / len(all_match_feature)
            