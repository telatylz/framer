from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import asyncio
import logging
from edge_impulse_client import EdgeImpulseClient

router = APIRouter(prefix="/api/edge-impulse", tags=["Edge Impulse"])

class SensorData(BaseModel):
    device_name: str
    sensor_type: str
    values: List[float]

class DeviceMetrics(BaseModel):
    device_name: str
    cpu_usage: float
    ram_usage: float
    disk_usage: float

@router.post("/sensor-data")
async def send_sensor_data(data: SensorData):
    """Sensor verilerini Edge Impulse'a gönder"""
    try:
        client = EdgeImpulseClient()
        response = client.send_sensor_data(
            data.device_name, 
            data.values, 
            data.sensor_type
        )
        
        if response.status_code == 200:
            return {"status": "success", "message": "Veri başarıyla gönderildi"}
        else:
            raise HTTPException(status_code=400, detail=f"Edge Impulse hatası: {response.text}")
            
    except Exception as e:
        logging.error(f"Edge Impulse gönderim hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/device-metrics")
async def send_device_metrics(metrics: DeviceMetrics):
    """Cihaz metriklerini Edge Impulse'a gönder"""
    try:
        client = EdgeImpulseClient()
        response = client.send_device_metrics(
            metrics.device_name,
            metrics.cpu_usage,
            metrics.ram_usage,
            metrics.disk_usage
        )
        
        if response.status_code == 200:
            return {"status": "success", "message": "Metrikler başarıyla gönderildi"}
        else:
            raise HTTPException(status_code=400, detail=f"Edge Impulse hatası: {response.text}")
            
    except Exception as e:
        logging.error(f"Edge Impulse metrik gönderim hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/bulk-data")
async def send_bulk_data(devices_data: List[DeviceMetrics]):
    """Toplu cihaz verisi gönder"""
    results = []
    client = EdgeImpulseClient()
    
    for device in devices_data:
        try:
            response = client.send_device_metrics(
                device.device_name,
                device.cpu_usage,
                device.ram_usage,
                device.disk_usage
            )
            results.append({
                "device": device.device_name,
                "status": "success" if response.status_code == 200 else "failed",
                "response_code": response.status_code
            })
        except Exception as e:
            results.append({
                "device": device.device_name,
                "status": "error",
                "error": str(e)
            })
    
    return {"results": results}
