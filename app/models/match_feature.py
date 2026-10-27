from dataclasses import dataclass

@dataclass
class MatchFeature:
    feature_type: str
    cv_text: str
    jd_text: str
    weight: float = 1.0