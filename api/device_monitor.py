import asyncio
import json
import psutil
import time
import requests
from datetime import datetime

class DeviceMonitor:
    def __init__(self):
        self.api_base = "https://panel.dakiktabela.com/api"
        
    async def collect_system_metrics(self):
        """Sistem metriklerini topla"""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return {
            "device_name": "dakitai_server",
            "cpu_usage": cpu_percent,
            "ram_usage": memory.percent,
            "disk_usage": disk.percent,
            "timestamp": datetime.now().isoformat()
        }
    
    async def send_to_edge_impulse(self, metrics):
        """Metrikleri Edge Impulse'a gönder"""
        try:
            response = requests.post(
                f"{self.api_base}/edge-impulse/device-metrics",
                json=metrics,
                headers={"Content-Type": "application/json"}
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Edge Impulse gönderim hatası: {e}")
            return False
    
    async def monitor_loop(self):
        """Ana izleme döngüsü"""
        print("DAKİTAI Edge Impulse Monitor başlatıldı...")
        
        while True:
            try:
                # Metrikleri topla
                metrics = await self.collect_system_metrics()
                
                # Edge Impulse'a gönder
                success = await self.send_to_edge_impulse(metrics)
                
                status = "✅ Başarılı" if success else "❌ Hata"
                print(f"{datetime.now().strftime('%H:%M:%S')} - {status} - CPU: {metrics['cpu_usage']:.1f}% RAM: {metrics['ram_usage']:.1f}%")
                
                # 30 saniye bekle
                await asyncio.sleep(30)
                
            except Exception as e:
                print(f"Monitor hatası: {e}")
                await asyncio.sleep(10)

if __name__ == "__main__":
    monitor = DeviceMonitor()
    asyncio.run(monitor.monitor_loop())
