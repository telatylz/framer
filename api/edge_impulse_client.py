import requests
import hmac
import hashlib
import json
import time
import os
from typing import List, Dict

class EdgeImpulseClient:
    def __init__(self):
        self.api_key = os.getenv("EDGE_IMPULSE_API_KEY", "ei_2c3de7eb7709a48a29157acdcd5f63fd76c548abbf52e0e7130bc444f67631dd")
        self.hmac_key = os.getenv("EDGE_IMPULSE_HMAC_KEY", "ef700bb07877e8e29b52e2c1db85396a")
        self.base_url = "https://ingestion.edgeimpulse.com/api"
    
    def send_sensor_data(self, device_name: str, sensor_data: List[float], sensor_name: str = "accelerometer"):
        """Cihaz sensor verilerini Edge Impulse'a gönder"""
        
        payload = {
            "protected": {
                "ver": "v1",
                "alg": "HS256",
                "iat": int(time.time())
            },
            "payload": {
                "device_name": device_name,
                "device_type": "DAKITAI_DEVICE",
                "interval_ms": 10,
                "sensors": [{"name": sensor_name, "units": "m/s2"}],
                "values": [sensor_data]
            }
        }
        
        # HMAC imzalama
        message = json.dumps(payload["payload"], separators=(',', ':'))
        signature = hmac.new(
            bytes.fromhex(self.hmac_key),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        payload["signature"] = signature
        
        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        
        response = requests.post(
            f"{self.base_url}/training/data",
            json=payload,
            headers=headers
        )
        
        return response
    
    def send_device_metrics(self, device_name: str, cpu: float, ram: float, disk: float):
        """Sistem metriklerini gönder"""
        metrics = [cpu, ram, disk]
        return self.send_sensor_data(device_name, metrics, "system_metrics")

# Test fonksiyonu
if __name__ == "__main__":
    client = EdgeImpulseClient()
    
    # Test verisi gönder
    response = client.send_device_metrics("test_device", 45.2, 67.8, 23.1)
    print(f"Response: {response.status_code}")
    print(f"Content: {response.text}")
