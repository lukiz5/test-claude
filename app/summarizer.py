"""Email summarization using Anthropic Claude API."""

import os
from typing import Any

from anthropic import Anthropic


def summarize_emails(emails: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Summarize a list of emails using Claude 3.5 Sonnet.

    Args:
        emails: List of email dictionaries with keys 'from', 'subject', 'snippet'

    Returns:
        Dictionary with 'summary' and 'top_actions' keys

    Raises:
        ValueError: If ANTHROPIC_API_KEY environment variable is not set
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError(
            "ANTHROPIC_API_KEY environment variable is not set. "
            "Please set it with your Anthropic API key."
        )

    # Prepare email text for Claude
    email_text = _format_emails_for_prompt(emails)

    # Call Anthropic API
    client = Anthropic(api_key=api_key)

    prompt = f"""Przeanalizuj poniższą listę emaili i wykonaj dwa zadania:

1. Napisz krótkie streszczenie całej skrzynki odbiorczej (maksymalnie ~150 słów)
2. Wypisz 3-5 najważniejszych zadań do wykonania na podstawie tych emaili

Emaile:
{email_text}

Zwróć odpowiedź w formacie JSON:
{{
  "summary": "krótkie streszczenie...",
  "top_actions": ["zadanie 1", "zadanie 2", "zadanie 3"]
}}"""

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )

    # Parse response
    response_text = message.content[0].text

    # Extract JSON from response (Claude sometimes wraps it in markdown)
    import json
    import re

    # Try to find JSON in the response
    json_match = re.search(r"\{[\s\S]*\}", response_text)
    if json_match:
        result = json.loads(json_match.group())
    else:
        # Fallback: assume the entire response is JSON
        result = json.loads(response_text)

    return result


def _format_emails_for_prompt(emails: list[dict[str, Any]]) -> str:
    """Format emails into a readable text for the prompt."""
    if not emails:
        return "Brak emaili."

    formatted = []
    for i, email in enumerate(emails, 1):
        from_addr = email.get("from", "Nieznany")
        subject = email.get("subject", "Brak tematu")
        snippet = email.get("snippet", "")

        formatted.append(f"""Email {i}:
Od: {from_addr}
Temat: {subject}
Treść: {snippet}
""")

    return "\n".join(formatted)
