"""Parser for raw text email input."""

import re
from typing import Any


def parse_raw_text(text: str) -> list[dict[str, Any]]:
    """
    Parse raw plain text into a list of email-like structures.

    Args:
        text: Raw plain text (copied from email apps, notes, etc.)

    Returns:
        List of email dictionaries with keys 'from', 'subject', 'snippet'
    """
    if not text or not text.strip():
        return []

    # Try to parse as structured emails with headers
    structured_emails = _parse_structured_emails(text)
    if structured_emails:
        return structured_emails

    # Fallback: split by paragraphs
    return _parse_as_paragraphs(text)


def _parse_structured_emails(text: str) -> list[dict[str, Any]]:
    """
    Try to parse text as structured emails with headers.

    Looks for patterns like:
    - From: / Od:
    - Subject: / Temat:
    """
    emails = []

    # Pattern to detect email blocks
    # Matches lines starting with "From:", "Od:", "Subject:", "Temat:"
    header_pattern = r'(?:^|\n)((?:From|Od|Subject|Temat):\s*.+?)(?=\n(?:From|Od|Subject|Temat):|$)'

    # Split text into potential email blocks
    # Look for blocks that start with From/Od
    email_blocks = re.split(
        r'\n(?=(?:From|Od):\s*)',
        text,
        flags=re.IGNORECASE | re.MULTILINE
    )

    for block in email_blocks:
        if not block.strip():
            continue

        email_dict = _extract_email_from_block(block)
        if email_dict:
            emails.append(email_dict)

    return emails


def _extract_email_from_block(block: str) -> dict[str, Any] | None:
    """Extract email fields from a text block."""
    from_match = re.search(
        r'(?:From|Od):\s*(.+?)(?:\n|$)',
        block,
        re.IGNORECASE | re.MULTILINE
    )
    subject_match = re.search(
        r'(?:Subject|Temat):\s*(.+?)(?:\n|$)',
        block,
        re.IGNORECASE | re.MULTILINE
    )

    # Extract the body/snippet (everything after headers)
    snippet_text = block
    if from_match or subject_match:
        # Remove header lines to get the body
        snippet_text = re.sub(
            r'(?:From|Od|Subject|Temat):\s*.+?\n',
            '',
            block,
            flags=re.IGNORECASE | re.MULTILINE
        )

    from_addr = from_match.group(1).strip() if from_match else "unknown"
    subject = subject_match.group(1).strip() if subject_match else "(no subject)"
    snippet = snippet_text.strip()[:500] if snippet_text.strip() else ""

    # Only return if we have at least a from or subject, or some content
    if from_match or subject_match or snippet:
        return {
            "from": from_addr,
            "subject": subject,
            "snippet": snippet
        }

    return None


def _parse_as_paragraphs(text: str) -> list[dict[str, Any]]:
    """
    Parse text as simple paragraphs when no structure is detected.

    Each paragraph becomes a separate "email" with default fields.
    """
    emails = []

    # Split by double newlines or multiple newlines
    paragraphs = re.split(r'\n\s*\n', text)

    for i, para in enumerate(paragraphs, 1):
        para = para.strip()
        if not para:
            continue

        # Try to extract a subject from the first line if it's short
        lines = para.split('\n')
        if lines:
            first_line = lines[0].strip()
            # If first line is short (< 80 chars), use it as subject
            if len(first_line) < 80 and len(lines) > 1:
                subject = first_line
                snippet = '\n'.join(lines[1:]).strip()
            else:
                subject = f"Message {i}"
                snippet = para

            emails.append({
                "from": "unknown",
                "subject": subject,
                "snippet": snippet[:500]  # Limit snippet length
            })

    # If no paragraphs found, treat entire text as one message
    if not emails and text.strip():
        emails.append({
            "from": "unknown",
            "subject": "(no subject)",
            "snippet": text.strip()[:500]
        })

    return emails
