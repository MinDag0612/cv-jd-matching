from app.models.infor_extracted import InforExtractedJD, InforExtractedResume
from app.models.match_feature import MatchFeature

class PairingService:
    def __init__(self):
        pass
        
    def match_features(
        self,
        cv_data: InforExtractedResume, 
        jd_data: InforExtractedJD
    ) -> list[MatchFeature]:
        feature_groups = [
                ("skill", cv_data.skill, jd_data.skill),
                ("education", cv_data.education, jd_data.education),
                ("experience", cv_data.experience, jd_data.experience),
                ("certificate", cv_data.certificate, jd_data.certificate),
                ("project", cv_data.project, jd_data.responsibilities),
            ]
        return [
            MatchFeature(
                feature_type=feature_type,
                cv_text="\n".join(cv_items),
                jd_text="\n".join(jd_items),
            )
            for feature_type, cv_items, jd_items in feature_groups
            if cv_items and jd_items
        ]