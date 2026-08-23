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
            full_name=settings.OWNER_NAME,
            is_admin=True,
            is_active=True
        )
        db.add(admin)
        db.commit()
    else:
        admin.full_name = settings.OWNER_NAME
        admin.email = settings.ADMIN_EMAIL
        db.commit()

    # 2. Seed Skills (Exact resume skills: Python, Java, HTML, CSS, JS, MySQL, FastAPI, REST APIs, ML models, AWS, Git, Docker)
    skills_data = [
        # Programming Languages
        {"name": "Python", "category": "Programming Languages", "proficiency": 95, "experience_years": "", "icon": "🐍", "is_primary": True},
        {"name": "Java", "category": "Programming Languages", "proficiency": 85, "experience_years": "", "icon": "☕", "is_primary": True},
        {"name": "JavaScript", "category": "Programming Languages", "proficiency": 85, "experience_years": "", "icon": "🟨", "is_primary": True},

        # Web Technologies
        {"name": "HTML & CSS", "category": "Web Technologies", "proficiency": 92, "experience_years": "", "icon": "🌐", "is_primary": True},
        {"name": "JavaScript (DOM & Fetch)", "category": "Web Technologies", "proficiency": 88, "experience_years": "", "icon": "📜", "is_primary": True},

        # Backend
        {"name": "FastAPI", "category": "Backend", "proficiency": 96, "experience_years": "", "icon": "⚡", "is_primary": True},
        {"name": "REST APIs", "category": "Backend", "proficiency": 95, "experience_years": "", "icon": "📐", "is_primary": True},

        # Database
        {"name": "MySQL", "category": "Database", "proficiency": 90, "experience_years": "", "icon": "🐬", "is_primary": True},

        # Machine Learning & AI
        {"name": "TensorFlow", "category": "Machine Learning & AI", "proficiency": 88, "experience_years": "", "icon": "🧠", "is_primary": True},
        {"name": "LSTM", "category": "Machine Learning & AI", "proficiency": 86, "experience_years": "", "icon": "🔄", "is_primary": True},
        {"name": "OpenCV", "category": "Machine Learning & AI", "proficiency": 86, "experience_years": "", "icon": "👁️", "is_primary": True},
        {"name": "Scikit-learn", "category": "Machine Learning & AI", "proficiency": 90, "experience_years": "", "icon": "📊", "is_primary": True},
        {"name": "Logistic Regression", "category": "Machine Learning & AI", "proficiency": 88, "experience_years": "", "icon": "📈", "is_primary": True},

        # Cloud & Tools
        {"name": "Git & GitHub", "category": "Cloud & Tools", "proficiency": 92, "experience_years": "", "icon": "🐙", "is_primary": True},
        {"name": "Docker", "category": "Cloud & Tools", "proficiency": 86, "experience_years": "", "icon": "🐳", "is_primary": True},
    ]

    db.query(Skill).delete()
    for s in skills_data:
        db.add(Skill(**s))
    db.commit()

    # 3. Seed Projects (FastAPI Platform + Sign Language Recognition + Breast Cancer Prediction)
    projects_data = [
        {
            "title": "FastAPI Developer Portfolio & Live Platform",
            "slug": "fastapi-developer-portfolio",
            "summary": "Self-hosted developer portfolio and interactive live API sandbox built with FastAPI, Pydantic V2, SQLite, and WebSockets.",
            "description": (
                "Engineered a production-grade full-stack developer portfolio and API platform. Features dynamic OpenAPI documentation, "
                "OAuth2 JWT authentication, background asynchronous email processing with FastAPI BackgroundTasks, real-time WebSocket "
                "telemetry, and an interactive developer playground with 43 automated Pytest tests and CI/CD on Vercel."
            ),
            "tech_stack": json.dumps(["FastAPI", "Python", "SQLite", "Pydantic V2", "WebSockets", "Docker", "Pytest", "HTML/CSS/JS"]),
            "category": "Backend & APIs",
            "live_url": "/",
            "github_url": "https://github.com/pavankammari21-glitch/portfolio",
            "image_url": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=800&q=80",
            "architecture_notes": "Modular ASGI architecture, custom request execution time middleware (X-Process-Time-Sec), serverless SQLite persistence.",
            "is_featured": True,
            "stars_count": 98
        },
        {
            "title": "Sign Language Recognition System",
            "slug": "sign-language-recognition-system",
            "summary": "Real-time sign language gesture recognition and translation system utilizing Python, TensorFlow, LSTM, and OpenCV.",
            "description": (
                "Developed a real-time computer vision sign language recognition system using Python, TensorFlow, LSTM neural networks, and OpenCV. "
                "Achieved 92% accuracy in hand gesture classification and translation. Implemented real-time hand gesture detection, frame preprocessing, "
                "and sign-to-text conversion for accessible communication."
            ),
            "tech_stack": json.dumps(["Python", "TensorFlow", "LSTM", "OpenCV", "Machine Learning", "Deep Learning"]),
            "category": "Machine Learning & AI",
            "live_url": None,
            "github_url": "https://github.com/pavankammari6-wq",
            "image_url": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=800&q=80",
            "architecture_notes": "Real-time video frame preprocessing pipeline, MediaPipe/OpenCV hand coordinate extraction, multi-frame sequential LSTM inference.",
            "is_featured": True,
            "stars_count": 86
        },
        {
            "title": "FastAPI Task Manager",
            "slug": "fastapi-task-manager",
            "summary": "Full-stack task and workflow management application built with FastAPI, RESTful CRUD APIs, and Tailwind CSS.",
            "description": (
                "Engineered a responsive, high-performance task and productivity management system. "
                "Features complete RESTful CRUD endpoints for task lifecycle management, status filtering, priority classification, "
                "SQLite persistence, and serverless cloud deployment on Vercel."
            ),
            "tech_stack": json.dumps(["FastAPI", "Python", "SQLite", "REST APIs", "Tailwind CSS", "Vercel"]),
            "category": "Backend & Web",
            "live_url": "https://fast-api-task-manager-nine.vercel.app/",
            "github_url": "https://github.com/pavankammari6-wq/fast-api-task_manager",
            "image_url": "https://images.unsplash.com/photo-1484480974693-6ca0a78fb36b?w=800&q=80",
            "architecture_notes": "RESTful API architecture, structured Pydantic data modeling, asynchronous route handlers, Tailwind CSS UI, and Vercel serverless deployment.",
            "is_featured": True,
            "stars_count": 82
        },
        {
            "title": "Breast Cancer Prediction using Logistic Regression",
            "slug": "breast-cancer-prediction-logistic-regression",
            "summary": "Diagnostic machine learning model built with Scikit-learn on the Wisconsin Breast Cancer Dataset achieving over 94% accuracy.",
            "description": (
                "Built an accurate predictive machine learning model using Scikit-learn on the Wisconsin Breast Cancer Dataset. "
                "Achieved over 94% classification accuracy for tumor prediction. Applied feature scaling, data preprocessing, and rigorous "
                "model evaluation using precision, recall, and F1-score metrics."
            ),
            "tech_stack": json.dumps(["Python", "Scikit-learn", "Logistic Regression", "Data Preprocessing", "Evaluation Metrics"]),
            "category": "Machine Learning & AI",
            "live_url": None,
            "github_url": "https://github.com/pavankammari6-wq",
            "image_url": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=800&q=80",
            "architecture_notes": "Data normalization & standard scaling, cross-validation, binary cross-entropy loss optimization, and precision-recall trade-off tuning.",
            "is_featured": True,
            "stars_count": 74
        }
    ]

    db.query(Project).delete()
    for p in projects_data:
        db.add(Project(**p))
    db.commit()

    # 4. Seed Education & Certifications (From verified resume)
    experiences_data = [
        {
            "role_or_degree": "B.Tech in Information Technology",
            "organization": "Vignan Institute of Technology and Science, Telangana",
            "period": "2022 – 2026",
            "location": "Telangana, India",
            "item_type": "education",
            "description": "Pursuing Bachelor of Technology in Information Technology. Focused on Core Software Engineering, Python Programming, Database Management, and Machine Learning.",
            "key_achievements": json.dumps([
                "Active member of Infy Coders Club and coordinator of coding competitions.",
                "Demonstrated strong problem-solving, logical thinking, and teamwork skills.",
                "Engineered Machine Learning systems (Sign Language Recognition & Breast Cancer Prediction) and FastAPI backend architectures."
            ]),
            "skills_used": json.dumps(["Python", "Java", "FastAPI", "MySQL", "Data Structures", "HTML/CSS/JS"]),
            "order_index": 1
        },
        {
            "role_or_degree": "Intermediate (MPC)",
            "organization": "Narayana Junior College, Chaitanyapuri",
            "period": "2020 – 2022",
            "location": "Telangana, India",
            "item_type": "education",
            "description": "Completed higher secondary education in Mathematics, Physics, and Chemistry.",
            "key_achievements": json.dumps([
                "Developed strong analytical, mathematical, and logical thinking foundation."
            ]),
            "skills_used": json.dumps(["Mathematics", "Physics", "Analytical Thinking"]),
            "order_index": 2
        },
        {
            "role_or_degree": "SSC (10th Grade)",
            "organization": "Shanthi Nikethan High School",
            "period": "Completed 2020",
            "location": "Telangana, India",
            "item_type": "education",
            "description": "Completed secondary school certificate with high academic standing.",
            "key_achievements": json.dumps([
                "Excellence in science, mathematics, and communication."
            ]),
            "skills_used": json.dumps(["Science", "Mathematics", "Problem Solving"]),
            "order_index": 3
        }
    ]

    db.query(Experience).delete()
    for exp in experiences_data:
        db.add(Experience(**exp))
    db.commit()
