<div align="center">
  <i class="fa-solid fa-shield-halved"></i>
  <h1>Phishing URL Detector 🛡️</h1>
  <p><b>Sezgisel ve kural tabanlı algoritmalarla URL güvenliğini analiz eden modern asistan.</b></p>
  
  <a href="https://github.com/muhammetozkaya/phishing-detector">
    <img src="https://img.shields.io/badge/GitHub-Repository-black?style=for-the-badge&logo=github">
  </a>
  <img src="https://img.shields.io/badge/Python-Flask-blue?style=for-the-badge&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/Frontend-Vanilla_JS-yellow?style=for-the-badge&logo=javascript&logoColor=black">
  <img src="https://img.shields.io/badge/UI-Glassmorphism-ff69b4?style=for-the-badge">
</div>

<br>

## 🚀 Genel Bakış

**Phishing URL Detector**, internet üzerinde tıkladığınız bağlantıların güvenliğini, makine kurallarına ve açık kaynak istihbaratlarına (WHOIS, SSL geçerlilik doğrulama vs.) dayanarak analiz eden profesyonel bir web uygulamasıdır. Backend için **Python (Flask)** kullanırken, ön yüz tarafında ise **HTML5, Vanilla JavaScript ve modern CSS (Cam Efekti)** mimarisiyle geliştirilmiştir.

Uygulama, bağlantı içerisindeki potansiyel oltalama (phishing) taktiklerini şu başlıca kıstaslara göre ölçer:
- Doğrudan IP adresi kullanımı (Domain maskeleme tespiti)
- Aşırı uzun URL'ler ve özel karakter (tire vb.) limit aşımları
- `login`, `secure`, `verify` vb. şüpheli yemleme kelimeleri analizi
- Algoritmik SSL (HTTPS) geçerliliği doğrulaması
- Güvenilir Alexa/Top sitelerle karşılaştırmalı doğrulama

👤 **Geliştiren:** Muhammet Özkaya

---

## 🎨 Arayüz (Frontend)

Saf (Vanilla) JavaScript ve CSS kullanılarak hiçbir dış tasarım kütüphanesine (Tailwind veya Bootstrap) ihtiyaç duymadan **Glassmorphism (Cam Efekti)** kullanılarak tasarlandı.
Dinamik risk göstergesi (Gauge Indicator) uygulanan kurallara göre yüzdelik oranı hesaplayıp yeşil 🟩, sarı 🟨 ya da kırmızı 🟥 uyarı durumuna geçer. Ek olarak, detaylı analiz bulguları dinamik liste olarak kartın hemen altında raporlanır.

---

## ⚙️ Kurulum ve Çalıştırma

Projeyi kendi ortamınızda test etmek için aşağıdaki adımları sırayla uygulayın:

### 1- Arka Sunucuyu Başlatın
Sisteminizde Python 3.8+ bulunduğundan emin olun. Terminalden (veya PowerShell'den) projenin ana klasörüne gidin:

```bash
# Sanal ortam oluşturup aktif hale getirme
python -m venv venv
.\venv\Scripts\activate   # Mac/Linux için: source venv/bin/activate

# Gerekli kütüphaneleri yükleme
pip install -r backend/requirements.txt

# API sunucusunu ayağa kaldırma
cd backend
python app.py
```
> Sunucu **http://127.0.0.1:5000** adresinde çalışmaya başlayacaktır.

### 2- Arayüze Erişin
Arka plan çalıştığı sürece herhangi bir web sunucusuna (Nginx, Apache vs.) ihtiyacınız yoktur.
Projedeki `frontend/index.html` dosyasına bir web tarayıcısından çift tıklayarak ulaşmanız uygulamanın çalışması için yeterlidir! Çıkan ekrandan URL girişlerinizi yapabilirsiniz.

---

## 📖 Endpoint ve API Kullanımı

Uygulama diğer otomasyon sistemlerine entegre edilebilir bir API olarak hizmet verir. Örnek bir JSON isteği (`POST /api/analyze`):

```json
{
    "url": "http://192.168.1.1/login.php"
}
```

Tüm taramalarınız projenin `backend/logs.json` dosyasına tarihi ile birlikte otomatik olarak kayıt edilir. Detaylı teknik rehberlik için **[Kullanım Kılavuzu (docs/usage.md)](docs/usage.md)** klasörünü inceleyebilirsiniz.

---

<div align="center">
  <sub>Bu proje <b>Muhammet Özkaya</b> tarafından geliştirilmiş açık kodlu bir yapıdır. Detaylar ve kaynak kodlar için <a href="https://github.com/muhammetozkaya/phishing-detector">Github Repo'sunu</a> ziyaret edebilirsiniz.</sub>
</div>
