from typing import Any

from fastapi import UploadFile

from app.features.recommendation.service import RecommendationService
from app.models.infor_process import ResultCompareResponse
from app.features.scoring.service import ScoringService
from app.features.extraction.service import extract_information
from app.features.parsing.service import parse_uploaded_file
from app.models.infor_extracted import InforExtractedJD, InforExtractedResume
from app.models.match_feature import MatchFeature
from app.models.infor_process import ProcessorFileResponse
from app.features.pairing.service import PairingService


# def _match_features(
#     cv_data: InforExtractedResume,
#     jd_data: InforExtractedJD,
# ) -> list[MatchFeature]:
#     feature_groups = [
#         ("skill", cv_data.skill, jd_data.skill),
#         ("education", cv_data.education, jd_data.education),
#         ("experience", cv_data.experience, jd_data.experience),
#         ("certificate", cv_data.certificate, jd_data.certificate),
#         ("project", cv_data.project, jd_data.responsibilities),
#     ]
#     return [
#         MatchFeature(
#             feature_type=feature_type,
#             cv_text="\n".join(cv_items),
#             jd_text="\n".join(jd_items),
#         )
#         for feature_type, cv_items, jd_items in feature_groups
#         if cv_items and jd_items
#     ]


class ProcessingService:
    def __init__(self) -> None:
        self._scorer: ScoringService | None = None # Truyền score vào ở API
        self.pairer = PairingService()

    def process_text(self, text: str, is_resume: bool = False) -> dict:
        return extract_information(text, is_resume)

    def process_file(self, file: UploadFile, is_resume: bool = False) -> dict:
        parsed_text = parse_uploaded_file(file)
        information = self.process_text(parsed_text, is_resume)
        return ProcessorFileResponse(
            filename=file.filename,
            parsed_text=parsed_text,
            information=information
        )

    def compare(
        self,
        cv_data: InforExtractedResume,
        jd_data: InforExtractedJD,
    ) -> ResultCompareResponse:
        match_features = self.pairer.match_features(cv_data, jd_data)

        if self._scorer is None:
            self._scorer = ScoringService()
        total_score = self._scorer.score_total(match_features)

        recommender = RecommendationService()
        try:
            list_commend = {
                match_feature.feature_type: recommender.recommend(match_feature)
                for match_feature in match_features
            }
        finally:
            recommender.client.close()

        return ResultCompareResponse(
            total_score=total_score,
            list_commend=list_commend,
        )
