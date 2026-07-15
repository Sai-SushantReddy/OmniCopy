from groq import Groq

from app.core.config import settings

from app.services.platform_service import (
    PLATFORM_INSTRUCTIONS
)


client = Groq(
    api_key=settings.GROQ_API_KEY
)


def generate_platform_content(
    source_title: str,
    source_content: str,
    platform: str,
    tone: str
) -> str:

    platform_instruction = PLATFORM_INSTRUCTIONS[
        platform
    ]

    system_prompt = """
You are OmniCopy, an AI content repurposing assistant.

Your job is to transform source content into content designed
for a specific publishing platform.

Preserve the meaning and factual claims of the source material.

Never invent statistics, quotes, events, or claims that are not
present in the source content.

Return only the final generated content.
"""

    user_prompt = f"""
SOURCE TITLE:
{source_title}

SOURCE CONTENT:
{source_content}

TARGET PLATFORM:
{platform}

REQUESTED TONE:
{tone}

PLATFORM REQUIREMENTS:
{platform_instruction}

Transform the source content for the target platform.
"""

    completion = client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        temperature=0.7
    )

    generated_content = (
        completion
        .choices[0]
        .message
        .content
    )

    if not generated_content:

        raise ValueError(
            "LLM returned empty content"
        )

    return generated_content.strip()