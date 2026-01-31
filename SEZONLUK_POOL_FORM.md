# Champion Pool - Sezonluk + Form Güncellemesi

## 🎯 Yeni Algoritma

### İki Aşamalı Sistem

**1. Pool Eligibility (Sezonluk)**
- Son 100 maç analiz ediliyor
- Minimum **5 oyun** şartı (sezon boyunca)
- Tüm roller kapsanıyor

**2. Form Calculation (Son 20 Maç)**
- Son 20 maç analiz ediliyor
- Win rate hesaplanıyor
- Güncel form gösteriliyor

## 📊 Nasıl Çalışıyor?

```python
# 1. Sezonluk veriler (100 maç)
champion_season_stats = {
    'Malphite': {'games': 15, 'wins': 9},  # ✅ 5+ oyun, pool'a dahil
    'Garen': {'games': 8, 'wins': 5},      # ✅ 5+ oyun, pool'a dahil
    'Yasuo': {'games': 3, 'wins': 1}       # ❌ 5'ten az, pool'a dahil değil
}

# 2. Son form (20 maç)
champion_recent_stats = {
    'Malphite': {'games': 2, 'wins': 2},   # %100 form (son 20'de)
    'Garen': {'games': 5, 'wins': 2}       # %40 form (son 20'de)
}

# 3. Sonuç
Pool:
- Malphite: Season 15 oyun, Form %100 (son 20'de 2/2)
- Garen: Season 8 oyun, Form %40 (son 20'de 2/5)
- Yasuo: Pool'da yok (5'ten az)
```

## ✅ Avantajlar

**Sezonluk 5 Maç:**
- ✅ Tüm sezon boyunca oynadığı şampiyonlar dahil
- ✅ Multi-role oyuncular destekleniyor
- ✅ Eski ama deneyimli şampiyonlar dahil

**Son 20 Maç Form:**
- ✅ Güncel performans gösteriliyor
- ✅ "Şu an iyi oynuyor mu?" sorusuna cevap
- ✅ Score hesaplamasında güncel form kullanılıyor

## 🎮 Örnek Senaryo

**Oyuncu:**
- Sezon başında Malphite ile 20 oyun (15 galibiyet)
- Son zamanlarda oynamıyor (son 20 maçta 0 oyun)

**Eski Sistem:**
- ❌ Pool'da yok (son 20'de 5 oyun yok)

**Yeni Sistem:**
- ✅ Pool'da var (sezonluk 20 oyun)
- Form: %50 (default, son 20'de yok)
- Kullanıcı görebilir ve seçebilir!

## 🔧 Teknik Detaylar

**API Calls:**
- 100 maç metadata (hızlı)
- 100 maç detayı (yavaş ama gerekli)
- 20 maç detayı (form için)

**Optimizasyon:**
- İlk 20 maç hem sezon hem form için kullanılıyor
- Sadece 80 ek maç detayı çekiliyor
- Cache yapılabilir (gelecek için)
