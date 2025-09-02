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
1. Önerilecek filmler, iki kullanıcının da izlediği listesinde **olmamalı**. Eğer bir film tek bir kullanıcı tarafından izlendiyse veya yasaklı listedeyse, onu atla.
2. Sadece **3 film** önereceksin. Başka açıklama, giriş cümlesi veya ek bilgi ekleme.
3. Her film için:
   - Film adı **kalın** yazılacak.
   - Bir alt satırda, bu filmi neden seçtiğini, iki kullanıcının yüksek puan verdiği filmler ve ortak izleme listesi ile bağlantı kurarak açıklayacaksın. Açıklama ikna edici ve detaylı olacak.
4. Cevabını verdikten sonra tekrar kontrol et: Önerdiğin tüm filmler yasaklı listede olmamalı ve iki kullanıcının da izlemediği filmler olmalı.
5. Watchlist listesinde varsa önerebilirsin. Ama izlenen listedeyse asla önerme. İzlenen liste = all_watched_films, watchlist = common_watchlist
6. Film öneri metinlerini yazarken bu listeler hakkında bir şey söyleme. Sadece filmler hakkında bilgi ver ve o filmi neden seçtiğini söyle. Mesela iki kullanıcı da x filmini izlemiş, o yüzden bunu sevebilirler çünkü... gibi
7. Vereceğin çıktı yazısında asla yasaklı liste gibi şeyler kullanma. Bunlar arkaplan işleri. Sadece film ve kullanıcı bazında konuşmalar yap. Giriş cümlesi falan kullanma. 

VERİLER:
- İki kullanıcının da 4+ puan vererek çok sevdiği filmler (Yüksek Öncelikli İlham Kaynağı):
  {', '.join(highly_rated_films) if highly_rated_films else 'Yok'}
- İki kullanıcının ortak izleme listesi (İkincil İlham Kaynağı):
  {', '.join(common_watchlist) if common_watchlist else 'Yok'}
Bu filmlerin hepsini dikkatlice hafızana al.
iki kullanıcının da izlediği YASAKLI LİSTE: (Bu listedeki filmleri KESİNLİKLE önerme): {', '.join(sorted(list(all_watched_films)))}
"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"HATA: Yapay zeka ile iletişim kurulurken bir sorun oluştu: {e}"

