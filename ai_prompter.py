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
    SENİN TEK VE EN ÖNEMLİ GÖREVİN: Sana vereceğim 'YASAKLI LİSTE' içinde OLMAYAN 3 film önermek. Bu kuralı ihlal etmen, görevin tamamen başarısız olması demektir.

    ANALİZ VERİLERİ:
    - İki kullanıcının da 4+ puan vererek çok sevdiği filmler (Yüksek Öncelikli İlham Kaynağı):
      {', '.join(highly_rated_films) if highly_rated_films else 'Yok'}
    - İki kullanıcının da izleme listesindeki ortak filmler (İkincil İlham Kaynağı):
      {', '.join(common_watchlist) if common_watchlist else 'Yok'}

    YASAKLI LİSTE (Bu listedeki filmler KESİNLİKLE önerilemez):
    {', '.join(sorted(list(all_watched_films)))}

    GÖREVİN:
    Yukarıdaki analiz verilerinden ilham alarak, 'YASAKLI LİSTE'de olmayan 3 film öner. Her öneri için filmin tam adını kalın harflerle yaz. Bir alt satırda, bu filmi neden seçtiğini, analiz verilerindeki filmlerle bağlantı kurarak detaylı ve ikna edici bir şekilde açıkla. Önerilerinin içeriği kaliteli ve bilgilendirici olsun.

    SON KONTROL: Cevabını vermeden önce, önerdiğin 3 filmin de 'YASAKLI LİSTE' içinde olmadığından tekrar emin ol. Bu son ve en önemli kontroldür.
    Giriş cümlesi falan hiçbir şey yazma. Sadece film önerilerini yap. Listeden çıkardığın bir film olursa bunun için bir bilgi verme. Saf çıktın 3 adet film, neden seçtiğin ve film içeriği olsun. Ne olursa olsun önereceğin 3 adet film iki kullanıcının da izleme listesinde OLAMYAN bir film olsun
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"HATA: Yapay zeka ile iletişim kurulurken bir sorun oluştu: {e}"


