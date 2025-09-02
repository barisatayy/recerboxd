import streamlit as st
import google.generativeai as genai


def get_ai_recommendations(highly_rated_films, common_watchlist, all_watched_films):
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
    except Exception as e:
        return "HATA: Gemini API anahtarı bulunamadı veya yanlış. Lütfen .streamlit/secrets.toml dosyasını kontrol edin."

    model = genai.GenerativeModel('gemini-2.0-flash')

   prompt = f"""
GÖREVİN: Sana vereceğim verilerden ilham alarak, 'YASAKLI LİSTE'de **olmayan** 3 film önermek. 
Kesinlikle ve hiçbir koşulda yasaklı listedeki filmleri önerme. Eğer yanlışlıkla önerirsen, onu tamamen atla ve başka bir film öner.

KURALLAR:
1. Önerilecek filmler, iki kullanıcının da izleme listesinde **olmamalı**. Eğer bir film tek bir kullanıcı tarafından izlendiyse veya yasaklı listedeyse, onu atla.
2. Sadece **3 film** önereceksin. Başka açıklama, giriş cümlesi veya ek bilgi ekleme.
3. Her film için:
   - Film adı **kalın** yazılacak.
   - Bir alt satırda, bu filmi neden seçtiğini, iki kullanıcının yüksek puan verdiği filmler ve ortak izleme listesi ile bağlantı kurarak açıklayacaksın. Açıklama ikna edici ve detaylı olacak.
4. Cevabını verdikten sonra tekrar kontrol et: Önerdiğin tüm filmler yasaklı listede olmamalı ve iki kullanıcının da izlemediği filmler olmalı.

VERİLER:
- İki kullanıcının da 4+ puan vererek çok sevdiği filmler (Yüksek Öncelikli İlham Kaynağı):
  {', '.join(highly_rated_films) if highly_rated_films else 'Yok'}
- İki kullanıcının ortak izleme listesi (İkincil İlham Kaynağı):
  {', '.join(common_watchlist) if common_watchlist else 'Yok'}
- YASAKLI LİSTE (Bu listedeki filmleri KESİNLİKLE önerme):
  {', '.join(sorted(list(all_watched_films)))}

SADECE yukarıdaki kurallara uygun üç film öner ve her biri için neden seçtiğini açıkla. Başka hiçbir şey ekleme.
"""


    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"HATA: Yapay zeka ile iletişim kurulurken bir sorun oluştu: {e}"



