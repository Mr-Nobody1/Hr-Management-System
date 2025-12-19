# HR Management System

A multi-agent HR Management System with Python backend and React frontend, powered by Google Gemini 2.5 Flash.

## Features

- 🤖 **8 AI Agents**: Orchestrator, Payslip, Leave, Employee, Attendance, Benefits, Performance, Policy
- 💬 **Chat Interface**: Clean, modern chatbot UI
- 🌙 **Dark/Light Mode**: Toggle between themes
- 📱 **Responsive Design**: Works on desktop and mobile
- 🧠 **Conversation Memory**: Context-aware multi-turn conversations
- 🌐 **Multi-language**: English, Spanish, French, Arabic, Chinese

---

## High-Level Workflow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              USER INTERFACE                                  │
│                         (React + TypeScript + Tailwind)                      │
└─────────────────────────────────┬───────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              FASTAPI BACKEND                                 │
│                                                                              │
│  ┌──────────────┐    ┌─────────────────┐    ┌──────────────────┐           │
│  │ Session      │    │  Chat Endpoint  │    │   Translations   │           │
│  │ Memory       │◄───┤  /api/chat      │───►│   (5 Languages)  │           │
│  └──────────────┘    └────────┬────────┘    └──────────────────┘           │
│                               │                                              │
└───────────────────────────────┼──────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ORCHESTRATOR AGENT                                   │
│                    (Routes queries using LLM intelligence)                   │
│                                                                              │
│         ┌────────────────────────────────────────────────────┐              │
│         │              Gemini 2.5 Flash LLM                  │              │
│         │         (Query classification & routing)           │              │
│         └────────────────────────┬───────────────────────────┘              │
│                                  │                                           │
└──────────────────────────────────┼───────────────────────────────────────────┘
                                   │
           ┌───────────────────────┼───────────────────────┐
           │                       │                       │
           ▼                       ▼                       ▼
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│ 💰 Payslip Agent │  │ 📅 Leave Agent   │  │ 👤 Employee Agent│
│   salary, tax,   │  │  balance, PTO,   │  │  profile, team,  │
│   deductions     │  │  requests        │  │  department      │
└──────────────────┘  └──────────────────┘  └──────────────────┘
           │                       │                       │
           ▼                       ▼                       ▼
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│ ⏰ Attendance    │  │ 🎁 Benefits Agent│  │ 📊 Performance   │
│   clock in/out,  │  │  insurance,      │  │  reviews, goals, │
│   hours, OT      │  │  401k, wellness  │  │  KPIs, feedback  │
└──────────────────┘  └──────────────────┘  └──────────────────┘
           │                       │                       │
           └───────────────────────┼───────────────────────┘
                                   │
                                   ▼
                      ┌──────────────────────┐
                      │ 📋 Policy Agent      │
                      │   HR policies, FAQs, │
                      │   guidelines, rules  │
                      └──────────────────────┘
                                   │
                                   ▼
                      ┌──────────────────────┐
                      │    JSON Data Store   │
                      │ employees, payslips, │
                      │ leaves, attendance,  │
                      │ benefits, performance│
                      │ policies             │
                      └──────────────────────┘
