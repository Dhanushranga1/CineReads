
# CineReads - Overview & Architecture

## Navigation
- **Current**: 01-overview-and-architecture.md
- **Next**: [02-technical-implementation.md](./02-technical-implementation.md)
- **Related**: [03-apis-and-data-flow.md](./03-apis-and-data-flow.md) | [04-code-quality-and-gaps.md](./04-code-quality-and-gaps.md)

---

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Quick Start Guide](#quick-start-guide)
3. [System Architecture](#system-architecture)
4. [Technology Stack](#technology-stack)  
5. [Directory Structure](#directory-structure)
6. [Design Patterns & Principles](#design-patterns--principles)
7. [Configuration & Environment](#configuration--environment)
8. [Deployment Architecture](#deployment-architecture)

---

## Executive Summary

**CineReads** is a full-stack AI-powered application that provides personalized book recommendations based on users' favorite movies. The system analyzes movie preferences to understand users' taste profiles and suggests books that match their storytelling preferences, themes, and narrative styles.

### Core Value Proposition
- **Input**: User provides 1-5 favorite movies with optional preferences (mood, pace, genre)
- **Processing**: AI analyzes movie themes, narrative styles, and emotional tones to create a unified taste profile
- **Output**: Curated book recommendations with cover images, ratings, and detailed explanations for why each book matches their taste

### Key Features
- ✅ **AI-Powered Analysis**: Uses OpenAI GPT (or Groq) to analyze movie preferences and generate sophisticated taste profiles
- ✅ **Rich Book Metadata**: Integrates with Hardcover API for book covers, ratings, descriptions, and publication details
- ✅ **Movie Database Integration**: TMDB integration for movie poster display and metadata
- ✅ **Intelligent Caching**: Multi-tier caching system for recommendations and book metadata
- ✅ **Responsive UI**: Modern React-based interface with cinematic design elements
- ✅ **Unified Taste Analysis**: Analyzes overall taste patterns rather than individual movie-to-book mappings

---

## Quick Start Guide

### Prerequisites
- **Node.js 18+** and npm
- **Python 3.13+** 
- **OpenAI API key** or **Groq API key**
- **Hardcover API key** (optional but recommended for book metadata)
- **TMDB API key** (optional, for movie poster display)

### Installation Steps

1. **Clone and Setup**
   ```bash
   git clone https://github.com/Dhanushranga1/CineReads.git
   cd CineReads
   ```

2. **Backend Setup**
   ```bash
   # Create Python virtual environment
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   
   # Install Python dependencies
   pip install -r backend/requirements.txt
   
   # Configure environment
   cp backend/.env.example backend/.env
   # Edit backend/.env with your API keys
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   ```

4. **Start the Application**
   ```bash
   # Terminal 1: Start Backend (from project root)
   cd backend
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   
   # Terminal 2: Start Frontend (from project root)
   cd frontend
   npm run dev
   ```

5. **Access the Application**
   - Frontend: http://localhost:3000 (or 3001 if 3000 is in use)
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

---

## System Architecture

### High-Level Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │  External APIs  │
│   (Next.js)     │◄──►│   (FastAPI)     │◄──►│                 │
│                 │    │                 │    │ • OpenAI/Groq   │
│ • React 19      │    │ • Python 3.13   │    │ • Hardcover     │
│ • TypeScript    │    │ • Async/Await   │    │ • TMDB          │
│ • Tailwind CSS  │    │ • Pydantic      │    │                 │
│ • Framer Motion │    │ • CORS Enabled  │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │  File System    │
                       │  Cache Storage  │
                       │                 │
                       │ • Recommendations│
                       │ • Book Metadata │
                       │ • Taste Profiles │
                       └─────────────────┘
```

### Component Relationships

#### Frontend Architecture
```
src/
├── app/                    # Next.js App Router
│   ├── layout.tsx         # Root layout with theme system
│   └── page.tsx           # Main application page
├── components/            # React components
│   ├── ui/               # Base UI components (Button, Card, Input)
│   ├── cinematic/        # Cinematic design components
│   ├── MovieInput.tsx    # Movie selection interface
│   ├── PreferencesPanel.tsx # User preference configuration
│   ├── RecommendationResult.tsx # Results display
│   └── BookCard.tsx      # Individual book display
├── service/              # API communication
│   ├── api.ts           # Backend API client
│   └── tmdb.ts          # TMDB API integration
├── types/               # TypeScript definitions
└── lib/                 # Utilities and helpers
```

#### Backend Architecture
```
app/
├── main.py              # FastAPI application entry point
├── config.py            # Configuration management
├── models/              # Pydantic data models
│   ├── request_models.py   # API request schemas
│   └── response_models.py  # API response schemas
├── routers/             # API route handlers
│   └── recommendations.py  # Main recommendation endpoints
├── services/            # Business logic services
│   ├── gpt_service.py      # AI/GPT integration
│   ├── hardcover_service.py # Book metadata service
│   └── cache_service.py    # Caching implementation
└── utils/               # Helper functions
```

### Data Flow Architecture

1. **User Input Flow**
   ```
   User → MovieInput → API Request → GPT Analysis → Book Recommendations
   ```

2. **Recommendation Generation Flow**
   ```
   Movies + Preferences → Cache Check → GPT Service → Hardcover Enhancement → Response
   ```

3. **Caching Strategy**
   ```
   Request → Cache Key Generation → File System Check → API Call (if miss) → Cache Store
   ```

---

## Technology Stack

### Frontend Stack
| Technology | Version | Purpose | Configuration |
|------------|---------|---------|---------------|
| **Next.js** | 15.4.1 | React framework with App Router | `next.config.ts` |
| **React** | 19.1.0 | UI library with latest features | JSX/TSX components |
| **TypeScript** | ^5.0 | Type safety and development experience | `tsconfig.json` |
| **Tailwind CSS** | ^4.0 | Utility-first styling framework | `tailwind.config.ts` |
| **Framer Motion** | ^12.23.6 | Animation and micro-interactions | Component-level animations |
| **Lucide React** | ^0.525.0 | Modern icon library | SVG-based icons |
| **Radix UI** | Multiple | Headless UI components | Accessible primitives |

### Backend Stack
| Technology | Version | Purpose | Configuration |
|------------|---------|---------|---------------|
| **FastAPI** | 0.115.4 | High-performance async Python web framework | `app/main.py` |
| **Python** | 3.13+ | Programming language | `runtime.txt` |
| **Uvicorn** | 0.32.1 | ASGI server with auto-reload | Development server |
| **Pydantic** | 2.10.3 | Data validation and serialization | Model definitions |
| **OpenAI** | 1.55.3 | AI model integration (GPT) | Async client |
| **HTTPX** | 0.28.1 | Async HTTP client for external APIs | Service integrations |
| **Aiofiles** | 24.1.0 | Async file operations for caching | Cache management |

### External Service Integrations
| Service | Purpose | Authentication | Rate Limits |
|---------|---------|----------------|-------------|
| **OpenAI/Groq** | AI-powered recommendation generation | API Key (Bearer) | Varies by provider |
| **Hardcover API** | Book metadata, covers, ratings | JWT Token (Bearer) | 60 requests/minute |
| **TMDB API** | Movie posters and metadata | API Key | 40 requests/10 seconds |

### Development Tools
| Tool | Purpose | Configuration |
|------|---------|---------------|
| **ESLint** | Code linting for frontend | `eslint.config.mjs` |
| **PostCSS** | CSS processing | `postcss.config.mjs` |
| **Pytest** | Python testing framework | Optional |
| **Black** | Python code formatting | Optional |

---

## Directory Structure

### Root Level Structure
```
CineReads-latest/
├── .github/
│   └── copilot-instructions.md    # GitHub Copilot configuration
├── .gitignore                     # Git ignore rules
├── README.md                      # Project documentation
├── backend/                       # Python FastAPI backend
├── frontend/                      # Next.js React frontend
├── documentation/                 # Comprehensive documentation (this folder)
└── .venv/                        # Python virtual environment
```

### Backend Directory (`backend/`)
```
backend/
├── app/                          # Main application code
│   ├── __init__.py              # Package initialization
│   ├── main.py                  # FastAPI app entry point (144 lines)
│   ├── config.py                # Configuration settings (53 lines)
│   ├── models/                  # Pydantic data models
│   │   ├── __init__.py
│   │   ├── request_models.py    # API request schemas
│   │   └── response_models.py   # API response schemas (54 lines)
│   ├── routers/                 # API route handlers
│   │   ├── __init__.py
│   │   └── recommendations.py   # Main API endpoints (401 lines)
│   ├── services/                # Business logic services
│   │   ├── __init__.py
│   │   ├── gpt_service.py       # AI integration (351 lines)
│   │   ├── hardcover_service.py # Book metadata service (596 lines)
│   │   └── cache_service.py     # Caching implementation
│   └── utils/                   # Helper functions
│       ├── __init__.py
│       └── helpers.py
├── cache/                       # File-based cache storage
│   ├── recommendations/         # Cached recommendation responses
│   └── books/                  # Cached book metadata
├── .env                        # Environment variables (excluded from git)
├── .env.example               # Environment template
├── .gitignore                 # Backend-specific git ignores
├── requirements.txt           # Python dependencies
├── runtime.txt               # Python version specification
├── Procfile                  # Process configuration for deployment
├── render.yaml              # Render.com deployment config
├── health_check.py          # Health monitoring script
├── test_hardcover.py        # Hardcover API testing script
├── ENV_SETUP.md            # Environment setup guide
├── KEEP_ALIVE_SETUP.md     # Keep-alive configuration
└── RENDER_DEPLOYMENT_GUIDE.md # Deployment documentation
```

### Frontend Directory (`frontend/`)
```
frontend/
├── src/                         # Source code
│   ├── app/                    # Next.js App Router
│   │   ├── layout.tsx          # Root layout (applies to all pages)
│   │   ├── page.tsx            # Home page component (278 lines)
│   │   ├── globals.css         # Global styles
│   │   ├── globals-old.css     # Legacy styles
│   │   ├── globals-new.css     # Updated styles
│   │   └── favicon.ico         # Site icon
│   ├── components/             # React components
│   │   ├── ui/                # Base UI components (shadcn/ui)
│   │   │   ├── button.tsx      # Button component
│   │   │   ├── card.tsx        # Card component
│   │   │   ├── input.tsx       # Input component
│   │   │   └── textarea.tsx    # Textarea component
│   │   ├── cinematic/         # Cinematic design system
│   │   │   ├── index.ts        # Component exports
│   │   │   ├── AnimatedText.tsx     # Text animations
│   │   │   ├── CinematicBackground.tsx # Dynamic backgrounds
│   │   │   ├── CinematicButton.tsx  # Styled buttons
│   │   │   ├── FloatingParticles.tsx # Particle effects
│   │   │   ├── GlassPanel.tsx       # Glass morphism panels
│   │   │   └── SparkleEffect.tsx    # Sparkle animations
│   │   ├── BookCard.tsx        # Individual book display (156 lines)
│   │   ├── ErrorMessage.tsx    # Error state display
│   │   ├── MovieInput.tsx      # Movie selection interface
│   │   ├── PreferencesPanel.tsx # User preferences
│   │   ├── RecommendationResult.tsx # Results display (77 lines)
│   │   ├── ThemeSelector.tsx   # Theme switching
│   │   ├── ThemeTransition.tsx # Theme transition effects
│   │   └── index.ts           # Component exports
│   ├── service/               # API integration
│   │   ├── api.ts            # Backend API client (103 lines)
│   │   └── tmdb.ts           # TMDB API integration
│   ├── lib/                  # Utilities and helpers
│   │   ├── api.ts           # API utilities
│   │   ├── themes.ts        # Theme configuration
│   │   └── utils.ts         # General utilities
│   └── types/               # TypeScript type definitions
│       └── index.ts         # Application types (70+ interfaces)
├── public/                   # Static assets
│   ├── next.svg            # Next.js logo
│   ├── vercel.svg          # Vercel logo
│   ├── file.svg            # File icon
│   ├── globe.svg           # Globe icon
│   └── window.svg          # Window icon
├── .gitignore              # Frontend git ignores
├── .eslintrc.json          # ESLint configuration
├── components.json         # shadcn/ui configuration
├── eslint.config.mjs      # ESLint configuration
├── next.config.ts         # Next.js configuration
├── package.json           # Dependencies and scripts
├── package-lock.json      # Dependency lock file
├── postcss.config.mjs     # PostCSS configuration
├── tailwind.config.ts     # Tailwind CSS configuration
├── tsconfig.json          # TypeScript configuration
├── ENV_SETUP.md          # Environment setup guide
├── README.md             # Frontend documentation
└── VERCEL_DEPLOYMENT.md  # Vercel deployment guide
```

---

## Design Patterns & Principles

### Architectural Patterns

#### 1. **Separation of Concerns**
- **Frontend**: Presentation layer with React components
- **Backend**: Business logic with FastAPI services  
- **External APIs**: Data sources (OpenAI, Hardcover, TMDB)
- **Caching**: Performance optimization layer

#### 2. **Service-Oriented Architecture (SOA)**
```python
# Backend services are isolated and focused
- GPTService: AI recommendation generation
- HardcoverService: Book metadata enrichment  
- CacheService: Performance optimization
```

#### 3. **Repository Pattern** (Implicit)
```python
# Each service acts as a repository for its domain
class GPTService:
    async def generate_recommendations(...)
    
class HardcoverService:
    async def get_book_metadata(...)
```

#### 4. **Factory Pattern**
```typescript
// Frontend API client factory
export class CineReadsAPI {
    constructor(baseURL: string = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000')
}
```

### Design Principles

#### 1. **Single Responsibility Principle**
- Each component/service has one clear purpose
- `BookCard.tsx`: Only displays book information
- `GPTService`: Only handles AI communication
- `CacheService`: Only manages caching operations

#### 2. **Dependency Injection**
```python
# Services are injected at router level
gpt_service = GPTService()
hardcover_service = HardcoverService()
cache_service = CacheService(cache_dir=settings.cache_dir)
```

#### 3. **Configuration Over Convention**
```python
# Extensive configuration options in config.py
class Settings(BaseSettings):
    gpt_model: str = "gpt-4o-mini"
    books_per_recommendation: int = 5
    enable_hardcover_integration: bool = True
```

#### 4. **Fail-Safe Design**
```python
# Graceful degradation when services fail
try:
    book_metadata = await hardcover_service.get_book_metadata(...)
    if book_metadata:
        # Apply metadata
    else:
        logger.warning(f"No metadata found for book: {book.title}")
except Exception as e:
    logger.error(f"Error enhancing book metadata: {e}")
    return book  # Return book without enhancement
```

### React/Frontend Patterns

#### 1. **Composition Pattern**
```tsx
// Components are composed from smaller parts
<GlassPanel>
  <MovieInput />
  <PreferencesPanel />
  <RecommendationResults />
</GlassPanel>
```

#### 2. **Hook Pattern**
```tsx
// Custom hooks for state management (implied)
const [movies, setMovies] = useState<Movie[]>([]);
const [loading, setLoading] = useState(false);
```

#### 3. **Provider Pattern**
```tsx
// Theme and configuration providers
// Context providers for global state
```

---

## Configuration & Environment

### Environment Variables

#### Backend Configuration (`backend/.env`)
```bash
# Required API Keys
OPENAI_API_KEY=                    # OpenAI or Groq API key
HARDCOVER_API_KEY=                 # Hardcover book database API key

# OpenAI-Compatible API Configuration
OPENAI_BASE_URL=https://api.openai.com/v1  # Can be changed to Groq
GPT_MODEL=gpt-4o-mini             # Model selection

# Feature Toggles
ENABLE_HARDCOVER_INTEGRATION=true # Enable book metadata enhancement

# Cache Configuration
CACHE_DIR=cache                   # Cache storage directory
CACHE_EXPIRE_SECONDS=3600         # General cache expiration (1 hour)
BOOK_CACHE_EXPIRE_SECONDS=86400   # Book metadata cache (24 hours)

# API Limits and Settings
MAX_MOVIES_PER_REQUEST=5          # Maximum movies per request
GPT_MAX_TOKENS=1200              # Token limit for GPT responses
GPT_TEMPERATURE=0.7              # Creativity vs consistency balance

# Development Settings
DEBUG=false                      # Debug mode flag
LOG_LEVEL=INFO                   # Logging level
```

#### Frontend Configuration
```bash
# Frontend environment variables (optional)
NEXT_PUBLIC_API_URL=http://localhost:8000  # Backend API URL
NEXT_PUBLIC_TMDB_API_KEY=                  # TMDB API key for movie posters
```

### Configuration Files

#### Backend Configuration (`backend/app/config.py`)
```python
class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env")
    
    # Core API Configuration
    openai_api_key: str                    # Required
    hardcover_api_key: str = ""            # Optional
    openai_base_url: str = "https://api.openai.com/v1"
    
    # Performance Tuning
    books_per_recommendation: int = 5      # Books to recommend
    gpt_max_tokens: int = 1200            # Response length limit
    max_concurrent_book_requests: int = 10 # Concurrent API calls
    
    # Feature Flags
    enable_hardcover_integration: bool = True
    enable_taste_profile_analysis: bool = True
    enable_recommendation_insights: bool = True
```

#### Frontend Configuration (`frontend/next.config.ts`)
```typescript
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Configuration for Next.js
  images: {
    domains: ['assets.hardcover.app', 'image.tmdb.org']  // External image sources
  }
};
```

### Configuration Management Strategy

#### 1. **Environment-Based Configuration**
- Development: Local `.env` files
- Production: Environment variables via hosting platform
- Staging: Separate environment configurations

#### 2. **Type-Safe Configuration**
```python
# Backend uses Pydantic for validation
class Settings(BaseSettings):
    openai_api_key: str  # Will raise error if missing
```

#### 3. **Default Value Strategy**
```python
# Sensible defaults for optional settings
cache_expire_seconds: int = 3600
books_per_recommendation: int = 5
enable_hardcover_integration: bool = True
```

---

## Deployment Architecture

### Development Environment
```
Developer Machine
├── Backend: http://localhost:8000
├── Frontend: http://localhost:3000
├── File Cache: ./backend/cache/
└── Environment: .env files
```

### Production Deployment Options

#### Option 1: Render.com (Current Setup)
```yaml
# render.yaml configuration
services:
  - type: web
    name: cinereads-backend
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "uvicorn app.main:app --host 0.0.0.0 --port $PORT"
    
  - type: web  
    name: cinereads-frontend
    env: node
    buildCommand: "npm install && npm run build"
    startCommand: "npm start"
```

#### Option 2: Vercel + Render
- **Frontend**: Deployed to Vercel for optimal Next.js performance
- **Backend**: Deployed to Render or similar Python hosting service
- **Configuration**: Environment variables set in hosting platforms

### Infrastructure Components

#### 1. **Web Servers**
- **Backend**: Uvicorn ASGI server (production-ready)
- **Frontend**: Next.js built-in server (development) or static export

#### 2. **Caching Layer**
- **Development**: File-system based cache in `./cache/`
- **Production**: Could be upgraded to Redis or similar

#### 3. **External Dependencies**
- **OpenAI/Groq**: AI model API calls
- **Hardcover**: Book metadata API
- **TMDB**: Movie poster API

#### 4. **Monitoring & Health Checks**
```python
# Health check endpoint in main.py
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "version": "1.0.0"
    }
```

#### 5. **Keep-Alive Mechanism**
```python
# Prevents Render free tier from sleeping
async def keep_alive_task():
    while True:
        # Ping health endpoint every 14 minutes
        await asyncio.sleep(840)
```

### Scalability Considerations

#### Current Architecture Limitations
- File-based caching (single instance)
- No database persistence
- Synchronous processing for some operations

#### Potential Scaling Improvements
- **Database**: PostgreSQL for persistence
- **Cache**: Redis for distributed caching  
- **Queue**: Celery for background processing
- **Load Balancer**: For multiple backend instances
- **CDN**: For static assets and image caching

---

## Navigation
- **Current**: 01-overview-and-architecture.md
- **Next**: [02-technical-implementation.md](./02-technical-implementation.md) - Dive into code details and function documentation
- **Related**: [03-apis-and-data-flow.md](./03-apis-and-data-flow.md) | [04-code-quality-and-gaps.md](./04-code-quality-and-gaps.md)