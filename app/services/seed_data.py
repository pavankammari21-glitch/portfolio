import json
from sqlalchemy.orm import Session
from app.models import User, Project, Skill, Experience
from app.services.auth_service import get_password_hash
from app.config import settings

def seed_initial_data(db: Session):
    # 1. Seed Admin User
    admin = db.query(User).filter(User.username == settings.ADMIN_USERNAME).first()
    if not admin:
        admin = User(
            username=settings.ADMIN_USERNAME,
            email=settings.ADMIN_EMAIL,
            hashed_password=get_password_hash(settings.ADMIN_PASSWORD),
            full_name="Pavan",
            is_admin=True,
            is_active=True
        )
        db.add(admin)
        db.commit()

    # 2. Seed Skills
    if db.query(Skill).count() == 0:
        skills_data = [
            # Backend
            {"name": "Python 3.11+", "category": "Backend", "proficiency": 98, "experience_years": "4+ years", "icon": "🐍", "is_primary": True},
            {"name": "FastAPI", "category": "Backend", "proficiency": 96, "experience_years": "3+ years", "icon": "⚡", "is_primary": True},
            {"name": "Pydantic V2", "category": "Backend", "proficiency": 95, "experience_years": "3+ years", "icon": "🛡️", "is_primary": True},
            {"name": "SQLAlchemy & SQLModel", "category": "Backend", "proficiency": 92, "experience_years": "3+ years", "icon": "🗄️", "is_primary": True},
            {"name": "AsyncIO & WebSockets", "category": "Backend", "proficiency": 90, "experience_years": "3+ years", "icon": "🔌", "is_primary": True},
            {"name": "Celery & Redis", "category": "Backend", "proficiency": 88, "experience_years": "2+ years", "icon": "📦", "is_primary": True},
            
            # Databases
            {"name": "PostgreSQL", "category": "Databases", "proficiency": 92, "experience_years": "3+ years", "icon": "🐘", "is_primary": True},
            {"name": "Redis (Cache & PubSub)", "category": "Databases", "proficiency": 89, "experience_years": "2+ years", "icon": "🔥", "is_primary": True},
            {"name": "SQLite", "category": "Databases", "proficiency": 94, "experience_years": "4+ years", "icon": "💾", "is_primary": False},
            {"name": "MongoDB", "category": "Databases", "proficiency": 84, "experience_years": "2+ years", "icon": "🍃", "is_primary": False},
            
            # DevOps & Cloud
            {"name": "Docker & Compose", "category": "DevOps & Cloud", "proficiency": 91, "experience_years": "3+ years", "icon": "🐳", "is_primary": True},
            {"name": "CI/CD (GitHub Actions)", "category": "DevOps & Cloud", "proficiency": 88, "experience_years": "2+ years", "icon": "🔄", "is_primary": True},
            {"name": "AWS (EC2, S3, RDS, Lambda)", "category": "DevOps & Cloud", "proficiency": 85, "experience_years": "2+ years", "icon": "☁️", "is_primary": True},
            {"name": "Linux & Nginx", "category": "DevOps & Cloud", "proficiency": 89, "experience_years": "3+ years", "icon": "🐧", "is_primary": False},
            
            # AI & ML
            {"name": "LangChain & LangGraph", "category": "AI & ML", "proficiency": 88, "experience_years": "2+ years", "icon": "🦜", "is_primary": True},
            {"name": "RAG & Vector Embeddings", "category": "AI & ML", "proficiency": 86, "experience_years": "2+ years", "icon": "🧠", "is_primary": True},
            {"name": "HuggingFace & Transformers", "category": "AI & ML", "proficiency": 82, "experience_years": "1+ years", "icon": "🤗", "is_primary": False},
            
            # Frontend & Architecture
            {"name": "Modern JavaScript & HTML5/CSS3", "category": "Frontend & Tools", "proficiency": 87, "experience_years": "3+ years", "icon": "🌐", "is_primary": True},
            {"name": "REST & GraphQL API Design", "category": "Frontend & Tools", "proficiency": 96, "experience_years": "4+ years", "icon": "📐", "is_primary": True},
            {"name": "Pytest & TDD", "category": "Frontend & Tools", "proficiency": 93, "experience_years": "3+ years", "icon": "🧪", "is_primary": True},
        ]
        for s in skills_data:
            db.add(Skill(**s))
        db.commit()

    # 3. Seed Projects
    if db.query(Project).count() == 0:
        projects_data = [
            {
                "title": "FastAPI Distributed Microservices Hub",
                "slug": "fastapi-distributed-microservices",
                "summary": "High-throughput asynchronous backend platform featuring JWT auth, rate-limiting, and async background queue processing.",
                "description": (
                    "A production-grade distributed backend architecture built from the ground up using FastAPI, "
                    "SQLAlchemy 2.0, and Redis. Features OAuth2 password grant authentication with token blacklisting, "
                    "fine-grained RBAC permission decorators, distributed rate-limiting via Token Bucket algorithm, and "
                    "background task pipelines handling over 5,000 requests/sec with sub-10ms response times."
                ),
                "tech_stack": json.dumps(["FastAPI", "Python 3.11", "PostgreSQL", "Redis", "Docker", "Pytest"]),
                "category": "Backend & Cloud",
                "live_url": "https://github.com",
                "github_url": "https://github.com",
                "image_url": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=800&q=80",
                "architecture_notes": "Clean Hexagonal Architecture, Repository Pattern, Async Lifespan, Structured Logging with Correlation IDs.",
                "is_featured": True,
                "stars_count": 128
            },
            {
                "title": "Enterprise RAG & Autonomous Agent Engine",
                "slug": "enterprise-rag-agent-engine",
                "summary": "Multi-agent conversational workflow engine utilizing FastAPI, LangGraph, and Vector Databases for enterprise search.",
                "description": (
                    "End-to-end intelligent document retrieval and reasoning engine. Implements hybrid vector search "
                    "with cross-encoder re-ranking, streaming LLM completions via Server-Sent Events (SSE) and WebSockets, "
                    "and asynchronous background ingestion queues for multi-format document parsing (PDF, DOCX, Markdown)."
                ),
                "tech_stack": json.dumps(["FastAPI", "LangChain", "LangGraph", "ChromaDB", "Python", "WebSockets"]),
                "category": "AI & ML",
                "live_url": "https://github.com",
                "github_url": "https://github.com",
                "image_url": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=800&q=80",
                "architecture_notes": "Event-driven SSE streaming, Async Chunking worker, Milvus/Chroma vector indexing.",
                "is_featured": True,
                "stars_count": 94
            },
            {
                "title": "Real-time WebSocket Analytics & Telemetry Engine",
                "slug": "realtime-websocket-telemetry",
                "summary": "Ultra-low latency bidirectional WebSocket telemetry system with connection pooling and broadcast channels.",
                "description": (
                    "A high-concurrency real-time metrics and communication hub capable of orchestrating thousands of concurrent "
                    "WebSocket clients. Provides live room broadcasting, client state synchronization, heartbeats, and live "
                    "interactive dashboard widgets."
                ),
                "tech_stack": json.dumps(["FastAPI", "WebSockets", "Asyncio", "Vanilla JS", "Chart.js", "Docker"]),
                "category": "Real-time Systems",
                "live_url": "https://github.com",
                "github_url": "https://github.com",
                "image_url": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&q=80",
                "architecture_notes": "Custom ConnectionManager with pub/sub channel routing, backpressure handling.",
                "is_featured": True,
                "stars_count": 76
            },
            {
                "title": "Automated Legal & Court Data Harvester",
                "slug": "automated-court-data-harvester",
                "summary": "Asynchronous multi-threaded ETL pipeline extracting structured records with automatic captcha handling.",
                "description": (
                    "Engineered an automated data extraction and aggregation system utilizing Playwright, BeautifulSoup, "
                    "and FastAPI. Orchestrates scheduled background jobs, automated data sanitization, schema validation with Pydantic, "
                    "and exports to searchable PostgreSQL & Elasticsearch clusters."
                ),
                "tech_stack": json.dumps(["Python", "FastAPI", "Playwright", "PostgreSQL", "Pandas", "Docker"]),
                "category": "Data Engineering",
                "live_url": "https://github.com",
                "github_url": "https://github.com",
                "image_url": "https://images.unsplash.com/photo-1450133064473-71024230f91b?w=800&q=80",
                "architecture_notes": "Batch processing pipelines, idempotent database upserts, alerting webhooks.",
                "is_featured": False,
                "stars_count": 52
            },
            {
                "title": "Full-Stack Developer Portfolio & API Playground",
                "slug": "fastapi-developer-portfolio",
                "summary": "Self-hosted full-stack developer portfolio with an embedded interactive FastAPI API Sandbox.",
                "description": (
                    "The current platform! Engineered with FastAPI serving both dynamic REST APIs, WebSocket live streams, "
                    "and a glassmorphic frontend. Complete with CI/CD deployment presets for Render, Railway, Fly.io, and Docker."
                ),
                "tech_stack": json.dumps(["FastAPI", "Pydantic V2", "SQLAlchemy", "WebSockets", "Docker", "Render"]),
                "category": "Full Stack",
                "live_url": "/",
                "github_url": "https://github.com",
                "image_url": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&q=80",
                "architecture_notes": "Monolithic modular design, dynamic PDF/JSON resume exports, multi-cloud deployment manifests.",
                "is_featured": True,
                "stars_count": 89
            }
        ]
        for p in projects_data:
            db.add(Project(**p))
        db.commit()

    # 4. Seed Experience
    if db.query(Experience).count() == 0:
        experiences_data = [
            {
                "role_or_degree": "Senior Python & Backend Engineer",
                "organization": "Tech Innovations & Automation Labs",
                "period": "2023 - Present",
                "location": "Hyderabad, India",
                "item_type": "work",
                "description": "Leading the architecture and implementation of scalable FastAPI backend services, LLM autonomous workflows, and distributed microservices.",
                "key_achievements": json.dumps([
                    "Architected high-throughput RESTful APIs serving 2M+ monthly requests with 99.98% uptime.",
                    "Migrated monolithic backend pipelines to asynchronous FastAPI & Celery tasks, cutting API latency by 45%.",
                    "Integrated LangGraph and vector retrieval engines for automated intelligent document extraction.",
                    "Implemented rigorous automated testing suite with Pytest achieving >90% code coverage."
                ]),
                "skills_used": json.dumps(["FastAPI", "Python", "PostgreSQL", "Docker", "Redis", "LangChain", "WebSockets"]),
                "order_index": 1
            },
            {
                "role_or_degree": "Backend & Cloud Engineer",
                "organization": "Vee Group & Enterprise Automation",
                "period": "2021 - 2023",
                "location": "Hyderabad, India",
                "item_type": "work",
                "description": "Developed resilient data collection engines, automated web services, and cloud deployment pipelines.",
                "key_achievements": json.dumps([
                    "Engineered asynchronous ETL pipelines extracting and indexing millions of structured records.",
                    "Deployed containerized microservices across AWS EC2 and RDS with automated GitHub Actions CI/CD.",
                    "Designed secure JWT token-based authentication and role-based access control systems."
                ]),
                "skills_used": json.dumps(["Python", "FastAPI", "SQLAlchemy", "Docker", "AWS", "Git", "Playwright"]),
                "order_index": 2
            },
            {
                "role_or_degree": "Bachelor of Technology in Computer Science & Engineering",
                "organization": "Jawaharlal Nehru Technological University",
                "period": "2017 - 2021",
                "location": "Hyderabad, India",
                "item_type": "education",
                "description": "Comprehensive coursework in Data Structures, Algorithms, Distributed Systems, Database Management Systems, and Cloud Computing.",
                "key_achievements": json.dumps([
                    "Graduated with First Class with Distinction.",
                    "Lead Developer in University Coding Club and Finalist in National Hackathon."
                ]),
                "skills_used": json.dumps(["Data Structures", "Algorithms", "Python", "SQL", "Computer Networks"]),
                "order_index": 3
            },
            {
                "role_or_degree": "AWS Certified Solutions Architect & Python Specialist",
                "organization": "Amazon Web Services / Professional Certifications",
                "period": "2023",
                "location": "Global",
                "item_type": "certification",
                "description": "Certified in designing high-availability, fault-tolerant, and secure distributed cloud systems on AWS.",
                "key_achievements": json.dumps([
                    "Demonstrated mastery of VPC, IAM, EC2, S3, RDS, Lambda, and CloudWatch architectures."
                ]),
                "skills_used": json.dumps(["AWS", "Cloud Architecture", "Security", "DevOps"]),
                "order_index": 4
            }
        ]
        for exp in experiences_data:
            db.add(Experience(**exp))
        db.commit()
