from enum import Enum
from typing import List
from pydantic import BaseModel, Field

class MatchPrefix(str, Enum):
    MATCHED = "Matched"
    PARTIALLY_MATCHED = "Partially Matched"
    NOT_MATCHED = "Not Matched"

class ItemMatchDetail(BaseModel):
    jd_requirement: str = Field(
        description="The specific requirement extracted from the Job Description."
    )
    matched_cv_evidence: str = Field(
        description="The corresponding evidence extracted from the candidate's CV."
    )
    reason: str = Field(
        description="Detailed explanation in ENGLISH analyzing whether the CV evidence matches the JD requirement and why."
    )
    prefix: MatchPrefix = Field(
        description="Individual evaluation prefix for this requirement."
    )

class CommendResponse(BaseModel):
    item_details: List[ItemMatchDetail] = Field(
        description="Detailed mapping and evaluation for EVERY requirement listed in the JD."
    )
    overall_reason: str = Field(
        description="Summary explanation synthesizing all item_details above into a final verdict. MUST be written entirely in ENGLISH."
    )
    overall_prefix: MatchPrefix = Field(
        description=(
            "Final overall verdict:\n"
            "- 'Matched': Most or all key JD requirements are satisfied.\n"
            "- 'Partially Matched': Meets core requirements but lacks secondary ones.\n"
            "- 'Not Matched': Missing core capabilities or major mismatch."
        )
    )