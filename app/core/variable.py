from enum import Enum

class LLMModel(str, Enum):
    GPT_41_MINI = "gpt-4.1-mini"
    GPT_41 = "gpt-4.1"
    GEMINI_FLASH = "gemini-3.8-flash"
    OLLAMA_MODEL = "qwen2.5:3b"


class Prompt(str, Enum):
    SYSTEM_RULE = """
    You are an accurate information extraction system.
    Rules:
    - Extract ONLY information explicitly stated in the source text.
    - Do not infer, assume, or invent details.
    - Return data strictly matching the requested JSON schema.
    """

    PROMPT_EXTRACT_INFOR_JD = """
    Extract required and preferred qualifications from the Job Description:

    Field Guidelines:
    - skill: Technical, practical, and interpersonal skills (e.g., "Python", "FastAPI").
    - education: Required/preferred degrees, majors, or academic background.
    - experience: Years of experience, job titles, and background required.
    - certificate: Certifications, licenses, or formal credentials requested.
    - responsibilities: Work duties, tasks, and core responsibilities.
    """

    PROMPT_EXTRACT_INFOR_RESUME = """
    Extract candidate information from the Resume into their respective fields:

    Field Guidelines:
    - skill: Individual skills, tools, and technologies explicitly mentioned.
    - education: Degree, major, and school name combined per qualification (e.g., "Bachelor's in SE - Ton Duc Thang University").
    - experience: Full work history entries including role, company, duration, and key accomplishments.
    - certificate: EVERY explicitly earned certification, license, or credential (e.g., "AWS Certified Cloud Practitioner").
    - project: Each project consolidated into a single comprehensive string (Title + Description + Tech stack).

    Extraction Rules:
    - SCAN THE ENTIRE RESUME FROM TOP TO BOTTOM, ensuring no section (especially Certifications/Licenses) is skipped.
    - Keep each distinct project as ONE complete text block in the project array, do not split project details into multiple list items.
    """
