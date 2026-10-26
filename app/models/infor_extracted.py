
from pydantic import BaseModel, Field


class InforExtractedBase(BaseModel):
    skill: list[str] = Field(description="list of individual skills and tools")
    education: list[str] = Field(description="Educational background and degrees")
    experience: list[str] = Field(description="Work experience entries")
    certificate: list[str] = Field(description="Certifications and licenses earned")
class InforExtractedResume(InforExtractedBase):
    project: list[str] = Field(
        default_factory=list,
        description=(
            "Projects or substantial work. Crucial: Each distinct project must be formatted as EXACTLY ONE single complete string "
            "containing its name, tech stack, and description. Do not split a single project into multiple array elements."
        ),
    )


class InforExtractedJD(InforExtractedBase):
    responsibilities: list[str] = Field(
        default_factory=list,
        description=(
            "Duties, tasks, and expected work activities explicitly "
            "stated in the job description."
        ),
    )
