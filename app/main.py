"""FastAPI application."""

from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.summarizer import summarize_emails


app = FastAPI()


class Email(BaseModel):
    """Single email representation."""
    model_config = {"populate_by_name": True}

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


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok"}


@app.post("/summarize_emails", response_model=SummaryResponse)
async def summarize_emails_endpoint(request: EmailRequest):
    """
    Summarize emails using Claude 3.5 Sonnet.

    Accepts a list of emails and returns a summary with top actions.
    Requires ANTHROPIC_API_KEY environment variable to be set.
    """
    try:
        # Convert Pydantic models to dicts
        emails_data = [email.model_dump(by_alias=True) for email in request.emails]

        # Call summarizer
        result = summarize_emails(emails_data)

        return SummaryResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error summarizing emails: {str(e)}"
        )
