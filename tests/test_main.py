"""Tests for the main FastAPI application."""

import pytest
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root_endpoint():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Email Summary SaaS API"}


def test_summarize_emails_endpoint():
    """Test the /summarize_emails endpoint with valid data."""
    payload = {
        "emails": [
            {
                "from": "john@example.com",
                "subject": "Meeting tomorrow",
                "snippet": "Don't forget about our meeting"
            },
            {
                "from": "jane@example.com",
                "subject": "Project update",
                "snippet": "Here's the latest status"
            }
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


def test_summarize_emails_empty_list():
    """Test the endpoint with an empty email list."""
    payload = {"emails": []}

    response = client.post("/summarize_emails", json=payload)

    assert response.status_code == 200

    data = response.json()
    assert "summary" in data
    assert "top_actions" in data


def test_summarize_emails_minimal_data():
    """Test the endpoint with minimal email data."""
    payload = {
        "emails": [
            {"from": "test@example.com"}
        ]
    }

    response = client.post("/summarize_emails", json=payload)

    assert response.status_code == 200

    data = response.json()
    assert "summary" in data
    assert "top_actions" in data
