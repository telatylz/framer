# DAKİTAI Panel - Profesyonel İşletme Yönetim Sistemi

Modern teknolojilerle geliştirilmiş kapsamlı işletme yönetim ve uzaktan kontrol paneli.

## 🚀 Özellikler

### 🖥️ Uzaktan Cihaz Kontrolü
- Yerel ağdaki bilgisayarları uzaktan kontrol
- Gerçek zamanlı ekran paylaşımı
- Dosya transferi ve terminal erişimi
- Çoklu platform desteği (Windows, Linux, macOS)

### 📊 Cihaz Yönetimi
- Otomatik ağ tarama ve cihaz keşfi
- Gerçek zamanlı durum izleme
- Performans metrikleri (CPU, RAM, Disk)
- Cihaz gruplandırma ve etiketleme

### 📈 İzleme ve Analitik
- Grafana entegrasyonu ile detaylı metrikler
- Prometheus ile veri toplama
- Gerçek zamanlı uyarılar
- Özelleştirilebilir dashboard'lar

### 🔧 Otomasyon
- Node-RED ile görsel otomasyon
- MQTT protokolü desteği
- Koşullu tetikleyiciler
- Zamanlı görevler

### 🏢 İşletme Yönetimi
- CRM (Müşteri İlişkileri Yönetimi)
- Proje takibi ve görev yönetimi
- Envanter yönetimi
- Raporlama sistemi

### 🔒 Güvenlik
- JWT tabanlı kimlik doğrulama
- Rol tabanlı erişim kontrolü
- SSL/TLS şifreleme
- Audit log kayıtları

## 🛠️ Teknoloji Stack

### Frontend
- **Next.js 14** - Modern React framework
- **TypeScript** - Tip güvenli geliştirme
- **Tailwind CSS** - Utility-first CSS framework
- **Framer Motion** - Animasyonlar
- **Lucide React** - Modern ikonlar

### Backend
- **FastAPI** - Yüksek performanslı Python API
- **PostgreSQL** - İlişkisel veritabanı
- **Redis** - Önbellek ve session yönetimi
- **WebSocket** - Gerçek zamanlı iletişim

### DevOps & Monitoring
- **Docker & Docker Compose** - Konteynerizasyon
- **Nginx** - Reverse proxy
- **Grafana** - Metrik görselleştirme
- **Prometheus** - Metrik toplama
- **Node-RED** - IoT ve otomasyon

### IoT & Communication
- **MQTT** - IoT cihaz iletişimi
- **WebRTC** - P2P bağlantılar
- **SSH/VNC** - Uzaktan erişim protokolleri

## 📋 Sistem Gereksinimleri

- **İşletim Sistemi:** Linux (Ubuntu 20.04+, Debian 11+, CentOS 8+)
- **RAM:** Minimum 4GB, Önerilen 8GB+
- **Disk:** Minimum 20GB boş alan
- **Network:** Gigabit Ethernet önerilir
- **Docker:** 20.10+
- **Docker Compose:** 2.0+

## 🚀 Hızlı Kurulum

```bash
# Repoyu klonla
git clone https://github.com/dakiktabela/dakitai-panel.git
cd dakitai-panel

# Kurulum scriptini çalıştır
./install.sh
```

## 📖 Detaylı Kurulum

### 1. Ön Gereksinimler

```bash
# Docker kurulumu (Ubuntu/Debian)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Docker Compose kurulumu
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 2. Proje Kurulumu

```bash
# Proje dizinini oluştur
mkdir -p /opt/dakitai
cd /opt/dakitai

# Kaynak kodları indir
git clone https://github.com/dakiktabela/dakitai-panel.git .

# Environment dosyasını düzenle
cp .env.example .env
nano .env
```

### 3. Servisleri Başlat

```bash
# Tüm servisleri başlat
docker-compose up -d

# Logları izle
docker-compose logs -f
```

## 🔧 Konfigürasyon

### Environment Değişkenleri

```env
# Veritabanı
POSTGRES_PASSWORD=güçlü-şifre-buraya
DATABASE_URL=postgresql://dakitai:şifre@postgres:5432/dakitai

# Güvenlik
JWT_SECRET=çok-güçlü-jwt-anahtarı
AUTHENTIK_SECRET_KEY=authentik-gizli-anahtarı

# Monitoring
GRAFANA_PASSWORD=grafana-admin-şifresi

