<!-- # Flask + Gunicorn Portfolio App

Simple Cloud/DevOps portfolio site built with Flask and served via Gunicorn.

## Run locally

```bash
cd portfolio_flask_gunicorn
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
gunicorn --workers 2 --bind 0.0.0.0:8000 app:app
```

Open http://localhost:8000
 
