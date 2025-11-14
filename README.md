# test-claude

Backend w FastAPI do podsumowywania emaili przy użyciu Anthropic Claude API.

## Struktura projektu

```
.
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI aplikacja
│   └── summarizer.py    # Logika podsumowywania emaili
├── tests/
│   ├── __init__.py
│   ├── test_main.py
│   └── test_summarizer.py
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

### 4. Ustaw klucz API Anthropic

Aby korzystać z endpointu `/summarize_emails`, musisz ustawić zmienną środowiskową `ANTHROPIC_API_KEY`.

**Linux/macOS:**
```bash
export ANTHROPIC_API_KEY="twój-klucz-api"
```

**Windows (PowerShell):**
```powershell
$env:ANTHROPIC_API_KEY="twój-klucz-api"
```

**Windows (CMD):**
```cmd
set ANTHROPIC_API_KEY=twój-klucz-api
```

Możesz też stworzyć plik `.env` w głównym katalogu projektu:
```
ANTHROPIC_API_KEY=twój-klucz-api
```

Klucz API możesz uzyskać na: https://console.anthropic.com/

## Uruchomienie lokalnie

```bash
uvicorn app.main:app --reload
```

Serwer będzie dostępny pod adresem: http://localhost:8000

### Dokumentacja API

Po uruchomieniu serwera, dokumentacja interaktywna jest dostępna pod:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpointy

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "ok"
}
```

### POST /summarize_emails

Podsumowuje listę emaili przy użyciu Claude 3.5 Sonnet.

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
  "summary": "Otrzymano 2 emaile dotyczące nadchodzącego spotkania oraz aktualizacji projektu. Spotkanie zaplanowane jest na jutro o godzinie 10:00.",
  "top_actions": [
    "Potwierdź obecność na spotkaniu o 10:00",
    "Przejrzyj aktualizację statusu projektu",
    "Przygotuj materiały na spotkanie"
  ]
}
```

**Curl example:**
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

## Testowanie

### Uruchom wszystkie testy

```bash
pytest
```

### Uruchom testy z verbose output

```bash
pytest -v
```

### Uruchom konkretny plik testów

```bash
pytest tests/test_summarizer.py -v
```
