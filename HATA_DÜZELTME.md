# 🔧 Hızlı Düzeltme: API Hataları

## ⚠️ SORUN: "Unknown apikey" Hatası (401)

Backend loglarınızda şu hatayı görüyorsunuz:
```
API Error 401: {"status":{"message":"Unknown apikey","status_code":401}}
Account not found: veydamn#tr1
```

### ✅ ÇÖZÜM: API Key'i Yenileyin

**Riot Development API Key'leri 24 saat sonra sona erer!**

#### Adım 1: Yeni API Key Alın
1. [https://developer.riotgames.com/](https://developer.riotgames.com/) adresine gidin
2. Riot hesabınızla giriş yapın
3. **"REGENERATE API KEY"** butonuna tıklayın
4. Yeni API key'i kopyalayın (RGAPI-... ile başlar)

#### Adım 2: .env Dosyasını Güncelleyin
1. `backend\.env` dosyasını açın
2. `RIOT_API_KEY=` satırını bulun
3. Eski key'i silin ve yeni key'i yapıştırın:
   ```env
   RIOT_API_KEY=RGAPI-BURAYA-YENİ-KEYİNİZİ-YAPIŞTIRIN
   ```
4. Dosyayı kaydedin (`Ctrl + S`)

#### Adım 3: Backend'i Yeniden Başlatın
1. Backend terminalinde `Ctrl + C` basın
2. Tekrar başlatın:
   ```bash
   python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```
   veya
   ```bash
   start_backend.bat
   ```

#### Adım 4: Test Edin
1. Frontend'de `Faker#T1` girin
2. `KR - Korea` seçin
3. `Yasuo` yazın
4. "Find Counter-Picks" tıklayın
5. Backend loglarında artık "200 OK" görmelisiniz! ✅

---

## 🔧 Diğer Olası Hatalar

### Sorun: 404 Hatası (/analyze endpoint)

Tarayıcınız **eski JavaScript dosyasını cache'lemiş**. Eski kod `/analyze` endpoint'ini çağırıyor ama backend'de sadece `/recommend` var.

### ✅ Çözüm (3 Seçenek)

### Seçenek 1: Hard Refresh (EN KOLAY) ⭐
Tarayıcıda şu tuş kombinasyonunu kullanın:

**Windows/Linux:**
```
Ctrl + Shift + R
```

veya

```
Ctrl + F5
```

**Mac:**
```
Cmd + Shift + R
```

### Seçenek 2: Cache Temizleme
1. Tarayıcıda `F12` basın (Developer Tools)
2. Network sekmesine gidin
3. "Disable cache" kutucuğunu işaretleyin
4. Sayfayı yenileyin (`F5`)

### Seçenek 3: Frontend'i Yeniden Başlatın
1. Frontend terminalinde `Ctrl + C` basın
2. Tekrar çalıştırın:
   ```bash
   npm run dev
   ```
3. Tarayıcıda `http://localhost:5173` açın

## ✅ Test Edin
1. Sayfayı yeniledikten sonra
2. `F12` basın → Console sekmesi
3. "Find Counter-Picks" butonuna tıklayın
4. Artık `/recommend` endpoint'ini çağırmalı (404 hatası olmamalı)

## 📝 Neden Oldu?
- Vite dev server bazen eski dosyaları cache'ler
- Tarayıcı da JavaScript dosyalarını cache'ler
- Hard refresh her ikisini de temizler

---

**Hızlı Test:**
1. `Ctrl + Shift + R` basın
2. `Faker#T1` girin
3. `KR - Korea` seçin  
4. `Yasuo` yazın
5. "Find Counter-Picks" tıklayın
6. Şampiyonlar görünmeli! 🎮
