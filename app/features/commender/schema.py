from enum import Enum
from pydantic import BaseModel, Field


class MatchPrefix(str, Enum):
    MATCH = "Matched"
    PARTIAL_MATCH = "Partially Matched"
    NO_MATCH = "Not Matched"


class CommendResponse(BaseModel):
    reason: str = Field(
        description=(
            "Concise analysis comparing the CV item against the JD requirement. "
            "Identify whether requirements match fully, partially, or clash/missing."
        ),
    )

    prefix: MatchPrefix = Field(
        description=(
            "Final verdict based on the reason above:\n"
            "- 'Matched': Candidate explicitly satisfies the exact requirement.\n"
            "- 'Partially Matched': Related experience present, but lower level or incomplete.\n"
            "- 'Not Matched': Requirement is missing or completely different."
        ),
    )