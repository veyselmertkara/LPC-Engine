# U.GG API Entegrasyonu - Gerçek Zamanlı Counter Data

## 🎯 Amaç
Statik counter database yerine U.GG'den gerçek zamanlı counter data çekmek.

## ⚠️ Önemli Bilgi
U.GG'nin **resmi public API'si yok**. Ancak birkaç alternatif var:

### Seçenek 1: U.GG Web Scraping (Tavsiye Edilmez)
- U.GG web sitesini scrape etmek
- ❌ Terms of Service ihlali olabilir
- ❌ Site yapısı değişirse bozulur
- ❌ Rate limiting sorunları

### Seçenek 2: Community Dragon API ✅ (ÖNERİLEN)
- Riot'un Data Dragon'ının community versiyonu
- ✅ Ücretsiz ve legal
- ✅ Champion stats, items, runes vb.
- ❌ Counter data yok (sadece base stats)

### Seçenek 3: OP.GG / Mobalytics / Lolalytics
- Bu siteler de public API sunmuyor
- Benzer scraping sorunları

### Seçenek 4: Hybrid Yaklaşım ✅ (EN PRATİK)
- **Riot API** → Oyuncu data (mastery, match history)
- **Statik Database** → Counter matchups (mevcut sistemimiz)
- **Periyodik Güncelleme** → Database'i manuel/otomatik güncelle

## 🚀 Önerilen Çözüm

### Kısa Vadeli (Şu An)
Mevcut statik database'i kullanmaya devam edin. 100+ şampiyon kapsıyor ve test için yeterli.

### Orta Vadeli (Geliştirme)
1. **Community API Kullan**: Lolalytics veya benzeri community API'ler
2. **Web Scraping**: Dikkatli ve etik şekilde
3. **Crowdsourcing**: Kullanıcılardan veri topla

### Uzun Vadeli (Production)
1. **Ücretli API**: Mobalytics, Blitz.gg gibi servislerin API'leri
2. **Kendi Veritabanı**: Maç verilerini analiz edip kendi counter data'nızı oluşturun
3. **Machine Learning**: Riot API'den match data çekip ML ile counter'ları tahmin edin

## 💡 Pratik Çözüm: Lolalytics API

Lolalytics'in unofficial API'si var. Örnek:

```python
import requests

def get_lolalytics_counters(champion_name):
    # Lolalytics unofficial endpoint (değişebilir!)
    url = f"https://axe.lolalytics.com/tierlist/1/?lane=default&patch=30&tier=platinum_plus&queue=420&region=all"
    
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    
    response = requests.get(url, headers=headers)
    data = response.json()
    
    # Parse counter data
    # ...
    
    return counters
```

**Sorun:** Bu endpoint'ler dokümante değil ve her an değişebilir.

## ✅ Şu Anki En İyi Yaklaşım

### 1. Mevcut Sistemi Kullan
- 100+ şampiyon için counter data var
- Test ve development için yeterli
- Hızlı ve güvenilir

### 2. Database'i Periyodik Güncelle
- Haftada bir U.GG/OP.GG'den manuel kontrol
- Popüler şampiyonların counter'larını güncelle
- Meta değişikliklerini takip et

### 3. Generic Fallback Ekle
Database'de olmayan şampiyonlar için role-based counter'lar:

```python
ROLE_COUNTERS = {
    'tank': ['Fiora', 'Vayne', 'Gwen', 'Mordekaiser', 'Kayle'],
    'assassin': ['Malphite', 'Galio', 'Lissandra', 'Renekton', 'Pantheon'],
    'mage': ['Zed', 'Fizz', 'Kassadin', 'Yasuo', 'Sylas'],
    'marksman': ['Zed', 'Rengar', 'Kha\'Zix', 'Hecarim', 'Nocturne'],
    'support': ['Blitzcrank', 'Pyke', 'Nautilus', 'Leona', 'Thresh']
}
```

## 🔧 Hemen Yapılabilecekler

### Adım 1: Generic Counter Sistemi Ekle
```python
def get_champion_role(champion_name):
    # Data Dragon'dan şampiyon role'ünü al
    # Veya statik mapping kullan
    pass

def get_generic_counters(champion_name):
    role = get_champion_role(champion_name)
    return ROLE_COUNTERS.get(role, DEFAULT_COUNTERS)
```

### Adım 2: Fallback Mekanizması
```python
def get_global_counters(self, target_champion: str):
    # Önce database'e bak
    if target_champion in COUNTER_DATABASE:
        return COUNTER_DATABASE[target_champion]
    
    # Yoksa role-based counter'lar döndür
    return get_generic_counters(target_champion)
```

## 📝 Sonuç

**Şu an için en iyi çözüm:**
1. ✅ Mevcut statik database'i kullan (100+ şampiyon)
2. ✅ Generic role-based fallback ekle (eksik şampiyonlar için)
3. ✅ Database'i manuel olarak güncelle (meta değişikliklerinde)

**Gelecek için:**
- Lolalytics veya benzeri unofficial API'leri araştır
- Kendi match data analysis sisteminizi kurun
- Ücretli API servisleri değerlendirin

---

## 🎮 Hemen Uygulayalım mı?

Size generic role-based fallback sistemini ekleyeyim mi? Bu sayede database'de olmayan şampiyonlar için de mantıklı counter'lar döndürürüz.
