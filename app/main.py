"""FastAPI application."""

from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.summarizer import summarize_emails
from app.text_parser import parse_raw_text


app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


class RawTextRequest(BaseModel):
    """Request model for raw text input."""
    text: str


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


@app.post("/summarize_raw", response_model=SummaryResponse)
async def summarize_raw_endpoint(request: RawTextRequest):
    """
    Summarize emails from raw plain text.

    Accepts plain text copied from email apps and parses it into emails.
    Returns a summary with top actions.
    Requires ANTHROPIC_API_KEY environment variable to be set.
    """
    try:
        # Parse raw text into emails
        emails_data = parse_raw_text(request.text)

        # Call summarizer
        result = summarize_emails(emails_data)

        return SummaryResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error summarizing emails: {str(e)}"
        )
