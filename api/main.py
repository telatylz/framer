from fastapi import FastAPI, WebSocket, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db, engine, Base
import models
import auth
import uvicorn
import os
from edge_impulse_api import router as edge_impulse_router
from face_recognition import face_service

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DAKiTAI API",
    description="Profesyonel İşletme Yönetim Sistemi API",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://panel.dakiktabela.com", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

# Include Edge Impulse router
app.include_router(edge_impulse_router)

# Auth dependency
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    return auth.verify_token(credentials.credentials, db)

@app.get("/")
async def root():
    return {"message": "DAKiTAI API v1.0.0", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

# Auth endpoints
@app.post("/auth/login")
async def login(credentials: dict, db: Session = Depends(get_db)):
    return auth.authenticate_user(credentials["username"], credentials["password"], db)

@app.post("/auth/register")
async def register(user_data: dict, db: Session = Depends(get_db)):
    return auth.create_user(user_data, db)

# Dashboard endpoints
@app.get("/dashboard/stats")
async def dashboard_stats(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    return {
        "total_devices": 0,
        "online_devices": 0,
        "total_users": 1,
        "active_sessions": 1,
        "system_health": "good"
    }

# Device endpoints
@app.get("/devices")
async def get_devices(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    return []

@app.post("/devices")
async def create_device(device_data: dict, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    return {"message": "Device created", "id": 1}

# Network endpoints
@app.get("/network/scan")
async def network_scan(current_user = Depends(get_current_user)):
    return {"devices": [], "scan_time": "2026-01-22T07:30:00Z"}

# CRM endpoints
@app.get("/crm/customers")
async def get_customers(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    return []

# Vehicle tracking endpoints
@app.get("/vehicles")
async def get_vehicles(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    return []

# PBX endpoints
@app.get("/pbx/status")
async def pbx_status(current_user = Depends(get_current_user)):
    return {"status": "running", "extensions": 0, "active_calls": 0}

# Camera endpoints
@app.get("/cameras")
async def get_cameras(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    return []

# Face Recognition endpoints
@app.post("/face/detect")
async def detect_faces(data: dict, current_user = Depends(get_current_user)):
    """Görüntüden yüzleri tespit et"""
    if 'image' not in data:
        raise HTTPException(status_code=400, detail="Image data required")
    
    faces = face_service.detect_faces(data['image'])
    return {"faces": faces, "count": len(faces)}

@app.post("/face/add")
async def add_face(data: dict, current_user = Depends(get_current_user)):
    """Yeni yüz ekle"""
    required_fields = ['image', 'person_name', 'person_id']
    for field in required_fields:
        if field not in data:
            raise HTTPException(status_code=400, detail=f"{field} required")
    
    success = face_service.add_face(data['image'], data['person_name'], data['person_id'])
    if success:
        return {"message": "Face added successfully", "person_id": data['person_id']}
    else:
        raise HTTPException(status_code=400, detail="Failed to add face")

@app.get("/face/registered")
async def get_registered_faces(current_user = Depends(get_current_user)):
    """Kayıtlı yüzlerin listesini getir"""
    faces = face_service.get_registered_faces()
    return {"registered_faces": faces}

@app.delete("/face/{person_id}")
async def delete_face(person_id: int, current_user = Depends(get_current_user)):
    """Kayıtlı yüzü sil"""
    success = face_service.delete_face(person_id)
    if success:
        return {"message": "Face deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Face not found")

@app.post("/face/train")
async def train_model(current_user = Depends(get_current_user)):
    """Yüz tanıma modelini yeniden eğit"""
    success = face_service.train_model()
    if success:
        return {"message": "Model trained successfully"}
    else:
        raise HTTPException(status_code=400, detail="Training failed - no faces registered")

# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Echo: {data}")
    except:
        pass

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
