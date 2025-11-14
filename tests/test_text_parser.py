"""Tests for the text parser module."""

from app.text_parser import parse_raw_text, _parse_structured_emails, _parse_as_paragraphs


class TestParseRawText:
    """Tests for the parse_raw_text function."""

    def test_parse_structured_email(self):
        """Test parsing structured email with headers."""
        text = """From: john@example.com
Subject: Test Subject
This is the email body."""

        result = parse_raw_text(text)

        assert len(result) == 1
        assert result[0]["from"] == "john@example.com"
        assert result[0]["subject"] == "Test Subject"
        assert "email body" in result[0]["snippet"]

    def test_parse_multiple_emails(self):
        """Test parsing multiple emails."""
        text = """From: john@example.com
Subject: First Email
First email body.

From: jane@example.com
Subject: Second Email
Second email body."""

        result = parse_raw_text(text)

        assert len(result) == 2
        assert result[0]["from"] == "john@example.com"
        assert result[1]["from"] == "jane@example.com"

    def test_parse_polish_headers(self):
        """Test parsing emails with Polish headers."""
        text = """Od: jan@example.com
Temat: Testowy email
To jest treść emaila."""

        result = parse_raw_text(text)

        assert len(result) == 1
        assert result[0]["from"] == "jan@example.com"
        assert result[0]["subject"] == "Testowy email"

    def test_parse_mixed_headers(self):
        """Test parsing with mixed English and Polish headers."""
        text = """From: john@example.com
Temat: Mixed email
Body content.

Od: jan@example.com
Subject: Another mixed
More content."""

        result = parse_raw_text(text)

        assert len(result) == 2

    def test_parse_plain_paragraphs(self):
        """Test parsing plain text without headers."""
        text = """This is the first paragraph.
It has multiple lines.

This is the second paragraph.
Also with multiple lines."""

        result = parse_raw_text(text)

        assert len(result) >= 2
        assert result[0]["from"] == "unknown"
        assert "first paragraph" in result[0]["snippet"]

    def test_parse_empty_text(self):
        """Test parsing empty text."""
        result = parse_raw_text("")
        assert result == []

        result = parse_raw_text("   ")
        assert result == []

    def test_parse_single_line(self):
        """Test parsing single line of text."""
        text = "Just a single line of text"

        result = parse_raw_text(text)

        assert len(result) == 1
        assert result[0]["from"] == "unknown"
        assert result[0]["snippet"] == text

    def test_snippet_length_limit(self):
        """Test that snippets are limited in length."""
        long_text = "a" * 1000

        text = f"""From: test@example.com
Subject: Long email
{long_text}"""

        result = parse_raw_text(text)

        assert len(result) == 1
        assert len(result[0]["snippet"]) <= 500

    def test_parse_email_without_subject(self):
        """Test parsing email with only From header."""
        text = """From: john@example.com
This is the email content without a subject line."""

        result = parse_raw_text(text)

        assert len(result) == 1
        assert result[0]["from"] == "john@example.com"
        assert result[0]["subject"] == "(no subject)"
        assert "email content" in result[0]["snippet"]

    def test_parse_email_without_from(self):
        """Test parsing email with only Subject header."""
        text = """Subject: Important notification
This is the notification content."""

        result = parse_raw_text(text)

        assert len(result) == 1
        assert result[0]["from"] == "unknown"
        assert result[0]["subject"] == "Important notification"
