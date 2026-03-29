import unittest
from backend.analyzer import analyze_url

class TestAnalyzer(unittest.TestCase):
    
    def test_safe_domain(self):
        result = analyze_url("https://www.google.com")
        self.assertLess(result["score"], 30, "Google should be considered low risk.")
        self.assertEqual(result["level"], "Düşük Risk")

    def test_ip_address_url(self):
        result = analyze_url("http://192.168.1.1/login")
        self.assertGreaterEqual(result["score"], 40, "IP address URLs should increase risk score by at least 40.")
        
    def test_suspicious_words_in_url(self):
        result = analyze_url("http://some-random-domain.com/secure-login-verify")
        # Should detect suspicious words 'secure', 'login', 'verify'
        self.assertGreater(result["score"], 20, "Suspicious words should increase risk score.")
        
        # Verify findings list contains info about suspicious words
        found_suspicious_msg = any("şüpheli kelimeler" in finding["message"] for finding in result["findings"])
        self.assertTrue(found_suspicious_msg, "Findings should mention suspicious words.")

    def test_long_url(self):
        long_path = "a" * 80
        result = analyze_url(f"http://example.com/{long_path}")
        self.assertGreaterEqual(result["score"], 15, "Overly long URLs should increase risk score.")

    def test_excessive_dashes(self):
        result = analyze_url("http://www-paypal-login-secure-account.com")
        self.assertGreater(result["score"], 15, "Excessive dashes in domain should increase risk score.")

if __name__ == "__main__":
    unittest.main()
