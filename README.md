# Email Summary SaaS

Minimalny szkielet aplikacji do podsumowywania emaili za pomocą FastAPI.

## Struktura projektu

```
.
├── app/
│   ├── __init__.py
│   └── main.py          # FastAPI aplikacja z endpointem /summarize_emails
├── tests/
│   ├── __init__.py
│   └── test_main.py     # Testy jednostkowe
├── pyproject.toml       # Konfiguracja projektu i zależności
└── README.md
```

## Instalacja

### 1. Stwórz wirtualne środowisko

```bash
python -m venv venv
```

### 2. Aktywuj wirtualne środowisko

**Linux/macOS:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### 3. Zainstaluj zależności

```bash
pip install -e ".[dev]"
```

## Uruchomienie serwera

```bash
uvicorn app.main:app --reload
```

Serwer będzie dostępny pod adresem: http://localhost:8000

### Dokumentacja API

Po uruchomieniu serwera, dokumentacja interaktywna jest dostępna pod:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testowanie

### Uruchom wszystkie testy

```bash
pytest
```

### Uruchom testy z verbose output

```bash
pytest -v
```

### Uruchom konkretny test

```bash
pytest tests/test_main.py::test_summarize_emails_endpoint -v
```

## Przykład użycia API

### Endpoint: POST /summarize_emails

**Request:**
```json
{
  "emails": [
    {
      "from": "john@example.com",
      "subject": "Meeting tomorrow",
      "snippet": "Don't forget about our meeting at 10 AM"
    },
    {
      "from": "jane@example.com",
      "subject": "Project update",
      "snippet": "Here's the latest status on the project"
    }
  ]
}
```

**Response:**
```json
{
  "summary": "Otrzymano 2 email(i). Tematy obejmują: Meeting tomorrow, Project update.",
  "top_actions": [
    "Odpowiedz na najważniejsze wiadomości",
    "Przejrzyj załączniki",
    "Zaplanuj follow-up na przyszły tydzień"
  ]
}
```

### Curl example

```bash
curl -X POST "http://localhost:8000/summarize_emails" \
  -H "Content-Type: application/json" \
  -d '{
    "emails": [
      {
        "from": "test@example.com",
        "subject": "Test",
        "snippet": "This is a test email"
      }
    ]
  }'
```

## Rozwój

Obecnie endpoint `/summarize_emails` zwraca mock dane. W przyszłości można zintegrować:
- AI/LLM do rzeczywistego podsumowywania (np. OpenAI, Anthropic)
- Uwierzytelnianie użytkowników
- Połączenie z dostawcami email (Gmail API, Outlook API)
- Baza danych do przechowywania historii
- Frontend do wizualizacji podsumowań
