# Flask Projesi Canlı Yayınlama Rehberi (Render.com & GitHub)

Harika! Projenizi babanızın ve herkesin erişebileceği bir web adresinde yayınlamak için tüm hazırlıkları yaptık. Sizin için `requirements.txt`, `Procfile` dosyalarını hazırladım ve yerel Git kurulumunu tamamladım.

Şimdi yapmanız gerekenleri en basit haliyle adım adım aşağıda anlatıyorum.

> [!WARNING]
> **Önemli Uyarı:** Render.com'un ücretsiz sürümünde (Free Tier), sunucu her yeniden başlatıldığında (veya yeni deploy yapıldığında) diskteki dosyalar **SIFIRLANIR**.
> Bu şu anlama gelir:
> 1. Sitenize yüklenen resimler silinebilir.
> 2. Veritabanı (SQLite) sıfırlanabilir ve üyeler/ürünler silinebilir.
>
> Kalıcı veri ve resim saklamak için ileride "Render PostgreSQL" (veritabanı için) ve "AWS S3/Cloudinary" (resimler için) gibi harici servisler kullanmanız gerekecektir. Şimdilik "Demo" amaçlı bu kurulum yeterlidir.

---

## 1. Adım: GitHub Deposu (Repository) Oluşturma

1. [GitHub.com](https://github.com) adresine gidin ve giriş yapın.
2. Sağ üst köşedeki **+** ikonuna tıklayıp **New repository** seçeneğini seçin.
3. **Repository name** kısmına bir isim verin (örneğin: `fashion-search-app`).
4. **Public** (Herkese açık) veya **Private** (Gizli) seçebilirsiniz (Private önerilir).
5. Diğer kutucukları işaretlemeyin (Readme, .gitignore vs. eklemeyin).
6. **Create repository** butonuna basın.

## 2. Adım: Projeyi GitHub'a Gönderme

Repository oluşturduktan sonra karşınıza çıkan sayfada **"…or push an existing repository from the command line"** başlığını göreceksiniz.

Bilgisayarınızdaki terminali ya da bu projenin olduğu komut satırını açın ve aşağıdaki komutları sırasıyla yapıştırıp Enter'a basın (Kendi GitHub kullanıcı adınızı ve repo adınızı yazdığınızdan emin olun):

```bash
# NOT: Aşağıdaki linki kendi oluşturduğunuz repo linkiyle değiştirin!
# Örnek: https://github.com/KULLANICI_ADINIZ/fashion-search-app.git

git remote add origin https://github.com/KULLANICI_ADINIZ/fashion-search-app.git
git branch -M main
git push -u origin main
```

Bu işlemden sonra GitHub sayfanızı yenilediğinizde dosyalarınızın orada olduğunu görmelisiniz.

---

## 3. Adım: Render.com Ayarları

1. [Render.com](https://render.com) adresine gidin ve giriş yapın (GitHub hesabı ile giriş yapabilirsiniz).
2. Sağ üst köşedeki **New +** butonuna tıklayın ve **Web Service**'i seçin.
3. **Connect a repository** bölümünde GitHub hesabınızı bağlayın ve az önce yüklediğiniz `fashion-search-app` projesini seçin (**Connect** diyerek).
4. Açılan ayar sayfasında şunları kontrol edin:
   - **Name:** Projenize bir isim verin (Bu site adresiniz olacak, örn: `fashion-app` -> `fashion-app.onrender.com`).
   - **Region:** `Frankfurt (EU Central)` seçebilirsiniz (Türkiye'ye yakın).
   - **Branch:** `main`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt` (Otomatik gelmeli)
   - **Start Command:** `gunicorn app:app` (Otomatik gelmeli, gelmezse elle yazın)
   - **Plan Type:** `Free` (Ücretsiz)

## 4. Adım: Ortam Değişkenleri (Environment Variables)

Projenizin çalışması için gizli anahtarlara ihtiyacı var. Render sayfasının aşağısında **Advanced** butonuna veya **Environment Variables** bölümüne gidin ve **Add Environment Variable** diyerek şunları ekleyin:

| Key | Value | Açıklama |
| :--- | :--- | :--- |
| `GEMINI_API_KEY` | `AIza...` | (Kendi Gemini API anahtarınızı yapıştırın) |
| `SECRET_KEY` | `gizli-bir-kelime-yazin` | Rastgele güvenli bir şifre/kelime |
| `PYTHON_VERSION` | `3.10.0` | (Opsiyonel) Python sürümü belirtmek için |

> **Not:** Veritabanı için `DATABASE_URL` eklemezseniz, proje otomatik olarak geçici bir SQLite veritabanı oluşturur.

## 5. Adım: Deploy (Yayınlama)

1. Sayfanın en altındaki **Create Web Service** butonuna tıklayın.
2. Render, projenizi inşa etmeye (build) başlayacak. Siyah bir terminal ekranında (Logs) işlemleri göreceksiniz.
3. İşlem bittiğinde **"Your service is live"** yazısını ve yeşil bir tik göreceksiniz.
4. Sol üstteki linke (örn: `https://fashion-app.onrender.com`) tıklayarak sitenize ulaşabilirsiniz!

Artık babanız bu linke tıklayarak sitenize girebilir. Bilgisayarınızda bir kod değiştirip `git push` yaptığınızda, Render bunu algılayıp sitenizi **otomatik olarak güncelleyecektir** (CI/CD).

Tebrikler! 🎉
