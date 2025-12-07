import google.generativeai as genai
import os
import json
from flask import current_app

def analyze_image_with_gemini(image_path):
    """
    Analyzes an image using Google Gemini 1.5 Flash model.
    Returns a JSON object with category, color, details, and accessories.
    """
    api_key = current_app.config.get('GEMINI_API_KEY')
    if not api_key:
        return {"error": "API Key not configured"}

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')

        # Read image data
        with open(image_path, 'rb') as f:
            image_data = f.read()

        prompt = """
        Bu moda görselini analiz et ve aşağıdaki alanları içeren bir JSON çıktısı ver:
        - category: Ürünün ana kategorisi (örn: Gömlek, Elbise, Pantolon).
        - color: Baskın renk (Türkçe).
        - details: 3-5 adet tasarım detayı içeren liste (örn: V yaka, çizgili, uzun kollu) (Türkçe).
        - accessories: Varsa görünen aksesuarların listesi (Türkçe).
        
        SADECE geçerli JSON çıktısı ver.
        """

        response = model.generate_content([
            {'mime_type': 'image/jpeg', 'data': image_data},
            prompt
        ])
        
        # Clean up response text to ensure it's valid JSON
        text = response.text.strip()
        if text.startswith('```json'):
            text = text[7:-3]
        
        return json.loads(text)

    except Exception as e:
        print(f"Gemini Error: {e}")
        return {"error": str(e)}
