# CineReads - Copilot Instructions

This is a full-stack application that provides book recommendations based on favorite movies using AI.

## Project Structure

- **Backend**: FastAPI with Python 3.13 (port 8000)
- **Frontend**: Next.js 15 with React 19 and TypeScript (port 3000)
- **APIs**: OpenAI GPT for recommendations, Hardcover API for book metadata

## Development Commands

### Backend (FastAPI)
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend (Next.js)
```bash
cd frontend  
npm run dev
```

## Environment Setup

1. Backend requires `.env` file with:
   - `OPENAI_API_KEY`
   - `HARDCOVER_API_KEY`
   
2. Python virtual environment is configured at project root (`.venv/`)

## Key Directories

- `backend/app/` - FastAPI application code
- `frontend/src/` - Next.js application code  
- `backend/cache/` - API response caching
- `.venv/` - Python virtual environment

## Troubleshooting

- If file watch limit error occurs, increase system limit with: `echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf && sudo sysctl -p`
- Run uvicorn from `backend/` directory to avoid module import errors
- API documentation available at http://localhost:8000/docs when backend is running
