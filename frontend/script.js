document.addEventListener('DOMContentLoaded', () => {
    const urlInput = document.getElementById('urlInput');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const loadingDiv = document.getElementById('loading');
    const resultsCard = document.getElementById('resultsCard');
    const errorAlert = document.getElementById('errorAlert');
    const errorMessage = document.getElementById('errorMessage');
    
    const API_URL = 'http://127.0.0.1:5000/api/analyze';

    // UI Elements for Results
    const scoreValue = document.getElementById('scoreValue');
    const progressCircle = document.getElementById('progressCircle');
    const riskLevel = document.getElementById('riskLevel');
    const riskDesc = document.getElementById('riskDesc');
    const findingsList = document.getElementById('findingsList');
    const timestampSpan = document.getElementById('timestamp');

    // Trigger analysis on Enter key
    urlInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            analyzeUrl();
        }
    });

    analyzeBtn.addEventListener('click', analyzeUrl);

    async function analyzeUrl() {
        const url = urlInput.value.trim();
        if (!url) {
            showError("Lütfen analiz edilecek bir URL girin.");
            return;
        }

        // Reset UI
        hideError();
        resultsCard.classList.add('hidden');
        loadingDiv.classList.remove('hidden');
        analyzeBtn.disabled = true;

        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url: url })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || "Sunucu hatası oluştu.");
            }

            displayResults(data);

        } catch (error) {
            showError("Bağlantı hatası: Backend çalışmıyor olabilir. (" + error.message + ")");
        } finally {
            loadingDiv.classList.add('hidden');
            analyzeBtn.disabled = false;
        }
    }

    function displayResults(data) {
        // Formatted timestamp
        const date = new Date(data.timestamp);
        timestampSpan.textContent = date.toLocaleString('tr-TR');

        findingsList.innerHTML = '';
        const score = data.score;
        let color, description;

        // Reset Color Classes
        riskLevel.className = '';
        scoreValue.style.color = 'var(--text-main)';

        if (score < 30) {
            color = 'var(--success)';
            description = 'Bu URL güvenilir görünmektedir. Phishing göstergelerine rastlanmadı.';
            riskLevel.classList.add('status-success');
        } else if (score < 60) {
            color = 'var(--warning)';
            description = 'Bu URL bazı şüpheli unsurlar içeriyor. İşlem yaparken dikkatli olun.';
            riskLevel.classList.add('status-warning');
        } else {
            color = 'var(--danger)';
            description = 'DİKKAT! Yüksek riskli (Phishing) bağlantı. Verilerinizi girmeyiniz.';
            riskLevel.classList.add('status-danger');
            scoreValue.style.color = 'var(--danger)'; // Make numeric text red too
        }

        riskLevel.textContent = data.level;
        riskDesc.textContent = description;

        // Animate Circular Progress gauge
        animateScore(score, color);

        // Populate Findings
        if (data.findings && data.findings.length > 0) {
            data.findings.forEach(item => {
                const li = document.createElement('li');
                li.classList.add(`bg-${item.type}`); // Use bg-success/warning/danger for border color

                const icon = document.createElement('i');
                if (item.type === 'success') {
                    icon.className = 'fa-solid fa-circle-check status-success';
                } else if (item.type === 'warning') {
                    icon.className = 'fa-solid fa-triangle-exclamation status-warning';
                } else {
                    icon.className = 'fa-solid fa-circle-xmark status-danger';
                }

                const textSpan = document.createElement('span');
                textSpan.textContent = item.message;

                li.appendChild(icon);
                li.appendChild(textSpan);
                findingsList.appendChild(li);
            });
        }

        // Show card smoothly
        resultsCard.classList.remove('hidden');
    }

    function animateScore(targetScore, color) {
        let currentScore = 0;
        const duration = 1500; // ms
        const steps = 60;
        const increment = targetScore / steps;
        const stepTime = duration / steps;

        const timer = setInterval(() => {
            currentScore += increment;
            if (currentScore >= targetScore) {
                currentScore = targetScore;
                clearInterval(timer);
            }
            scoreValue.textContent = Math.round(currentScore) + '%';
            // Conic gradient dynamically updates
            progressCircle.style.background = `conic-gradient(${color} ${currentScore * 3.6}deg, rgba(255,255,255,0.05) ${currentScore * 3.6}deg)`;
        }, stepTime);
    }

    function showError(message) {
        errorMessage.textContent = message;
        errorAlert.classList.remove('hidden');
        resultsCard.classList.add('hidden');
    }

    function hideError() {
        errorAlert.classList.add('hidden');
    }
});
