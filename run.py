"""
Single command production / dev server runner for Pavan's FastAPI Portfolio
"""
import os
import sys
import uvicorn

# Configure stdout/stderr for utf-8 on Windows
if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    reload = os.getenv("ENV", "development").lower() == "development"

    print(f"[*] Starting Pavan's Portfolio API & Platform on http://{host}:{port}")
    print(f"[*] Swagger OpenAPI Docs available at http://{host}:{port}/docs")
    print(f"[*] Frontend Portfolio available at http://{host}:{port}")
    
    uvicorn.run("app.main:app", host=host, port=port, reload=reload)
