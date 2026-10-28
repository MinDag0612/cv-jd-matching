from enum import Enum
from typing import List
from pydantic import BaseModel, Field


class MatchPrefix(str, Enum):
    MATCH = "Matched"
    PARTIAL_MATCH = "Partially Matched"
    NO_MATCH = "Not Matched"


class ItemMatchDetail(BaseModel):
    jd_requirement: str = Field(
        description="The exact item/requirement listed in the Job Description."
    )
    matched_cv_evidence: str = Field(
        description="The matching evidence found in the CV. Put 'None' if completely missing."
    )
    reason: str = Field(
        description="Concise 1-sentence analysis comparing CV evidence against this JD requirement."
    )
    prefix: MatchPrefix = Field(
        description="Verdict for THIS SPECIFIC requirement ('Matched', 'Partially Matched', or 'Not Matched')."
    )


class CommendResponse(BaseModel):
    item_details: List[ItemMatchDetail] = Field(
        description="Detailed mapping and evaluation for EVERY requirement listed in the JD."
    )
    overall_reason: str = Field(
        description="Summary explanation synthesizing the item_details above into a final verdict."
    )
    overall_prefix: MatchPrefix = Field(
        description=(
            "Final overall verdict:\n"
            "- 'Matched': Most or all key JD requirements are satisfied.\n"
            "- 'Partially Matched': Meets core requirements but lacks secondary ones.\n"
            "- 'Not Matched': Missing core capabilities or major mismatch."
        ),
    )