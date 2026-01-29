#!/bin/bash

echo "🚀 DAKİTAI Panel Kurulumu Başlıyor..."

# Gerekli dizinleri oluştur
mkdir -p nginx/ssl
mkdir -p prometheus
mkdir -p mqtt

# Docker ve Docker Compose kontrolü
if ! command -v docker &> /dev/null; then
    echo "❌ Docker bulunamadı. Lütfen Docker'ı yükleyin."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose bulunamadı. Lütfen Docker Compose'u yükleyin."
    exit 1
fi

# Environment dosyası oluştur
if [ ! -f .env ]; then
    echo "📝 Environment dosyası oluşturuluyor..."
    cat > .env << EOF
POSTGRES_PASSWORD=dakitai123
GRAFANA_PASSWORD=admin123
JWT_SECRET=your-super-secret-jwt-key-here
AUTHENTIK_SECRET_KEY=your-authentik-secret-key-here
EOF
    echo "✅ .env dosyası oluşturuldu"
fi

# Frontend bağımlılıklarını yükle
echo "📦 Frontend bağımlılıkları yükleniyor..."
cd dakitai-panel
npm install
cd ..

echo "🐳 Docker servisleri başlatılıyor..."

# Veritabanını önce başlat
docker-compose up -d postgres redis

echo "⏳ Veritabanının hazır olması bekleniyor..."
sleep 10

# Diğer servisleri başlat
docker-compose up -d

echo "⏳ Servislerin başlaması bekleniyor..."
sleep 30

# Sağlık kontrolü
echo "🔍 Servis durumları kontrol ediliyor..."

if curl -f http://localhost:8000/api/health > /dev/null 2>&1; then
    echo "✅ API servisi çalışıyor"
else
    echo "❌ API servisi çalışmıyor"
fi

if curl -f http://localhost:3001 > /dev/null 2>&1; then
    echo "✅ Frontend servisi çalışıyor"
else
    echo "❌ Frontend servisi çalışmıyor"
fi

if curl -f http://localhost:3000 > /dev/null 2>&1; then
    echo "✅ Grafana servisi çalışıyor"
else
    echo "❌ Grafana servisi çalışmıyor"
fi

echo ""
echo "🎉 DAKİTAI Panel kurulumu tamamlandı!"
echo ""
echo "📋 Erişim Bilgileri:"
echo "   Panel: http://localhost (veya http://panel.dakiktabela.com)"
echo "   API: http://localhost:8000"
echo "   Grafana: http://localhost:3000 (admin/admin123)"
echo "   Node-RED: http://localhost:1880"
echo ""
echo "📚 Kullanım:"
echo "   - Panel üzerinden cihazlarınızı yönetebilirsiniz"
echo "   - Uzaktan erişim için cihazlara agent yükleyin"
echo "   - Grafana'da sistem metriklerini izleyin"
echo "   - Node-RED ile otomasyonlar oluşturun"
echo ""
echo "🔧 Yönetim Komutları:"
echo "   Durdur: docker-compose down"
echo "   Başlat: docker-compose up -d"
echo "   Loglar: docker-compose logs -f"
echo "   Güncelle: docker-compose pull && docker-compose up -d"
