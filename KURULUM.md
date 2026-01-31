# LoL Personal Counter-Pick Engine - Kurulum ve Kullanım Rehberi

## 📋 Genel Bakış

Bu uygulama, League of Legends oyuncularının Riot Games API'sini kullanarak:
- Kullanıcının son maçlarını analiz eder
- Şampiyon ustalık puanlarını gösterir
- Belirli bir düşman şampiyona karşı en iyi counter-pick'leri önerir
- Kullanıcının şampiyon havuzundan dinamik öneriler sunar

**ÖNEMLİ:** Bu uygulama MOCK DATA kullanmaz, gerçek Riot API ile çalışır!

---

## 🔧 Gereksinimler

### Yazılım Gereksinimleri
- **Python 3.8+** (Backend için)
- **Node.js 16+** ve **npm** (Frontend için)
- **Riot Games API Key** (Ücretsiz)

### API Key Alma
1. [Riot Developer Portal](https://developer.riotgames.com/) adresine gidin
2. Riot hesabınızla giriş yapın
3. "Development API Key" oluşturun (24 saat geçerli)
4. Production için "Personal API Key" veya "Production API Key" başvurusu yapın

---

## 📦 Kurulum Adımları

### 1. Backend Kurulumu

#### a) Python Bağımlılıklarını Yükleyin
```bash
cd backend
pip install -r requirements.txt
```

**requirements.txt içeriği:**
```
fastapi
uvicorn
requests
python-dotenv
aiohttp
tenacity
pydantic
```

#### b) API Key Yapılandırması
`backend/.env` dosyasını düzenleyin:

```env
RIOT_API_KEY=RGAPI-XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
RATE_LIMIT_PER_SECOND=20
RATE_LIMIT_PER_TWO_MINUTES=100
```

> **DİKKAT:** `RIOT_API_KEY` değerini kendi API key'inizle değiştirin!

#### c) Backend'i Başlatın
```bash
cd backend
python main.py
```

veya

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend şu adreste çalışacak: `http://localhost:8000`

---

### 2. Frontend Kurulumu

#### a) Node.js Bağımlılıklarını Yükleyin
```bash
cd frontend
npm install
```

#### b) Frontend'i Başlatın
```bash
npm run dev
```

Frontend şu adreste çalışacak: `http://localhost:5173`

---

## 🎮 Kullanım

### 1. Uygulamayı Açın
Tarayıcınızda `http://localhost:5173` adresine gidin.

### 2. Oyuncu Bilgilerini Girin

**Summoner Name:** Riot ID formatında girin
- Örnek: `Faker#T1`
- Örnek: `YourName#TR1`
- Format: `İsim#Tag`

**Region:** Bölgenizi seçin
- TR - Turkey (tr1)
- EUW - West Europe (euw1)
- EUNE - Nordic & East (eun1)
- NA - North America (na1)
- KR - Korea (kr)
- vb.

**Target Enemy:** Karşı şampiyonun adını girin
- Örnek: `Darius`
- Örnek: `Yasuo`
- Örnek: `Zed`

### 3. Analiz Edin
"Find Counter-Picks" butonuna tıklayın.

### 4. Sonuçları İnceleyin
Uygulama size:
- **En iyi counter-pick'leri** gösterir (şampiyon havuzunuzdan)
- **Suitability Score** (0-100): Ne kadar uygun olduğunu gösterir
- **Global Win Rate:** Dünya genelinde bu matchup'taki kazanma oranı
- **Mastery Points:** Sizin o şampiyondaki ustalık puanınız
- **Recent Form:** Son maçlardaki performansınız

---

## 📊 Özellikler

### ✅ Gerçek Veri Analizi
- Riot Games API'den canlı veri çeker
- Kullanıcının gerçek şampiyon havuzunu analiz eder
- Son 20 maçı inceleyerek form durumunu hesaplar

### ✅ Akıllı Skorlama Sistemi
Skorlama 3 faktöre dayanır:
1. **Global Win Rate (45%):** Dünya genelinde bu matchup'taki başarı oranı
2. **Mastery Points (35%):** Şampiyondaki deneyiminiz
3. **Recent Performance (20%):** Son maçlardaki formunuz

### ✅ Dinamik Öneriler
- Sadece sizin oynadığınız şampiyonları önerir
- En çok oynadığınız 15 şampiyonu analiz eder
- Gerçek zamanlı veri ile güncellenir

---

## 🔍 Dosya Yapısı

```
riotapi/
├── backend/
│   ├── main.py              # FastAPI ana dosyası
│   ├── riot_client.py       # Riot API istemcisi
│   ├── scoring.py           # Skorlama motoru
│   ├── models.py            # Pydantic modelleri
│   ├── requirements.txt     # Python bağımlılıkları
│   └── .env                 # API key yapılandırması
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Ana React bileşeni
│   │   ├── main.jsx         # React giriş noktası
│   │   └── index.css        # Tailwind CSS stilleri
│   ├── index.html           # HTML şablonu
│   ├── package.json         # Node.js bağımlılıkları
│   ├── tailwind.config.js   # Tailwind yapılandırması
│   └── vite.config.js       # Vite yapılandırması
│
└── KURULUM.md              # Bu dosya
```

---

## 🛠️ Teknik Detaylar

### Backend API Endpoints

#### `GET /`
Sunucu durumunu kontrol eder.

**Response:**
```json
{
  "message": "LPC-Engine Backend [Real Riot API] is Running",
  "status": "ready"
}
```

#### `POST /recommend`
Counter-pick önerileri alır.

**Request Body:**
```json
{
  "summoner_name": "Faker",
  "tag_line": "T1",
  "region": "kr",
  "target_champion": "Zed"
}
```

**Response:**
```json
{
  "target_champion": "Zed",
  "recommendations": [
    {
      "champion_id": "Malphite",
      "champion_name": "Malphite",
      "score": 78.5,
      "details": {
        "global_wr": 0.56,
        "mastery": 250000,
        "recent_wr": 0.65
      }
    }
  ]
}
```

### Frontend Teknolojileri
- **React 18:** UI framework
- **Vite:** Build tool ve dev server
- **Tailwind CSS:** Styling
- **Axios:** HTTP istekleri
- **Framer Motion:** Animasyonlar

### Backend Teknolojileri
- **FastAPI:** Modern Python web framework
- **Uvicorn:** ASGI server
- **Requests/Aiohttp:** HTTP client
- **Tenacity:** Retry logic
- **Pydantic:** Data validation

---

## 🐛 Sorun Giderme

### Backend Başlamıyor
**Hata:** `RIOT_API_KEY not found in .env file!`
- **Çözüm:** `.env` dosyasında API key'inizi kontrol edin

**Hata:** `ModuleNotFoundError: No module named 'fastapi'`
- **Çözüm:** `pip install -r requirements.txt` komutunu çalıştırın

### Frontend Başlamıyor
**Hata:** `Cannot find module 'react'`
- **Çözüm:** `npm install` komutunu çalıştırın

**Hata:** `Port 5173 is already in use`
- **Çözüm:** Başka bir port kullanın: `npm run dev -- --port 3000`

### API Hataları
**Hata:** `Failed to fetch recommendations`
- **Çözüm:** Backend'in çalıştığından emin olun (`http://localhost:8000`)
- **Çözüm:** CORS ayarlarını kontrol edin

**Hata:** `Account not found`
- **Çözüm:** Summoner name formatını kontrol edin (`İsim#Tag`)
- **Çözüm:** Doğru region'u seçtiğinizden emin olun

**Hata:** `Rate limited`
- **Çözüm:** Development API key 24 saatte sınırlıdır, biraz bekleyin
- **Çözüm:** Production API key başvurusu yapın

### CORS Hataları
**Hata:** `Access to XMLHttpRequest blocked by CORS policy`
- **Çözüm:** Backend'de CORS middleware'inin aktif olduğundan emin olun
- **Çözüm:** `main.py` dosyasında `allow_origins=["*"]` ayarını kontrol edin

---

## 📝 Önemli Notlar

### API Key Güvenliği
- ✅ `.env` dosyasını asla Git'e commit etmeyin
- ✅ `.gitignore` dosyasına `.env` ekleyin
- ✅ Production'da environment variables kullanın

### Rate Limiting
- Development API Key: 20 istek/saniye, 100 istek/2 dakika
- Production API Key: Daha yüksek limitler
- Uygulama otomatik retry mekanizması içerir

### Veri Güncelliği
- Champion mastery: Gerçek zamanlı
- Match history: Son 20 maç
- Global counter data: Statik database (production'da U.GG/OP.GG API entegrasyonu önerilir)

---

## 🚀 Geliştirme Önerileri

### Production İçin
1. **Global Counter Data:** U.GG veya OP.GG API entegrasyonu
2. **Caching:** Redis ile API yanıtlarını cache'leyin
3. **Database:** Kullanıcı tercihlerini kaydedin
4. **Authentication:** Kullanıcı hesapları ekleyin
5. **Analytics:** Kullanım istatistikleri toplayın

### Özellik Fikirleri
- 🎯 Multi-role analizi (Top, Jungle, Mid, ADC, Support)
- 📊 Detaylı matchup istatistikleri
- 🏆 Rank-based öneriler (Bronze, Silver, Gold, vb.)
- 📈 Trend analizi (Meta şampiyonlar)
- 🎮 Team composition analizi

---

## 📞 Destek

### Faydalı Linkler
- [Riot Developer Portal](https://developer.riotgames.com/)
- [Riot API Documentation](https://developer.riotgames.com/apis)
- [Data Dragon](https://developer.riotgames.com/docs/lol#data-dragon)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)

### Hata Raporlama
Hata bulursanız veya öneriniz varsa:
1. Backend loglarını kontrol edin
2. Browser console'u kontrol edin
3. API yanıtlarını inceleyin

---

## ✅ Başarılı Kurulum Kontrolü

### Backend Kontrolü
```bash
curl http://localhost:8000
```
**Beklenen Yanıt:**
```json
{"message":"LPC-Engine Backend [Real Riot API] is Running","status":"ready"}
```

### Frontend Kontrolü
Tarayıcıda `http://localhost:5173` açıldığında:
- ✅ "LPC Engine" başlığı görünmeli
- ✅ Summoner Name, Region, Target Enemy inputları olmalı
- ✅ "Find Counter-Picks" butonu çalışmalı

### API Testi
Postman veya curl ile test edin:
```bash
curl -X POST http://localhost:8000/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "summoner_name": "Faker",
    "tag_line": "T1",
    "region": "kr",
    "target_champion": "Zed"
  }'
```

---

## 🎉 Başarıyla Kuruldu!

Artık LoL Personal Counter-Pick Engine'iniz hazır! İyi oyunlar! 🎮

**Not:** İlk kullanımda API yanıt süreleri biraz uzun olabilir (Riot API'den veri çekme süresi). Sonraki istekler daha hızlı olacaktır.
