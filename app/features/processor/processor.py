from typing import Any

from fastapi import UploadFile

from app.features.commender.commender import Commender
from app.features.processor.schema import ResultCompareResponse
from app.features.score.similarity_scorer import SimilarityScorer
from app.features.extractor.extractor_service import extract_information
from app.features.parser.parser_service import parse_uploaded_file
from app.models.infor_extracted import InforExtractedJD, InforExtractedResume
from app.models.match_feature import MatchFeature


class Processor:
    def __init__(self) -> None:
        self._scorer: SimilarityScorer | None = None

    def process_text(self, text: str, is_resume: bool = False) -> dict:
        return extract_information(text, is_resume)

    def process_file(self, file: UploadFile, is_resume: bool = False) -> dict:
        parsed_text = parse_uploaded_file(file)
        information = self.process_text(parsed_text, is_resume)
        return {
            "filename": file.filename,
            "parsed_text": parsed_text,
            "information": information,
        }

    def compare(
        self,
        cv_data: InforExtractedResume,
        jd_data: InforExtractedJD,
    ) -> ResultCompareResponse:
        feature_groups = [
            ("skill", cv_data.skill, jd_data.skill),
            ("education", cv_data.education, jd_data.education),
            ("experience", cv_data.experience, jd_data.experience),
            ("certificate", cv_data.certificate, jd_data.certificate),
            ("project", cv_data.project, jd_data.responsibilities),
        ]
        match_features = [
            MatchFeature(
                feature_type=feature_type,
                cv_text="\n".join(cv_items),
                jd_text="\n".join(jd_items),
            )
            for feature_type, cv_items, jd_items in feature_groups
            if cv_items and jd_items
        ]

        if self._scorer is None:
            self._scorer = SimilarityScorer()
        total_score = self._scorer.score_total(match_features)

        commender = Commender()
        try:
            list_commend = {
                match_feature.feature_type: commender.commend(match_feature)
                for match_feature in match_features
            }
        finally:
            commender.client.close()

        return ResultCompareResponse(
            total_score=total_score,
            list_commend=list_commend,
        )
