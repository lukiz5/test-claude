"""Tests for the email summarizer module."""

import json
import os
from unittest.mock import Mock, patch

import pytest

from app.summarizer import summarize_emails, _format_emails_for_prompt


class TestSummarizeEmails:
    """Tests for the summarize_emails function."""

    @patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-api-key"})
    @patch("app.summarizer.Anthropic")
    def test_summarize_emails_returns_summary_and_actions(self, mock_anthropic):
        """Test that summarize_emails returns summary and top_actions."""
        # Mock the Anthropic API response
        mock_client = Mock()
        mock_anthropic.return_value = mock_client

        mock_message = Mock()
        mock_message.content = [
            Mock(
                text=json.dumps(
                    {
                        "summary": "Testowe podsumowanie emaili",
                        "top_actions": ["Akcja 1", "Akcja 2", "Akcja 3"],
                    }
                )
            )
        ]
        mock_client.messages.create.return_value = mock_message

        # Test data
        emails = [
            {
                "from": "test@example.com",
                "subject": "Test Subject",
                "snippet": "Test content",
            }
        ]

        # Call function
        result = summarize_emails(emails)

        # Assertions
        assert "summary" in result
        assert "top_actions" in result
        assert isinstance(result["summary"], str)
        assert isinstance(result["top_actions"], list)
        assert len(result["summary"]) > 0
        assert len(result["top_actions"]) > 0

        # Verify API was called correctly
        mock_client.messages.create.assert_called_once()
        call_args = mock_client.messages.create.call_args
        assert call_args.kwargs["model"] == "claude-3-5-sonnet-20241022"
        assert call_args.kwargs["max_tokens"] == 1024

    @patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-api-key"})
    @patch("app.summarizer.Anthropic")
    def test_summarize_emails_with_multiple_emails(self, mock_anthropic):
        """Test summarization with multiple emails."""
        # Mock the Anthropic API response
        mock_client = Mock()
        mock_anthropic.return_value = mock_client

        mock_message = Mock()
        mock_message.content = [
            Mock(
                text=json.dumps(
                    {
                        "summary": "Otrzymano 3 emaile dotyczące różnych tematów",
                        "top_actions": [
                            "Odpowiedz na email od managera",
                            "Przejrzyj raport sprzedażowy",
                            "Zaplanuj spotkanie zespołowe",
                        ],
                    }
                )
            )
        ]
        mock_client.messages.create.return_value = mock_message

        # Test data with multiple emails
        emails = [
            {
                "from": "manager@example.com",
                "subject": "Urgent: Project Update",
                "snippet": "We need to discuss the project timeline",
            },
            {
                "from": "sales@example.com",
                "subject": "Sales Report Q4",
                "snippet": "Please review the attached sales report",
            },
            {
                "from": "team@example.com",
                "subject": "Team Meeting",
                "snippet": "Let's schedule our weekly sync",
            },
        ]

        # Call function
        result = summarize_emails(emails)

        # Assertions
        assert "summary" in result
        assert "top_actions" in result
        assert len(result["top_actions"]) == 3

    @patch.dict(os.environ, {}, clear=True)
    def test_summarize_emails_raises_error_without_api_key(self):
        """Test that function raises ValueError when API key is not set."""
        emails = [{"from": "test@example.com", "subject": "Test", "snippet": "Test"}]

        with pytest.raises(ValueError) as exc_info:
            summarize_emails(emails)

        assert "ANTHROPIC_API_KEY" in str(exc_info.value)

    @patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-api-key"})
    @patch("app.summarizer.Anthropic")
    def test_summarize_emails_handles_json_in_markdown(self, mock_anthropic):
        """Test that function can extract JSON from markdown code blocks."""
        # Mock the Anthropic API response with JSON in markdown
        mock_client = Mock()
        mock_anthropic.return_value = mock_client

        mock_message = Mock()
        mock_message.content = [
            Mock(
                text='```json\n{"summary": "Test summary", "top_actions": ["Action 1"]}\n```'
            )
        ]
        mock_client.messages.create.return_value = mock_message

        emails = [{"from": "test@example.com", "subject": "Test", "snippet": "Test"}]

        result = summarize_emails(emails)

        assert result["summary"] == "Test summary"
        assert result["top_actions"] == ["Action 1"]

    def test_format_emails_for_prompt_empty_list(self):
        """Test formatting empty email list."""
        result = _format_emails_for_prompt([])
        assert result == "Brak emaili."

    def test_format_emails_for_prompt_single_email(self):
        """Test formatting single email."""
        emails = [
            {
                "from": "sender@example.com",
                "subject": "Important Update",
                "snippet": "Please review this update",
            }
        ]

        result = _format_emails_for_prompt(emails)

        assert "Email 1:" in result
        assert "sender@example.com" in result
        assert "Important Update" in result
        assert "Please review this update" in result

    def test_format_emails_for_prompt_multiple_emails(self):
        """Test formatting multiple emails."""
        emails = [
            {"from": "sender1@example.com", "subject": "Subject 1", "snippet": "Text 1"},
            {"from": "sender2@example.com", "subject": "Subject 2", "snippet": "Text 2"},
        ]

        result = _format_emails_for_prompt(emails)

        assert "Email 1:" in result
        assert "Email 2:" in result
        assert "sender1@example.com" in result
        assert "sender2@example.com" in result

    def test_format_emails_for_prompt_missing_fields(self):
        """Test formatting emails with missing fields."""
        emails = [{"snippet": "Only snippet provided"}]

        result = _format_emails_for_prompt(emails)

        assert "Nieznany" in result  # Default for missing 'from'
        assert "Brak tematu" in result  # Default for missing 'subject'
        assert "Only snippet provided" in result
