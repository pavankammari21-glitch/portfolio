# 🚀 Deployment Guide — Pavan's FastAPI Portfolio & Platform

This repository is built to be deployed to all major cloud hosting platforms in minutes.

---

## 🌟 Option 1: Deploy to Render (Recommended — Free Tier)

1. Push your code to GitHub:
   ```bash
   git init
   git add .
   git commit -m "FastAPI Portfolio Platform"
   git remote add origin https://github.com/YOUR_USERNAME/portfolio.git
   git push -u origin main
   ```
2. Log into [Render.com](https://render.com).
3. Click **New +** -> **Web Service**.
4. Connect your GitHub repository.
5. Configure settings:
   - **Name**: `pavan-fastapi-portfolio`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. Click **Create Web Service**. Your portfolio will be live at `https://pavan-fastapi-portfolio.onrender.com`!

*(Alternatively, connect the included `render.yaml` as a Render Blueprint for 100% automated configuration).*

---

## 🚂 Option 2: Deploy to Railway

1. Install Railway CLI or go to [railway.app](https://railway.app).
2. Click **New Project** -> **Deploy from GitHub repo**.
3. Select this repository. Railway automatically detects `railway.json` and `Procfile`.
4. Add environment variables if needed (`ADMIN_PASSWORD`, `JWT_SECRET_KEY`).
5. Railway provides a live `.up.railway.app` HTTPS domain immediately.

---

## 🐳 Option 3: Deploy with Docker / Docker Compose

### Local / Server Docker Build:
```bash
# Build the production Docker image
docker build -t pavan-portfolio:latest .

# Run container on port 8000
docker run -d -p 8000:8000 --name portfolio pavan-portfolio:latest
```

### Docker Compose:
```bash
docker compose up -d --build
```
Access at `http://localhost:8000`.

---

## ✈️ Option 4: Deploy to Fly.io

1. Install Fly CLI: `curl -L https://fly.io/install.sh | sh` (or `winget install flyctl` on Windows).
2. Authenticate: `fly auth login`
3. Launch:
   ```bash
   fly launch
   fly deploy
   ```

---

## ▲ Option 5: Deploy to Vercel (Serverless ASGI)

1. Install Vercel CLI: `npm i -g vercel`
2. Run in the root directory:
   ```bash
   vercel
   ```
3. Vercel routes all requests via `vercel.json` to `api/index.py`.

---

## 🖥️ Option 6: Deploy to Ubuntu Linux VPS (Nginx + Systemd)

1. Clone repository to `/var/www/portfolio`:
   ```bash
   sudo apt update && sudo apt install python3-pip python3-venv git nginx -y
   git clone <REPO_URL> /var/www/portfolio
   cd /var/www/portfolio
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Create Systemd Service (`/etc/systemd/system/fastapi_portfolio.service`):
   ```ini
   [Unit]
   Description=FastAPI Portfolio Platform
   After=network.target

   [Service]
   User=www-data
   WorkingDirectory=/var/www/portfolio
   ExecStart=/var/www/portfolio/venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 4
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

3. Enable and start:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable --now fastapi_portfolio
   ```

4. Configure Nginx reverse proxy with WebSocket support:
   ```nginx
   server {
       server_name yourdomain.com;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
       }
   }
   ```
