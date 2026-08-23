# ⚡ FastAPI Developer Portfolio & Live Platform

> **A modern developer portfolio & interactive API platform for Pavan, engineered with FastAPI 0.111, Python 3.11, Pydantic V2, SQLite, and WebSockets.**

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Pydantic](https://img.shields.io/badge/Pydantic-V2-E92063?style=for-the-badge&logo=pydantic&logoColor=white)](https://docs.pydantic.dev/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Tests](https://img.shields.io/badge/Pytest-43%2F43%20Passed-4EBA6F?style=for-the-badge&logo=pytest&logoColor=white)](https://pytest.org/)

---

## 🎯 FastAPI Topics & Concepts Demonstrated

This portfolio implements all core & advanced topics of FastAPI:

| Topic | Implementation in Code |
| :--- | :--- |
| **Lifespan Context (`lifespan`)** | `app/main.py`: `asynccontextmanager` startup table migrations & default database seeding. |
| **Modular APIRouters** | `app/routers/`: Auth, Projects, Skills, Experience, Contact, Analytics, Resume, WebSockets. |
| **Pydantic V2 Modeling** | `app/schemas/`: `Field()`, `EmailStr`, `@field_validator`, `ConfigDict(from_attributes=True)`. |
| **Path & Query Parameters** | `Path(..., ge=1)`, `Query(...)` with regex, default filters, pagination (`limit`, `page`). |
| **File Uploads** | `app/routers/projects.py`: `UploadFile` & `File(...)` multipart image processing. |
| **Dependency Injection** | `app/dependencies.py`: Database sessions (`yield`), OAuth2 security, rate-limiting factory. |
| **OAuth2 & JWT Auth** | `app/routers/auth.py`: Password hashing with bcrypt, JWT token generation, protected `/me` & admin routes. |
| **Background Tasks** | `app/routers/contact.py`: `BackgroundTasks` asynchronous simulated notification dispatch. |
| **Real-time WebSockets** | `app/routers/websocket.py`: `/ws/live-stats` connection manager with live broadcast & latency ping. |
| **Custom Middleware** | `app/main.py`: CORS, `X-Process-Time-Sec` header injection, and security logging. |
| **Custom Exception Handlers** | `app/exceptions.py`: Standardized JSON error structures for 404, 401, 403, 422, 429. |
| **Dynamic Headers & Cookies** | `app/routers/resume.py`: Custom `Content-Disposition`, cookies, printable PDF/HTML view. |
| **Static Files SPA** | `app/static/`: Mounted glassmorphism UI with live API tester & real-time telemetry. |

---

## 🚀 Quick Start (Local Run)

1. Clone or navigate to the directory:
   ```bash
   cd resume_porfolio_pavan
   ```

2. Run the application:
   ```bash
   python run.py
   ```

3. Open your browser:
   - **Portfolio Website**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
   - **Interactive Swagger Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - **ReDoc Documentation**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
   - **Dynamic Resume JSON**: [http://127.0.0.1:8000/api/resume/json](http://127.0.0.1:8000/api/resume/json)
   - **Printable Resume (PDF)**: [http://127.0.0.1:8000/api/resume/download](http://127.0.0.1:8000/api/resume/download)

---

## 🧪 Automated Testing

Run the 20-point test suite covering auth, projects, skills, contact form, background tasks, and WebSockets:

```bash
python -m pytest tests/ -v
```

---

## 🚢 Deployment

Ready for 1-click deployment on **Render**, **Railway**, **Fly.io**, **Vercel**, or **Docker**. See [DEPLOYMENT.md](file:///d:/resume_porfolio_pavan/DEPLOYMENT.md) for full instructions.
