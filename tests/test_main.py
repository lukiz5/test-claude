"""Tests for the main FastAPI application."""

import json
import os
from unittest.mock import Mock, patch

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-api-key"})
@patch("app.summarizer.Anthropic")
def test_summarize_emails_endpoint(mock_anthropic):
    """Test the /summarize_emails endpoint with mocked API."""
    # Mock the Anthropic API response
    mock_client = Mock()
    mock_anthropic.return_value = mock_client

    mock_message = Mock()
    mock_message.content = [
        Mock(
            text=json.dumps(
                {
                    "summary": "Testowe podsumowanie dwóch emaili",
                    "top_actions": ["Akcja 1", "Akcja 2", "Akcja 3"],
                }
            )
        )
    ]
    mock_client.messages.create.return_value = mock_message

    # Test request
    payload = {
        "emails": [
            {
                "from": "john@example.com",
                "subject": "Meeting tomorrow",
                "snippet": "Don't forget about our meeting",
            },
            {
                "from": "jane@example.com",
                "subject": "Project update",
                "snippet": "Here's the latest status",
            },
        ]
    }

    response = client.post("/summarize_emails", json=payload)

    assert response.status_code == 200

    data = response.json()
    assert "summary" in data
    assert "top_actions" in data

    # Check types
    assert isinstance(data["summary"], str)
    assert isinstance(data["top_actions"], list)

    # Check that summary is not empty
    assert len(data["summary"]) > 0

    # Check that we have at least one action
    assert len(data["top_actions"]) > 0


@patch.dict(os.environ, {}, clear=True)
def test_summarize_emails_endpoint_without_api_key():
    """Test that endpoint returns 500 when API key is not set."""
    payload = {"emails": [{"from": "test@example.com", "subject": "Test"}]}

    response = client.post("/summarize_emails", json=payload)

    assert response.status_code == 500
    assert "ANTHROPIC_API_KEY" in response.json()["detail"]
