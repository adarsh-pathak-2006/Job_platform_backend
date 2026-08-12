# 🚀 Job Platform Backend

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Django REST Framework](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?&style=for-the-badge&logo=redis&logoColor=white)

A robust, production-ready backend for a modern Job Platform. Built with Django and Django Rest Framework (DRF), it facilitates interactions between **Candidates** and **Recruiters**.

## ✨ Features

* **Role-Based Authentication**: Secure JWT authentication supporting `CANDIDATE` and `RECRUITER` roles.
* **Recruiter Portal**: Post and manage active recruitments/job openings.
* **Candidate Portal**: Build digital resumes, list experiences/projects, and apply for jobs.
* **Production Ready**: Fully configured for production with Neon (PostgreSQL serverless), Upstash (Redis caching), Whitenoise (Static files), and CORS support.
* **Caching**: High-performance endpoint caching utilizing Redis.
* **Throttling**: Built-in API rate limiting protecting against abuse.
* **API Documentation**: Auto-generated Swagger and ReDoc documentation (`drf-spectacular`).

---

## 🏗 Architecture Overview

```mermaid
graph TD
    Client[Client App] -->|HTTPS| API[Django REST API]
    API --> Auth[Authentication App]
    API --> Cand[Candidate App]
    API --> Recr[Recruiter App]
    
    Auth --> DB[(Neon PostgreSQL)]
    Cand --> DB
    Recr --> DB
    
    API --> Cache[(Upstash Redis)]
```

---

## 🚀 Deployment Guide

This project is configured out-of-the-box for modern PAAS deployments (like Render, Railway, or Heroku).

### Prerequisites
1. **Neon PostgreSQL Database**: Get a connection string (`postgres://...`).
2. **Upstash Redis**: Get a connection string (`redis://...`).

### Environment Variables
Configure the following in your deployment dashboard or local `.env` file:

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | `your-secret-key` |
| `DEBUG` | Enable debug mode (set `False` in prod) | `False` |
| `ALLOWED_HOSTS` | Comma-separated domains | `api.domain.com` |
| `CORS_ALLOW_ALL_ORIGINS` | Allow all CORS origins | `False` |
| `CORS_ALLOWED_ORIGINS` | Comma-separated origins | `https://domain.com` |
| `DATABASE_URL` | Neon DB Connection String | `postgres://user:pass@host/db?sslmode=require` |
| `REDIS_URL` | Upstash Redis Connection String | `redis://default:pass@host:port` |

### Starting the Server in Production
```bash
gunicorn job.wsgi:application --bind 0.0.0.0:8000
```

---

## 💻 Local Development Setup

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd job
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Copy `.env.example` to `.env` and fill in your details. For local dev, you can leave `DATABASE_URL` and `REDIS_URL` empty to fallback to SQLite and Local Memory Cache.

5. **Run Migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Start the Development Server:**
   ```bash
   python manage.py runserver
   ```

---

## 📖 API Documentation

Once the server is running, you can access the automatically generated API documentation:
* **Swagger UI:** `/docs/`
* **ReDoc:** `/redoc/`
* **OpenAPI Schema:** `/schema/`
