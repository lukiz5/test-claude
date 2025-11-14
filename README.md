# test-claude

Minimalny szkielet backendu w FastAPI.

## Struktura projektu

```
.
├── app/
│   ├── __init__.py
│   └── main.py          # FastAPI aplikacja
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
pip install -e .
```

## Uruchomienie lokalnie

```bash
uvicorn app.main:app --reload
```

Serwer będzie dostępny pod adresem: http://localhost:8000

### Dokumentacja API

Po uruchomieniu serwera, dokumentacja interaktywna jest dostępna pod:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpoint

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "ok"
}
```
