document.addEventListener('DOMContentLoaded', () => {
    const onboardingScreen = document.getElementById('onboarding-screen');
    const animationLayer = document.getElementById('animation-layer');
    const startBtn = document.getElementById('start-btn');
    const centerIcon = document.querySelector('.center-icon');

    // Sadece ana sayfada ve daha önce girilmediyse göster
    if (window.location.pathname === '/' && !sessionStorage.getItem('visited')) {
        if (onboardingScreen) onboardingScreen.style.display = 'flex';
    } else {
        if (onboardingScreen) onboardingScreen.style.display = 'none';
    }

    const backBtn = document.getElementById('back-to-onboarding');
    if (backBtn) {
        backBtn.addEventListener('click', (e) => {
            e.preventDefault();
            // Eğer ana sayfada değilsek ana sayfaya git, sonra onboarding'i aç
            if (window.location.pathname !== '/') {
                sessionStorage.removeItem('visited');
                window.location.href = '/';
            } else {
                if (onboardingScreen) {
                    onboardingScreen.style.display = 'flex';
                    onboardingScreen.style.opacity = '1';
                    sessionStorage.removeItem('visited');
                }
            }
        });
    }

    if (startBtn) {
        startBtn.addEventListener('click', () => {
            // Gecikme olmadan hemen animasyonu başlat
            onboardingScreen.style.display = 'none';
            startAnimation();
        });
    }

    function startAnimation() {
        animationLayer.style.display = 'block';

        const icons = ['👕', '👗', '👖', '🧥', '👠', '🧢', '👜', '🕶️'];
        const numItems = 15;

        for (let i = 0; i < numItems; i++) {
            const el = document.createElement('div');
            el.classList.add('anim-item');
            el.innerText = icons[Math.floor(Math.random() * icons.length)];

            // Random start positions
            const startX = (Math.random() - 0.5) * 200 + 'vw';
            const startY = (Math.random() - 0.5) * 200 + 'vh';

            el.style.setProperty('--start-x', startX);
            el.style.setProperty('--start-y', startY);
            el.style.left = '50%';
            el.style.top = '50%';
            el.style.animation = `flyIn 1.5s ease-in forwards ${Math.random() * 0.5}s`;

            animationLayer.appendChild(el);
        }

        setTimeout(() => {
            centerIcon.classList.add('active');
        }, 1200);

        setTimeout(() => {
            animationLayer.style.opacity = '0';
            animationLayer.style.transition = 'opacity 0.5s';
            sessionStorage.setItem('visited', 'true');
            setTimeout(() => {
                animationLayer.style.display = 'none';
            }, 500);
        }, 2000);
    }

    // AI Analysis Simulation
    const aiAnalyzeBtn = document.getElementById('ai-analyze-btn');
    const aiLoading = document.getElementById('ai-loading');
    const aiSuggestions = document.getElementById('ai-suggestions');
    const suggestionContainer = document.getElementById('suggestion-container');
    const applySuggestionsBtn = document.getElementById('apply-suggestions');
    const featuresInput = document.getElementById('features-input');

    if (aiAnalyzeBtn) {
        aiAnalyzeBtn.addEventListener('click', () => {
            aiLoading.style.display = 'inline-block';
            aiAnalyzeBtn.disabled = true;
            aiSuggestions.style.display = 'none';
            suggestionContainer.innerHTML = '';

            // Call Mock API
            fetch('/api/analyze', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    aiLoading.style.display = 'none';
                    aiAnalyzeBtn.disabled = false;
                    aiSuggestions.style.display = 'block';

                    // Helper to create category group
                    const createGroup = (title, items, prefix) => {
                        if (!items || (Array.isArray(items) && items.length === 0)) return;

                        const group = document.createElement('div');
                        group.style.marginBottom = '10px';

                        const groupTitle = document.createElement('div');
                        groupTitle.style.cssText = 'color: #ccc; font-size: 0.9rem; margin-bottom: 5px; border-bottom: 1px solid #3e5871; padding-bottom: 2px;';
                        groupTitle.innerText = title;
                        group.appendChild(groupTitle);

                        const tagsDiv = document.createElement('div');
                        tagsDiv.style.cssText = 'display: flex; flex-wrap: wrap; gap: 8px;';

                        const itemList = Array.isArray(items) ? items : [items];

                        itemList.forEach(item => {
                            const tagEl = document.createElement('div');
                            tagEl.style.cssText = 'background: #1e2a3c; color: #fff; padding: 4px 10px; border-radius: 15px; font-size: 0.85rem; cursor: pointer; border: 1px solid #3e5871; transition: all 0.2s;';
                            tagEl.innerText = item;
                            tagEl.dataset.value = prefix ? `${prefix}:${item}` : item;

                            tagEl.onclick = () => {
                                addTagToInput(tagEl.dataset.value);
                                tagEl.style.background = '#00e5ff';
                                tagEl.style.color = '#1e2a3c';
                                tagEl.style.borderColor = '#00e5ff';
                            };
                            tagsDiv.appendChild(tagEl);
                        });

                        group.appendChild(tagsDiv);
                        suggestionContainer.appendChild(group);
                    };

                    createGroup('Ana Ürün', data.category, 'kategori');
                    createGroup('Renk', data.color, 'renk');
                    createGroup('Detaylar', data.details, 'detay');
                    createGroup('Aksesuarlar', data.accessories, 'aksesuar');

                })
                .catch(err => {
                    console.error(err);
                    aiLoading.style.display = 'none';
                    aiAnalyzeBtn.disabled = false;
                    alert('Analiz sırasında bir hata oluştu.');
                });
        });
    }

    if (applySuggestionsBtn) {
        applySuggestionsBtn.addEventListener('click', () => {
            const allTags = suggestionContainer.querySelectorAll('div[data-value]');
            allTags.forEach(tagEl => {
                addTagToInput(tagEl.dataset.value);
                tagEl.style.background = '#00e5ff';
                tagEl.style.color = '#1e2a3c';
                tagEl.style.borderColor = '#00e5ff';
            });
        });
    }

    function addTagToInput(tag) {
        let currentVal = featuresInput.value;
        // Clean up spaces
        tag = tag.trim();

        if (currentVal) {
            // Check if tag already exists to avoid duplicates
            const parts = currentVal.split(',').map(s => s.trim());
            if (!parts.includes(tag)) {
                featuresInput.value = currentVal + ', ' + tag;
            }
        } else {
            featuresInput.value = tag;
        }
    }
});

function resimDegistir(yeniResimYolu) {
    // 1. Büyük resmi bul (ID'si 'anaGorsel' olsun)
    var buyukResim = document.getElementById("anaGorsel");

    // 2. Onun 'src' (kaynak) özelliğini değiştir
    buyukResim.src = yeniResimYolu;

    // *** BURAYA YENİ KOD GELECEK ***
    // Lütfen buraya eklenmesini istediğiniz kodu yapıştırın.
    // Örnek:
    // console.log("Görsel yolu başarıyla değiştirildi: " + yeniResimYolu);
    // Veya:
    // buyukResim.setAttribute('data-last-changed', new Date().toISOString());
}
