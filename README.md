# 🧥 AI Moda - Akıllı Model Arama Uygulaması

Modern, yapay zeka destekli moda ürünleri arama ve yönetim platformu.

## ✨ Özellikler

- 🔍 **Akıllı Arama:** Tek kelime veya çok kelimeli aramalar (AND/OR mantığı)
- 🤖 **AI Analiz:** Yapay zeka ile otomatik etiketleme (kategori, renk, detaylar, aksesuarlar)
- 📝 **Düzenleme:** Ürün bilgilerini doğrudan detay sayfasından düzenleyin
- 🎨 **Modern Tasarım:** Yeşil tema, animasyonlu geçişler, responsive tasarım
- 📸 **Çoklu Görsel:** Ön, arka ve yan görünümler

## 🚀 Kurulum

### Yöntem 1: EXE Dosyası Oluşturma (ÖNERİLEN)

**Tek seferlik kurulum:**
1. `create_exe.bat` dosyasına çift tıklayın
2. Bekleyin (birkaç dakika sürebilir)
3. `dist` klasöründe `AI_Moda.exe` dosyası oluşacak

**Kullanım:**
1. `dist\AI_Moda.exe` dosyasına çift tıklayın
2. Tarayıcınızda `http://localhost:5000` adresini açın

**Paylaşım:**
- `AI_Moda.exe` dosyasını başkalarıyla paylaşabilirsiniz
- Python yüklü olmasına gerek yok!

### Yöntem 2: Manuel Kurulum

**Gereksinimler:**
- Python 3.7 veya üzeri

**Adımlar:**
```bash
# 1. run.bat dosyasına çift tıklayın
# VEYA manuel olarak:

# Sanal ortam oluştur
python -m venv venv

# Sanal ortamı aktif et (Windows)
venv\Scripts\activate

# Gereksinimleri yükle
pip install -r requirements.txt

# Uygulamayı başlat
python app.py
```

**Tarayıcıda açın:**
```
http://localhost:5000
```

## 📖 Kullanım

### Arama Yapma
1. Ana sayfada arama kutusuna kelime(ler) girin
2. **Tek kelime:** Tüm eşleşen ürünleri gösterir (örn: "etek")
3. **Çok kelime:** Sadece TÜM kelimeleri içeren ürünleri gösterir (örn: "yeşil etek")

### Ürün Ekleme
1. Sol menüden "Resim Yükleme" seçin
2. Ürün bilgilerini girin
3. Görselleri yükleyin (ön görünüm zorunlu)
4. "Yapay Zeka ile Analiz Et" butonuna basarak otomatik etiketleme yapın
5. Önerilen etiketleri seçin veya manuel ekleyin
6. "Yükle" butonuna basın

### Ürün Düzenleme
1. Bir ürüne tıklayın
2. Sağ üstteki "DÜZENLE" butonuna basın
3. Bilgileri güncelleyin
4. "KAYDET" butonuna basın

## 🗂️ Proje Yapısı
```
fashion-search-app/
├── app.py                 # Ana uygulama
├── run.bat               # Windows başlatma scripti
├── create_exe.bat        # EXE oluşturma scripti
├── requirements.txt      # Python bağımlılıkları
├── static/
│   ├── style.css        # Stil dosyası
│   ├── script.js        # JavaScript
│   └── uploads/         # Yüklenen görseller
└── templates/
    ├── base.html        # Ana şablon
    ├── index.html       # Arama sayfası
    ├── upload.html      # Yükleme sayfası
    └── detail.html      # Detay sayfası
```

## 🛠️ Teknolojiler

- **Backend:** Flask, SQLAlchemy
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **Veritabanı:** SQLite
- **Stil:** Google Fonts (Inter), Font Awesome
- **Paketleme:** PyInstaller

## 📝 Notlar

- Veritabanı otomatik olarak `fashion.db` dosyasında oluşturulur
- Yüklenen görseller `static/uploads/` klasöründe saklanır
- İlk çalıştırmada veritabanı boş olacaktır, ürün ekleyerek başlayın
- EXE dosyası ilk çalıştırmada biraz yavaş açılabilir (normaldir)

## 🐛 Sorun Giderme

**EXE oluşturulmuyor:**
- Python'un yüklü olduğundan emin olun: `python --version`
- İnternet bağlantınızı kontrol edin (PyInstaller indirilecek)

**EXE çalışmıyor:**
- Antivirüs programınız engelliyor olabilir, izin verin
- Windows Defender'ı geçici olarak kapatıp deneyin

**Uygulama başlamıyor:**
- Port 5000'in kullanımda olmadığından emin olun
- Başka bir Flask uygulaması çalışıyor olabilir

**Görseller görünmüyor:**
- `static/uploads/` klasörünün var olduğundan emin olun
- Dosya izinlerini kontrol edin

## 📄 Lisans

Bu proje eğitim amaçlıdır.

---

**Geliştirici:** AI Moda Ekibi  
**Versiyon:** 1.0.0  
**Son Güncelleme:** 2025
