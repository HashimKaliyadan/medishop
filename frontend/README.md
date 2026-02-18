# Medishop Frontend (React + Vite)

Quick start:

```bash
cd frontend
npm install
npm run dev
```

Build:

```bash
npm run build
npm run preview
```

Next steps:
- Convert Django templates in `templates/` into React components.
- Implement API calls to Django backend (use Django REST Framework).
- Configure environment variables for API base URL.

Environment:
- Copy `.env.example` to `.env` and set `VITE_API_BASE` to your backend API base URL, e.g. `https://api.example.com/api`.

Development notes:
- Frontend expects the API at `VITE_API_BASE` and uses `credentials: 'include'` for cookie-based auth.
- To deploy on Vercel: set the `VITE_API_BASE` environment variable in the Vercel project settings and deploy the `frontend/` folder.

Vercel deployment (quick):

1. Push repo to GitHub.
2. In Vercel, create a new project and point to the `frontend` folder.
3. Set environment variable `VITE_API_BASE` to your backend API endpoint.
4. Deploy.

If your backend uses session authentication, host the backend on HTTPS and add the frontend origin to `CORS_ALLOWED_ORIGINS` in Django settings.
