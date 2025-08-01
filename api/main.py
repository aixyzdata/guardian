from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime

app = FastAPI(
    title="Guardian - Canonika",
    description="Sistema de segurança e compliance do Canonika",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Página inicial do Guardian"""
    return {
        "service": "Guardian",
        "description": "Sistema de segurança e compliance do Canonika",
        "status": "online",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/health")
async def health():
    """Health check do Guardian"""
    return {
        "service": "Guardian",
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

@app.get("/api/security/status")
async def security_status():
    """Status de segurança do sistema"""
    return {
        "keycloak": {
            "status": "online",
            "url": "http://localhost:8080",
            "realm": "canonika"
        },
        "opa": {
            "status": "online",
            "url": "http://localhost:8181",
            "policies_loaded": 5
        },
        "sessions": {
            "active": 12,
            "total": 45
        },
        "security_events": {
            "last_24h": 156,
            "failed_logins": 3,
            "suspicious_activities": 1
        }
    }

@app.get("/api/security/services")
async def get_security_services():
    """Lista de serviços de segurança"""
    return {
        "services": [
            {
                "name": "Keycloak",
                "description": "Identity Provider",
                "url": "http://localhost:8080/admin",
                "port": 8080,
                "status": "online"
            },
            {
                "name": "OPA",
                "description": "Open Policy Agent",
                "url": "http://localhost:8181",
                "port": 8181,
                "status": "online"
            },
            {
                "name": "Quarter",
                "description": "Ponto de entrada",
                "url": "http://localhost",
                "port": 80,
                "status": "online"
            }
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005) 