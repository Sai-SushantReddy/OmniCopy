# OmniCopy

AI-powered content transformation platform built with FastAPI, PostgreSQL, Celery, Redis, Docker, and Groq LLMs.

OmniCopy allows users to create content once and automatically transform it into platform-specific versions (Instagram, LinkedIn, Twitter/X, etc.) using asynchronous AI-powered processing.

---

## Live Demo

**API docs (Swagger UI): https://omnicopy-production.up.railway.app/docs**

### Try it in 2 minutes
1. Open the link above and use `POST /api/v1/auth/register` to create an account (click **Try it out**, fill in the example body, **Execute**).
2. Use `POST /api/v1/auth/login` to get an access token, or click **Authorize** at the top right and enter your credentials.
3. Create content with `POST /api/v1/contents`.
4. Start a transformation with `POST /api/v1/contents/{id}/transform` (a background Celery worker calls the LLM).
5. Fetch your content with `GET /api/v1/contents` to see the transformed result. Processing is asynchronous, so if the status is still `pending`, wait a few seconds and try again.

> Hosted on Railway (API, PostgreSQL, Redis and a Celery worker as separate services). This is a demo deployment, so please use test data only.

## Run locally

```bash
git clone https://github.com/Sai-SushantReddy/OmniCopy.git
cd OmniCopy
cp .env.example .env        # add your GROQ_API_KEY and a strong JWT_SECRET
docker compose up --build
```

API docs will be at http://localhost:8000/docs (change the port if yours differs).

---

## Features

- JWT Authentication
- User Registration & Login
- Protected REST APIs
- Content Management
- AI-powered Content Transformation
- Background Processing using Celery
- Redis Task Queue
- PostgreSQL Database
- Alembic Database Migrations
- Dockerized Deployment
- Health & Readiness Endpoints
- Structured Logging
- Automatic Database Migrations on Startup

---

## Tech Stack

### Backend

- FastAPI
- SQLAlchemy
- Alembic
- Pydantic

### Database

- PostgreSQL

### Background Jobs

- Celery
- Redis

### AI

- Groq API
- Llama Models

### DevOps

- Docker
- Docker Compose

---

## Project Architecture

```
                 Client
                    │
                    ▼
             FastAPI REST API
                    │
      ┌─────────────┴─────────────┐
      ▼                           ▼
 PostgreSQL                  Redis Queue
      ▲                           │
      │                           ▼
 Generated Content         Celery Worker
                                  │
                                  ▼
                           Groq LLM API
                                  │
                                  ▼
                          Generated Output
```

---

## Folder Structure

```
OmniCopy
│
├── alembic/
├── app/
│   ├── api/
│   ├── core/
│   ├── database/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── workers/
│   └── main.py
│
├── docker-compose.yml
├── Dockerfile
├── entrypoint.sh
├── requirements.txt
└── README.md
```

---

## Authentication Flow

1. Register User
2. Login
3. Receive JWT Access Token
4. Authorize Swagger/API Requests
5. Access Protected Endpoints

---

## Content Transformation Workflow

1. User creates content.
2. FastAPI stores the content.
3. User requests transformation.
4. Celery receives the task.
5. Worker sends prompt to Groq.
6. AI generates platform-specific content.
7. Generated output is stored in PostgreSQL.
8. User retrieves transformed content.

---

## API Endpoints

### Authentication

| Method | Endpoint |
|----------|------------------------|
| POST | `/api/v1/auth/register` |
| POST | `/api/v1/auth/login` |

---

### Users

| Method | Endpoint |
|----------|----------------|
| GET | `/api/v1/users/me` |

---

### Content

| Method | Endpoint |
|----------|--------------------------|
| POST | `/api/v1/contents` |
| GET | `/api/v1/contents` |
| POST | `/api/v1/contents/{id}/transform` |

---


## Docker

The application runs with four services.

- FastAPI
- PostgreSQL
- Redis
- Celery Worker

Database migrations are automatically executed using an entrypoint script before the API server starts.

---

## Future Improvements

- Content Versioning
- Multiple AI Providers
- Streaming Responses
- Prompt Templates
- User Analytics Dashboard
- API Rate Limiting Enhancements
- CI/CD Pipeline
- Kubernetes Deployment
- Unit & Integration Testing
- Vector Database Support
- RAG-based Context Injection
- Multi-language Content Generation

---

## Learning Outcomes

This project demonstrates experience with:

- Production FastAPI Development
- REST API Design
- JWT Authentication
- SQLAlchemy ORM
- Alembic Migrations
- PostgreSQL
- Docker & Docker Compose
- Redis
- Celery Background Workers
- LLM API Integration
- Asynchronous Processing
- Clean Backend Architecture

---

## Author

**Sai Sushant Reddy**

GitHub:
https://github.com/Sai-SushantReddy

LinkedIn:
https://www.linkedin.com/in/sai-sushant-reddy-vudem