# API
API_HOST=0.0.0.0
API_PORT=8000
```

### Nginx Konfigürasyonu

Panel'i özel domain ile erişilebilir yapmak için:

```nginx
server {
    listen 80;
    server_name panel.dakiktabela.com;
    
    location / {
        proxy_pass http://localhost:3001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 📱 Kullanım

### 1. İlk Giriş

1. Tarayıcıda `http://localhost` veya `http://panel.dakiktabela.com` adresine git
2. Varsayılan kullanıcı: `admin` / `admin123`
3. İlk girişte şifrenizi değiştirin

### 2. Cihaz Ekleme

1. **Cihaz Yönetimi** sayfasına git
2. **"Cihaz Ekle"** butonuna tıkla
3. Cihaz bilgilerini doldur
4. Otomatik keşif için **"Ağ Tarama"** kullan

### 3. Uzaktan Erişim

1. **Uzaktan Erişim** sayfasına git
2. Hedef cihaza **DAKİTAI Agent** yükle
3. **"Bağlan"** butonuna tıkla
4. Uzaktan kontrol başlar

### 4. Monitoring Kurulumu

1. **Grafana** (`http://localhost:3000`) açın
2. Admin hesabıyla giriş yapın
3. Prometheus datasource ekleyin
4. Dashboard'ları import edin

## 🔌 API Kullanımı

### Cihaz Listesi

```bash
curl -X GET "http://localhost:8000/api/devices" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Yeni Cihaz Ekleme

```bash
curl -X POST "http://localhost:8000/api/devices" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "name": "Ofis PC #1",
    "device_type": "computer",
    "ip_address": "192.168.1.100",
    "mac_address": "00:1B:44:11:3A:B7",
    "location": "Ofis"
  }'
```

### WebSocket Bağlantısı

```javascript
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('Gerçek zamanlı veri:', data);
};
```

## 🔧 Geliştirme

### Development Ortamı

```bash
# Frontend geliştirme
cd dakitai-panel
npm install
npm run dev

# Backend geliştirme
cd dakitai-api
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Yeni Özellik Ekleme

1. Feature branch oluştur: `git checkout -b feature/yeni-ozellik`
2. Değişiklikleri yap ve test et
3. Commit ve push: `git commit -m "Yeni özellik eklendi"`
4. Pull request oluştur

## 📊 Performans Optimizasyonu

### Veritabanı Optimizasyonu

```sql
-- Index'leri kontrol et
SELECT schemaname, tablename, indexname, indexdef 
FROM pg_indexes 
WHERE schemaname = 'public';

-- Slow query'leri analiz et
SELECT query, mean_time, calls 
FROM pg_stat_statements 
ORDER BY mean_time DESC 
LIMIT 10;
```

### Sistem Monitoring

```bash
# Container kaynak kullanımı
docker stats

# Sistem metrikleri
htop
iotop
nethogs
```

## 🛡️ Güvenlik

### SSL Sertifikası

```bash
# Let's Encrypt ile ücretsiz SSL
sudo apt install certbot
sudo certbot --nginx -d panel.dakiktabela.com
```

### Firewall Konfigürasyonu

```bash
# UFW ile temel güvenlik
sudo ufw enable
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw deny 3000/tcp  # Grafana'yı sadece local erişim
```

### Backup Stratejisi

```bash
# Otomatik yedekleme scripti
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
docker exec dakitai-postgres pg_dump -U dakitai dakitai > backup_$DATE.sql
tar -czf dakitai_backup_$DATE.tar.gz backup_$DATE.sql docker-compose.yml .env
```

## 🚨 Sorun Giderme

### Yaygın Sorunlar

**1. Container başlamıyor**
```bash
docker-compose logs container_name
docker-compose down && docker-compose up -d
```

**2. Veritabanı bağlantı hatası**
```bash
docker exec -it dakitai-postgres psql -U dakitai -d dakitai
```

**3. Port çakışması**
```bash
sudo netstat -tulpn | grep :8000
sudo lsof -i :8000
```

**4. Disk alanı doldu**
```bash
docker system prune -a
docker volume prune
```

### Log Analizi

```bash
# Tüm servislerin logları
docker-compose logs -f

# Belirli servis logları
docker-compose logs -f api
docker-compose logs -f frontend

# Sistem logları
journalctl -u docker
tail -f /var/log/nginx/error.log
```

## 📞 Destek

- **Dokümantasyon:** [https://docs.dakiktabela.com](https://docs.dakiktabela.com)
- **GitHub Issues:** [https://github.com/dakiktabela/dakitai-panel/issues](https://github.com/dakiktabela/dakitai-panel/issues)
- **E-posta:** support@dakiktabela.com
- **Telefon:** +90 XXX XXX XX XX

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/AmazingFeature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add some AmazingFeature'`)
4. Branch'inizi push edin (`git push origin feature/AmazingFeature`)
5. Pull Request oluşturun

## 📈 Roadmap

- [ ] Mobile uygulama (React Native)
- [ ] AI tabanlı anomali tespiti
- [ ] Blockchain entegrasyonu
- [ ] Multi-tenant mimari
- [ ] Kubernetes desteği
- [ ] Advanced reporting
- [ ] Video analytics
- [ ] Voice control

---

**DAKİTAI Panel** - Dakik Tabela tarafından geliştirilmiştir.
© 2026 Tüm hakları saklıdır.
