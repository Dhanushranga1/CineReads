# CineReads

CineReads is a full-stack application that provides book recommendations based on your favorite movies. The app uses AI to suggest books that match the themes, genres, and storytelling styles of movies you love.

## 🏗️ Architecture

- **Frontend**: Next.js 15 with React 19, TypeScript, and Tailwind CSS
- **Backend**: FastAPI with Python 3.13, OpenAI API integration
- **APIs**: OpenAI GPT for recommendations, Hardcover API for book metadata

## 🚀 Getting Started

### Prerequisites

- Node.js 18+ and npm
- Python 3.13+
- OpenAI API key
- Hardcover API key (optional but recommended)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Dhanushranga1/CineReads.git
   cd CineReads
   ```

2. **Set up the backend:**
   ```bash
   # Create Python virtual environment and install dependencies
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r backend/requirements.txt
   
   # Configure environment variables
   cp backend/.env.example backend/.env
   # Edit backend/.env and add your API keys
   ```

3. **Set up the frontend:**
   ```bash
   cd frontend
   npm install
   ```

### Running the Application

1. **Start the backend API:**
   ```bash
   cd backend
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
   The API will be available at http://localhost:8000

2. **Start the frontend development server:**
   ```bash
   cd frontend
   npm run dev
   ```
   The web app will be available at http://localhost:3000

### Environment Variables

Create a `.env` file in the `backend/` directory with:

```env
# Required
OPENAI_API_KEY=your_openai_api_key_here
HARDCOVER_API_KEY=your_hardcover_api_key_here

# Optional (with defaults)
CACHE_DIR=cache
CACHE_EXPIRE_SECONDS=3600
BOOK_CACHE_EXPIRE_SECONDS=86400
MAX_MOVIES_PER_REQUEST=5
GPT_MAX_TOKENS=800
GPT_TEMPERATURE=0.7
DEBUG=false
```

## 📁 Project Structure

```
CineReads/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── main.py         # FastAPI application entry point
│   │   ├── routers/        # API route handlers
│   │   ├── services/       # Business logic services
│   │   ├── models/         # Pydantic models
│   │   └── utils/          # Utility functions
│   ├── requirements.txt    # Python dependencies
│   └── .env               # Environment variables
├── frontend/               # Next.js frontend
│   ├── src/
│   │   ├── app/           # Next.js app router
│   │   ├── components/    # React components
│   │   └── lib/          # Utility libraries
│   ├── package.json      # Node.js dependencies
│   └── tailwind.config.ts # Tailwind CSS configuration
└── README.md
```

## 🛠️ Development

### Backend Development

- The backend uses FastAPI with automatic API documentation available at http://localhost:8000/docs
- Environment variables are managed with Pydantic Settings
- Book metadata is cached to improve performance
- Rate limiting and error handling are implemented

### Frontend Development

- Built with Next.js 15 App Router and React 19
- Styled with Tailwind CSS and Radix UI components
- Uses TypeScript for type safety
- Responsive design with mobile-first approach

## 🚀 Deployment

### Backend Deployment (Render)

See `backend/RENDER_DEPLOYMENT_GUIDE.md` for detailed instructions.

### Frontend Deployment (Vercel)

See `frontend/VERCEL_DEPLOYMENT.md` for detailed instructions.

## 📝 API Documentation

Once the backend is running, visit http://localhost:8000/docs for interactive API documentation.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🔧 Troubleshooting

### Common Issues

1. **File watch limit error**: Increase your system's file watch limit:
   ```bash
   echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf && sudo sysctl -p
   ```

2. **ModuleNotFoundError**: Ensure you're running uvicorn from the backend directory:
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```

3. **API key errors**: Make sure your `.env` file is in the `backend/` directory with valid API keys.

## ✨ Features

- 🎬 Movie-based book recommendations using AI
- 📚 Rich book metadata integration
- 🎨 Beautiful, responsive UI
- ⚡ Fast caching system
- 🔍 Advanced search and filtering
- 📱 Mobile-friendly design