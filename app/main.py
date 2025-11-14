"""FastAPI application for Email Summary SaaS."""

from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict, Field


app = FastAPI(title="Email Summary SaaS")


class Email(BaseModel):
    """Single email representation."""
    model_config = ConfigDict(populate_by_name=True)

    from_: Optional[str] = Field(default=None, alias="from")
    subject: Optional[str] = None
    snippet: Optional[str] = None


class EmailRequest(BaseModel):
    """Request model for email summarization."""
    emails: list[Email]


class SummaryResponse(BaseModel):
    """Response model for email summary."""
    summary: str
    top_actions: list[str]


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Email Summary SaaS API"}


@app.post("/summarize_emails", response_model=SummaryResponse)
async def summarize_emails(request: EmailRequest):
    """
    Summarize emails and extract top actions.

    Currently returns mock data.
    """
    # Mock response
    email_count = len(request.emails)
    subjects = [email.subject for email in request.emails if email.subject]

    summary = f"Otrzymano {email_count} email(i). "
    if subjects:
        summary += f"Tematy obejmują: {', '.join(subjects[:3])}."
    else:
        summary += "Brak szczegółowych tematów."

    top_actions = [
        "Odpowiedz na najważniejsze wiadomości",
        "Przejrzyj załączniki",
        "Zaplanuj follow-up na przyszły tydzień"
    ]

    return SummaryResponse(
        summary=summary,
        top_actions=top_actions
    )