```

---

## Project Structure (Worktree)

```
.
├── README.md                          # Project documentation
├── .gitignore                         # Git ignore rules
├── backend/                           # Python FastAPI Backend
│   ├── main.py                        # FastAPI app, API endpoints
│   ├── models.py                      # Pydantic models (ChatMessage, etc.)
│   ├── llm_service.py                 # Gemini LLM integration
│   ├── session_memory.py              # Conversation memory service
│   ├── translations.py                # Multi-language support (5 langs)
│   ├── requirements.txt               # Python dependencies
│   ├── .env                           # Environment variables (API keys)
│   ├── agents/                        # AI Agent implementations
│   │   ├── __init__.py                # BaseAgent class & utilities
│   │   ├── orchestrator.py            # Main router agent (LLM-powered)
│   │   ├── payslip_agent.py           # Salary & payslip queries
│   │   ├── leave_agent.py             # Leave balance & requests
│   │   ├── employee_agent.py          # Profile & team queries
│   │   ├── attendance_agent.py        # Clock in/out, hours tracking
│   │   ├── benefits_agent.py          # Insurance, 401k, wellness
│   │   ├── performance_agent.py       # Reviews, goals, KPIs
│   │   └── policy_agent.py            # HR policies & FAQs
│   └── data/                          # JSON data files (mock database)
│       ├── employees.json             # Employee profiles
│       ├── payslips.json              # Salary & deduction records
│       ├── leaves.json                # Leave balances & history
│       ├── attendance.json            # Attendance records
│       ├── benefits.json              # Benefits enrollment
│       ├── performance.json           # Performance reviews & goals
│       └── policies.json              # HR policies & FAQs
└── frontend/                          # React + TypeScript Frontend
    ├── index.html                     # HTML entry point
    ├── package.json                   # Node dependencies
    ├── vite.config.ts                 # Vite configuration
    ├── tailwind.config.js             # Tailwind CSS config
    ├── tsconfig.json                  # TypeScript config
    └── src/
        ├── main.tsx                   # React entry point
        ├── App.tsx                    # Main app with routing
        ├── index.css                  # Global styles & animations
        ├── components/                # React components
        │   ├── ChatInterface.tsx      # Chat UI with messages
        │   ├── MessageBubble.tsx      # Individual message display
        │   ├── Sidebar.tsx            # Quick actions & agent status
        │   ├── ThemeToggle.tsx        # Dark/Light mode switch
        │   └── LanguageSelector.tsx   # Language dropdown
        ├── contexts/                  # React contexts
        │   └── LanguageContext.tsx    # Language state management
        └── hooks/                     # Custom React hooks
            └── useTheme.ts            # Theme management hook
```

---

## Data Flow Diagram

```
User Query                   System Response
    │                              ▲
    ▼                              │
┌───────────────────────────────────────────────────────────┐
│                    FRONTEND (React)                        │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────┐   │
│  │ ChatInterface│  │LanguageCtx   │  │ SessionStorage │   │
│  │ (messages)  │  │ (i18n state) │  │ (session ID)   │   │
│  └──────┬──────┘  └──────────────┘  └────────────────┘   │
└─────────┼─────────────────────────────────────────────────┘
          │ POST /api/chat
          │ {message, employee_id, session_id, language}
          ▼
┌───────────────────────────────────────────────────────────┐
│                    BACKEND (FastAPI)                       │
│                                                            │
│  1. Session Memory stores user message                     │
│  2. Orchestrator routes to correct agent via LLM          │
│  3. Specialized agent processes query                      │
│  4. LLM generates natural language response                │
│  5. Response translated if language != 'en'               │
│  6. Session Memory stores assistant response               │
│                                                            │
└───────────────────────────────────────────────────────────┘
```

---

## Getting Started

### Prerequisites

- Python 3.9+
- Bun (or npm/yarn)
- Gemini API Key (from https://aistudio.google.com/app/apikey)

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python -m uvicorn main:app --reload --port 8000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
bun install

# Run development server
bun run dev
```

### Access the Application

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## Agents

| Agent | Description | Example Queries |
|-------|-------------|-----------------|
| **Orchestrator** | Routes queries to specialized agents | (automatic routing) |
| **Payslip** | Salary, payslips, deductions, tax info | "Show my payslip", "What's my salary?" |
| **Leave** | Leave balance, requests, history | "Leave balance", "Request vacation" |
| **Employee** | Profile, team, department info | "My profile", "Who's my manager?" |
| **Attendance** | Clock in/out, hours, overtime | "Clock in", "Hours this week" |
| **Benefits** | Health, 401k, wellness programs | "My benefits", "401k details" |
| **Performance** | Reviews, goals, KPIs, feedback | "My performance", "What are my goals?" |
| **Policy** | HR policies, guidelines, FAQs | "WFH policy", "Dress code rules" |

---

## New Features

### Conversation Memory
The system remembers your conversation context within a session:
```
You: "Show my leave balance"
AI:  (shows all leave types)
You: "How many sick days specifically?"
AI:  (understands context, shows sick days only)
```

### Multi-language Support
Switch between languages using the language selector:
- 🇬🇧 English
- 🇪🇸 Spanish (Español)
- 🇫🇷 French (Français)
- 🇸🇦 Arabic (العربية)
- 🇨🇳 Chinese (中文)

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | Python 3.9+, FastAPI, Pydantic |
| **LLM** | Google Gemini 2.5 Flash |
| **Frontend** | React 18, TypeScript, Tailwind CSS |
| **Build Tool** | Vite, Bun |
| **Data** | JSON files (mock database) |
