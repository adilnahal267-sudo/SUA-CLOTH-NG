import re
from app.models import ClothingItem

def smart_search(query):
    """
    Hibrit arama motoru.
    - Tek kelime: OR mantığı (geniş arama)
    - Çok kelime: AND mantığı (zorunlu kesişim)
    Returns: (results_list, search_message)
    """
    # Virgül ve noktalama işaretlerini temizle, sadece kelimeleri al
    query_cleaned = re.sub(r'[,;.!?]', ' ', query)
    tokens = [t.strip().lower() for t in query_cleaned.split() if t.strip() and len(t.strip()) > 0]
    
    if not tokens:
        return [], ""
    
    # Tüm ürünleri al
    all_items = ClothingItem.query.all()
    results = []
    
    # Tek kelime mi, çok kelime mi?
    is_single_word = len(tokens) == 1
    
    for item in all_items:
        # Ürünün tüm metin verilerini topla
        searchable_text = []
        
        # İsim ve açıklama
        if item.name:
            searchable_text.append(item.name.lower())
        if item.description:
            searchable_text.append(item.description.lower())
        
        # Özellikler (key ve value)
        for feature in item.features:
            searchable_text.append(feature.key.lower())
            searchable_text.append(feature.value.lower())
        
        # Tüm metni birleştir
        full_text = ' '.join(searchable_text)
        
        if is_single_word:
            # TEK KELİME: OR mantığı - kelime geçiyorsa ekle
            if tokens[0] in full_text:
                results.append(item)
        else:
            # ÇOK KELİME: AND mantığı - TÜM kelimeler geçmeli
            all_tokens_match = all(token in full_text for token in tokens)
            if all_tokens_match:
                results.append(item)
    
    # Bilgi mesajı oluştur
    total_tokens = len(tokens)
    result_count = len(results)
    
    if result_count == 0:
        if is_single_word:
            message = f"'{query}' için sonuç bulunamadı."
        else:
            message = f"'{query}' araması için tüm kelimeleri içeren sonuç bulunamadı. Lütfen farklı kelimeler deneyin."
    else:
        if is_single_word:
            message = f"'{query}' için {result_count} sonuç bulundu."
        else:
            message = f"{total_tokens} kelimenin tümünü içeren {result_count} sonuç bulundu."
    
    return results, message
