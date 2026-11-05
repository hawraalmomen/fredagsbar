# Fredagsbaren

En simpel fredagsbar-applikation med en Flask API og en Streamlit frontend.

## Start med Docker

Kør følgende kommando fra projektets rodmappe:

```bash
docker compose up
```

## Adresser

- **Frontend (Streamlit):** http://localhost:8501
- **API (Flask):** http://localhost:5001
- **Events endpoint:** http://localhost:5001/events

API'et kan også testes med Postman.

## Stop Docker

Tryk `Ctrl + C` i terminalen, og kør derefter:

```bash
docker compose down
```

## Lokal kørsel uden Docker

API og frontend kan også startes separat på computeren.

Start API'et:

```bash
cd fredagsbar
python api.py
```

Start frontend i en anden terminal:

```bash
cd fredagsbar
streamlit run app.py
```

Frontend bruger som standard API-adressen `http://127.0.0.1:5000`, når den køres lokalt.