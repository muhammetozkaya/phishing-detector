import re
import socket
import ssl
import whois
import os
from urllib.parse import urlparse
from datetime import datetime

# Load sample list of common safe root domains from file
TOP_DOMAINS = []
try:
    domains_file = os.path.join(os.path.dirname(__file__), "top_domains.txt")
    with open(domains_file, "r", encoding="utf-8") as f:
        TOP_DOMAINS = [line.strip().lower() for line in f if line.strip()]
except Exception as e:
    TOP_DOMAINS = ["google.com", "facebook.com", "amazon.com", "microsoft.com", "apple.com"]

SUSPICIOUS_WORDS = [
    "login", "verify", "secure", "bank", "update", "account",
    "password", "auth", "credential", "billing", "support",
    "service", "recover"
]

def analyze_url(url):
    """
    Analyzes a given URL for phishing indicators and returns a risk score
    along with detailed findings.
    """
    findings = []
    risk_score = 0
    
    # Ensure URL has a scheme for parsing
    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    try:
        parsed = urlparse(url)
        hostname = parsed.hostname
        if not hostname:
            return {"score": 100, "findings": [{"message": "Geçersiz URL formatı.", "type": "danger"}]}
    except Exception:
        return {"score": 100, "findings": [{"message": "URL ayrıştırılamadı.", "type": "danger"}]}

    # 1. IP Address Rule
    # Threat actors often use raw IP addresses instead of domain names
    ip_pattern = re.compile(r"^\d{1,3}(\.\d{1,3}){3}$")
    if ip_pattern.match(hostname):
        risk_score += 40
        findings.append({
            "message": "URL doğrudan bir IP adresi (Domain adı değil). Bu yaygın bir phishing taktiğidir.",
            "type": "danger"
        })
    else:
        # Extract root domain roughly (e.g., mail.google.com -> google.com)
        parts = hostname.split('.')
        root_domain = ".".join(parts[-2:]) if len(parts) >= 2 else hostname
        
        # 2. Top Domain Check
        if root_domain in TOP_DOMAINS:
            # If it's a known top domain (e.g., genuine google.com) 
            risk_score -= 20
            findings.append({
                "message": f"'{root_domain}' bilinen ve güvenilir bir platform olarak tespit edildi.",
                "type": "success"
            })
        else:
            # 3. Suspicious Words Check
            found_words = [word for word in SUSPICIOUS_WORDS if word in url.lower()]
            if found_words:
                risk_score += 25
                findings.append({
                    "message": f"URL içerisinde şüpheli kelimeler bulundu: {', '.join(found_words)}",
                    "type": "warning"
                })

            # 4. Long URL Check
            if len(url) > 75:
                risk_score += 15
                findings.append({
                    "message": f"URL çok uzun ({len(url)} karakter). Karmaşık adresler şüphelidir.",
                    "type": "warning"
                })

            # 5. Dash & Number Rules
            dash_count = hostname.count("-")
            if dash_count > 2:
                risk_score += 15
                findings.append({
                    "message": f"Domain adında çok fazla tire (-) var ({dash_count} adet).",
                    "type": "warning"
                })

            # 6. Domain Age (Whois)
            try:
                original_timeout = socket.getdefaulttimeout()
                socket.setdefaulttimeout(5.0)  # 5-second timeout for whois socket connections
                domain_info = whois.whois(root_domain)
                socket.setdefaulttimeout(original_timeout)
                
                creation_date = domain_info.creation_date
                
                # Handling lists returned by whois
                if type(creation_date) is list:
                    creation_date = creation_date[0]
                    
                if creation_date:
                    age_days = (datetime.now() - creation_date).days
                    if age_days < 30:
                        risk_score += 35
                        findings.append({
                            "message": f"Domain yaşı çok genç ({age_days} gün). Yeni açılan siteler yüksek risk taşır.",
                            "type": "danger"
                        })
                    elif age_days < 180:
                        risk_score += 10
                        findings.append({
                            "message": f"Domain nispeten yeni ({age_days} gün).",
                            "type": "warning"
                        })
                    else:
                        findings.append({
                            "message": f"Domain uzun süredir kullanımda ({age_days} gün).",
                            "type": "success"
                        })
                else:
                    findings.append({
                        "message": "Domain kayıt tarihi WHOIS sorgusu ile alınamadı.",
                        "type": "warning"
                    })
            except Exception as e:
                try:
                    socket.setdefaulttimeout(original_timeout)
                except:
                    pass
                findings.append({
                    "message": "WHOIS bilgisi sorgulanamadı (Ağ hatası veya 5 saniye zaman aşımı).",
                    "type": "warning"
                })

    # 7. SSL Certificate Check
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        with socket.create_connection((hostname, 443), timeout=5) as sock:
            with ctx.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert(binary_form=True)
                if cert:
                    findings.append({
                        "message": "SSL Sertifikası mevcut (HTTPS destekleniyor).",
                        "type": "success"
                    })
                else:
                    risk_score += 20
                    findings.append({
                        "message": "SSL sertifikası detayları okunamadı.",
                        "type": "warning"
                    })
    except Exception as e:
        risk_score += 20
        findings.append({
            "message": "Güvenli SSL/TLS bağlantısı (HTTPS) sağlanamadı.",
            "type": "danger"
        })

    # Normalize score between 0 and 100
    risk_score = max(0, min(100, risk_score))
    
    # Determine overall risk level
    if risk_score < 30:
        level = "Düşük Risk"
    elif risk_score < 60:
        level = "Orta Risk"
    else:
        level = "Yüksek Risk"

    return {
        "url": url,
        "score": risk_score,
        "level": level,
        "findings": findings,
        "timestamp": datetime.now().isoformat()
    }
