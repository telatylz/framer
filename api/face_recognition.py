import cv2
import numpy as np
import base64
from typing import List, Dict, Optional
import os
import json
from datetime import datetime

class FaceRecognitionService:
    def __init__(self):
        # Haar Cascade yükle
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        
        # Yüz tanıma modeli (LBPH)
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        
        # Kayıtlı yüzler dizini
        self.faces_dir = "/app/data/faces"
        self.model_path = "/app/data/face_model.yml"
        
        # Dizinleri oluştur
        os.makedirs(self.faces_dir, exist_ok=True)
        
        # Model varsa yükle
        if os.path.exists(self.model_path):
            try:
                self.recognizer.read(self.model_path)
                self.is_trained = True
            except:
                self.is_trained = False
        else:
            self.is_trained = False
    
    def detect_faces(self, image_data: str) -> List[Dict]:
        """Base64 encoded görüntüden yüzleri tespit et"""
        try:
            # Base64'ü decode et
            image_bytes = base64.b64decode(image_data.split(',')[1] if ',' in image_data else image_data)
            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if img is None:
                return []
            
            # Gri tonlamaya çevir
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Yüzleri tespit et
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30)
            )
            
            detected_faces = []
            for i, (x, y, w, h) in enumerate(faces):
                face_data = {
                    'id': i,
                    'x': int(x),
                    'y': int(y),
                    'width': int(w),
                    'height': int(h),
                    'confidence': 0.0
                }
                
                # Eğer model eğitilmişse tanımaya çalış
                if self.is_trained:
                    face_roi = gray[y:y+h, x:x+w]
                    label, confidence = self.recognizer.predict(face_roi)
                    face_data['recognized_id'] = int(label)
                    face_data['confidence'] = float(confidence)
                    face_data['is_known'] = confidence < 100  # Eşik değeri
                
                detected_faces.append(face_data)
            
            return detected_faces
            
        except Exception as e:
            print(f"Yüz tespit hatası: {e}")
            return []
    
    def add_face(self, image_data: str, person_name: str, person_id: int) -> bool:
        """Yeni yüz ekle ve modeli yeniden eğit"""
        try:
            # Base64'ü decode et
            image_bytes = base64.b64decode(image_data.split(',')[1] if ',' in image_data else image_data)
            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if img is None:
                return False
            
            # Gri tonlamaya çevir
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Yüzleri tespit et
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 5)
            
            if len(faces) == 0:
                return False
            
            # İlk yüzü al
            (x, y, w, h) = faces[0]
            face_roi = gray[y:y+h, x:x+w]
            
            # Yüzü kaydet
            person_dir = os.path.join(self.faces_dir, str(person_id))
            os.makedirs(person_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            face_path = os.path.join(person_dir, f"{person_name}_{timestamp}.jpg")
            cv2.imwrite(face_path, face_roi)
            
            # Kişi bilgilerini kaydet
            info_path = os.path.join(person_dir, "info.json")
            info = {
                'id': person_id,
                'name': person_name,
                'added_date': datetime.now().isoformat(),
                'images': []
            }
            
            if os.path.exists(info_path):
                with open(info_path, 'r') as f:
                    info = json.load(f)
            
            info['images'].append({
                'path': face_path,
                'timestamp': timestamp
            })
            
            with open(info_path, 'w') as f:
                json.dump(info, f, indent=2)
            
            # Modeli yeniden eğit
            self.train_model()
            
            return True
            
        except Exception as e:
            print(f"Yüz ekleme hatası: {e}")
            return False
    
    def train_model(self) -> bool:
        """Kayıtlı yüzlerle modeli eğit"""
        try:
            faces = []
            labels = []
            
            # Tüm kayıtlı yüzleri yükle
            for person_id in os.listdir(self.faces_dir):
                person_dir = os.path.join(self.faces_dir, person_id)
                if not os.path.isdir(person_dir):
                    continue
                
                for image_file in os.listdir(person_dir):
                    if image_file.endswith('.jpg'):
                        image_path = os.path.join(person_dir, image_file)
                        face_img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                        if face_img is not None:
                            faces.append(face_img)
                            labels.append(int(person_id))
            
            if len(faces) > 0:
                # Modeli eğit
                self.recognizer.train(faces, np.array(labels))
                self.recognizer.save(self.model_path)
                self.is_trained = True
                return True
            
            return False
            
        except Exception as e:
            print(f"Model eğitim hatası: {e}")
            return False
    
    def get_registered_faces(self) -> List[Dict]:
        """Kayıtlı yüzlerin listesini getir"""
        registered_faces = []
        
        try:
            for person_id in os.listdir(self.faces_dir):
                person_dir = os.path.join(self.faces_dir, person_id)
                info_path = os.path.join(person_dir, "info.json")
                
                if os.path.exists(info_path):
                    with open(info_path, 'r') as f:
                        info = json.load(f)
                        registered_faces.append(info)
        
        except Exception as e:
            print(f"Kayıtlı yüzler listesi hatası: {e}")
        
        return registered_faces
    
    def delete_face(self, person_id: int) -> bool:
        """Kayıtlı yüzü sil"""
        try:
            person_dir = os.path.join(self.faces_dir, str(person_id))
            if os.path.exists(person_dir):
                import shutil
                shutil.rmtree(person_dir)
                
                # Modeli yeniden eğit
                self.train_model()
                return True
            
            return False
            
        except Exception as e:
            print(f"Yüz silme hatası: {e}")
            return False

# Global servis instance
face_service = FaceRecognitionService()
