# medishop

This repository contains a Django backend and a separate React frontend (in `frontend/`).

Deployment notes
-------------

- Frontend: deploy the `frontend/` folder to Vercel (set `VITE_API_BASE` env var).
- Backend: deploy Django to any host (e.g., Render, Fly, DigitalOcean). Ensure `CORS_ALLOWED_ORIGINS` includes your Vercel domain and configure media/static file hosting.

Quick commands
--------------

Backend dev:
```bash
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Frontend dev:
```bash
cd frontend
npm install
npm run dev
```