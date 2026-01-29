import React, { useState, useRef, useCallback } from 'react';
import { Camera, Users, UserPlus, Trash2, Eye, EyeOff } from 'lucide-react';

const FaceRecognition = () => {
  const [isActive, setIsActive] = useState(false);
  const [registeredFaces, setRegisteredFaces] = useState([]);
  const [detectedFaces, setDetectedFaces] = useState([]);
  const [isRegistering, setIsRegistering] = useState(false);
  const [newPersonName, setNewPersonName] = useState('');
  const [newPersonId, setNewPersonId] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const streamRef = useRef(null);

  // Kamera başlat
  const startCamera = useCallback(async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ 
        video: { width: 640, height: 480 } 
      });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        streamRef.current = stream;
        setIsActive(true);
      }
    } catch (error) {
      console.error('Kamera erişim hatası:', error);
      alert('Kamera erişimi reddedildi veya mevcut değil');
    }
  }, []);

  // Kamera durdur
  const stopCamera = useCallback(() => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      streamRef.current = null;
    }
    if (videoRef.current) {
      videoRef.current.srcObject = null;
    }
    setIsActive(false);
    setDetectedFaces([]);
  }, []);

  // Görüntüyü base64'e çevir
  const captureImage = useCallback(() => {
    if (!videoRef.current || !canvasRef.current) return null;
    
    const canvas = canvasRef.current;
    const video = videoRef.current;
    const ctx = canvas.getContext('2d');
    
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    ctx.drawImage(video, 0, 0);
    
    return canvas.toDataURL('image/jpeg', 0.8);
  }, []);

  // Yüz tespit et
  const detectFaces = useCallback(async () => {
    const imageData = captureImage();
    if (!imageData) return;

    setIsLoading(true);
    try {
      const response = await fetch('/api/face/detect', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({ image: imageData })
      });

      if (response.ok) {
        const data = await response.json();
        setDetectedFaces(data.faces);
      } else {
        console.error('Yüz tespit hatası');
      }
    } catch (error) {
      console.error('API hatası:', error);
    } finally {
      setIsLoading(false);
    }
  }, [captureImage]);

  // Yüz kaydet
  const registerFace = useCallback(async () => {
    if (!newPersonName || !newPersonId) {
      alert('Lütfen isim ve ID girin');
      return;
    }

    const imageData = captureImage();
    if (!imageData) return;

    setIsLoading(true);
    try {
      const response = await fetch('/api/face/add', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({
          image: imageData,
          person_name: newPersonName,
          person_id: parseInt(newPersonId)
        })
      });

      if (response.ok) {
        alert('Yüz başarıyla kaydedildi!');
        setNewPersonName('');
        setNewPersonId('');
        setIsRegistering(false);
        loadRegisteredFaces();
      } else {
        const error = await response.json();
        alert(`Hata: ${error.detail}`);
      }
    } catch (error) {
      console.error('API hatası:', error);
      alert('Kayıt sırasında hata oluştu');
    } finally {
      setIsLoading(false);
    }
  }, [newPersonName, newPersonId, captureImage]);

  // Kayıtlı yüzleri yükle
  const loadRegisteredFaces = useCallback(async () => {
    try {
      const response = await fetch('/api/face/registered', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (response.ok) {
        const data = await response.json();
        setRegisteredFaces(data.registered_faces);
      }
    } catch (error) {
      console.error('Kayıtlı yüzler yüklenemedi:', error);
    }
  }, []);

  // Yüz sil
  const deleteFace = useCallback(async (personId) => {
    if (!confirm('Bu yüzü silmek istediğinizden emin misiniz?')) return;

    try {
      const response = await fetch(`/api/face/${personId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (response.ok) {
        alert('Yüz başarıyla silindi');
        loadRegisteredFaces();
      } else {
        alert('Silme işlemi başarısız');
      }
    } catch (error) {
      console.error('Silme hatası:', error);
    }
  }, [loadRegisteredFaces]);

  // Otomatik tespit
  React.useEffect(() => {
    if (!isActive || isRegistering) return;

    const interval = setInterval(() => {
      detectFaces();
    }, 2000); // 2 saniyede bir tespit

    return () => clearInterval(interval);
  }, [isActive, isRegistering, detectFaces]);

  // Sayfa yüklendiğinde kayıtlı yüzleri getir
  React.useEffect(() => {
    loadRegisteredFaces();
  }, [loadRegisteredFaces]);

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Yüz Tanıma Sistemi</h1>
        <p className="text-gray-600">Kamera ile yüz tespit etme ve kaydetme</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Kamera Bölümü */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold flex items-center">
              <Camera className="mr-2" size={24} />
              Kamera
            </h2>
            <div className="flex gap-2">
              {!isActive ? (
                <button
                  onClick={startCamera}
                  className="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-lg flex items-center"
                >
                  <Eye className="mr-2" size={16} />
                  Başlat
                </button>
              ) : (
                <button
                  onClick={stopCamera}
                  className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg flex items-center"
                >
                  <EyeOff className="mr-2" size={16} />
                  Durdur
                </button>
              )}
            </div>
          </div>

          <div className="relative">
            <video
              ref={videoRef}
              autoPlay
              playsInline
              className="w-full h-64 bg-gray-200 rounded-lg object-cover"
            />
            <canvas ref={canvasRef} className="hidden" />
            
            {/* Tespit edilen yüzler */}
            {detectedFaces.map((face, index) => (
              <div
                key={index}
                className="absolute border-2 border-green-400"
                style={{
                  left: `${(face.x / 640) * 100}%`,
                  top: `${(face.y / 480) * 100}%`,
                  width: `${(face.width / 640) * 100}%`,
                  height: `${(face.height / 480) * 100}%`,
                }}
              >
                {face.is_known && (
                  <div className="absolute -top-6 left-0 bg-green-500 text-white px-2 py-1 rounded text-xs">
                    ID: {face.recognized_id}
                  </div>
                )}
              </div>
            ))}
          </div>

          {isActive && (
            <div className="mt-4 flex gap-2">
              <button
                onClick={detectFaces}
                disabled={isLoading}
                className="bg-blue-500 hover:bg-blue-600 disabled:bg-gray-400 text-white px-4 py-2 rounded-lg flex-1"
              >
                {isLoading ? 'Tespit Ediliyor...' : 'Yüz Tespit Et'}
              </button>
              <button
                onClick={() => setIsRegistering(!isRegistering)}
                className="bg-purple-500 hover:bg-purple-600 text-white px-4 py-2 rounded-lg flex items-center"
              >
                <UserPlus className="mr-2" size={16} />
                {isRegistering ? 'İptal' : 'Kaydet'}
              </button>
            </div>
          )}

          {/* Yüz kaydetme formu */}
          {isRegistering && (
            <div className="mt-4 p-4 bg-gray-50 rounded-lg">
              <h3 className="font-semibold mb-3">Yeni Yüz Kaydet</h3>
              <div className="space-y-3">
                <input
                  type="text"
                  placeholder="Kişi Adı"
                  value={newPersonName}
                  onChange={(e) => setNewPersonName(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <input
                  type="number"
                  placeholder="Kişi ID"
                  value={newPersonId}
                  onChange={(e) => setNewPersonId(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <button
                  onClick={registerFace}
                  disabled={isLoading}
                  className="w-full bg-green-500 hover:bg-green-600 disabled:bg-gray-400 text-white px-4 py-2 rounded-lg"
                >
                  {isLoading ? 'Kaydediliyor...' : 'Kaydet'}
                </button>
              </div>
            </div>
          )}
        </div>

        {/* Kayıtlı Yüzler */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold flex items-center">
              <Users className="mr-2" size={24} />
              Kayıtlı Yüzler ({registeredFaces.length})
            </h2>
            <button
              onClick={loadRegisteredFaces}
              className="bg-gray-500 hover:bg-gray-600 text-white px-3 py-1 rounded text-sm"
            >
              Yenile
            </button>
          </div>

          <div className="space-y-3 max-h-96 overflow-y-auto">
            {registeredFaces.length === 0 ? (
              <p className="text-gray-500 text-center py-8">Henüz kayıtlı yüz yok</p>
            ) : (
              registeredFaces.map((person) => (
                <div key={person.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div>
                    <div className="font-semibold">{person.name}</div>
                    <div className="text-sm text-gray-600">ID: {person.id}</div>
                    <div className="text-xs text-gray-500">
                      {person.images?.length || 0} görüntü
                    </div>
                  </div>
                  <button
                    onClick={() => deleteFace(person.id)}
                    className="bg-red-500 hover:bg-red-600 text-white p-2 rounded-lg"
                  >
                    <Trash2 size={16} />
                  </button>
                </div>
              ))
            )}
          </div>
        </div>
      </div>

      {/* Tespit Sonuçları */}
      {detectedFaces.length > 0 && (
        <div className="mt-6 bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-xl font-semibold mb-4">Tespit Sonuçları</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {detectedFaces.map((face, index) => (
              <div key={index} className="p-4 bg-gray-50 rounded-lg">
                <div className="text-sm space-y-1">
                  <div><strong>Yüz #{index + 1}</strong></div>
                  <div>Konum: ({face.x}, {face.y})</div>
                  <div>Boyut: {face.width}x{face.height}</div>
                  {face.is_known ? (
                    <div className="text-green-600">
                      <strong>Tanınan Kişi ID: {face.recognized_id}</strong>
                      <br />
                      Güven: {(100 - face.confidence).toFixed(1)}%
                    </div>
                  ) : (
                    <div className="text-orange-600">Bilinmeyen kişi</div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default FaceRecognition;
