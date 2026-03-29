# Phishing URL Detector Kullanım Kılavuzu

Uygulamanın hem arayüz (Frontend) üzerinden hem de API olarak nasıl kullanılacağına dair detaylar aşağıda listelenmiştir.

## 1. Web Arayüzü Kullanımı

1. Projeyi çalıştırdıktan sonra tarayıcınızdan `frontend/index.html` dosyasını açarak (veya bir canlı sunucu eklentisi yardımıyla) sayfaya erişin.
2. Ekranda ortalanmış olan URL giriş kutusuna, şüphelendiğiniz internet bağlantısını tam formatta girin. (Örn: `https://example.com/login`)
3. **Analiz Et** butonuna tıklayın veya "Enter" tuşuna basın.
4. "URL taranıyor..." mesajından sonra, ekran üzerinde beliren "Analiz Sonucu" kartından şu bilgileri görebilirsiniz:
   - **Risk Yüzdesi**: Animasyonlu halka üzerinde belirtilen skor (%0 - %100 arası).
   - **Risk Seviyesi**: Güvenli (Yeşil), Orta Şüpheli (Sarı), Yüksek Risk (Kırmızı).
   - **Detaylı Bulgular**: Hangi kuralların tetiklendiğini, SSL sertifikasının durumu ve Domain kayıt bilgisini anlatan liste.

## 2. API Üzerinden Kullanım (Geliştiriciler)

Arka planda çalışan Flask sunucusuna `POST` metoduyla istek yaparak URL analizini kendi otomatize sistemlerinize bağlayabilirsiniz. Sistem her sorguyu `backend/logs.json` dosyasına da kaydeder.

**Endpoint:**
`POST http://127.0.0.1:5000/api/analyze`

**Header:**
`Content-Type: application/json`

**Body Örneği:**
```json
{
    "url": "http://192.168.1.1/login.php"
}
```

**Yanıt Örneği:**
```json
{
    "url": "http://192.168.1.1/login.php",
    "score": 80,
    "level": "Yüksek Risk",
    "findings": [
        {
            "message": "URL doğrudan bir IP adresi (Domain adı değil). Bu yaygın bir phishing taktiğidir.",
            "type": "danger"
        },
        {
            "message": "URL içerisinde şüpheli kelimeler bulundu: login",
            "type": "warning"
        },
        {
            "message": "Güvenli SSL/TLS bağlantısı (HTTPS) sağlanamadı.",
            "type": "danger"
        }
    ],
    "timestamp": "2026-03-29T15:00:00.000000"
}
```

Eğer API'ye sorunlu bir format gönderirseniz (örneğin "url" alanı yoksa), sunucu 400 Bad Request statü kodunu `"error"` mesajı ile döndürür.
