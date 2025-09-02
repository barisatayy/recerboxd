import streamlit as st
from streamlit_option_menu import option_menu
import webscraping
from time import sleep
import ai_prompter

st.set_page_config(layout="wide")

if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False
    st.session_state.results = {}

col11, col22, col33 = st.columns([0.1, 1, 0.1])
with col22:
    st.markdown(
        "<h1 style='text-align:center;"
        "font-size:70px;"
        "color:orange'"">"
        "Recerboxd"
        "</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<h3 style='text-align:center;"
        "color:white'>"
        "Letterboxd kullanıcı film öneri ve analiz sistemi"
        "</h3>",
        unsafe_allow_html=True
    )

st.write("---")
menu1 = option_menu("", ("Film Öneri Sistemi", "Profil Analizi"),
                    icons=["film", "bar-chart-fill"],
                    menu_icon="cast",
                    orientation="horizontal"
                    )

st.write("")
st.write("")
st.write("")

if menu1 == "Film Öneri Sistemi":
    col1, col2, col3 = st.columns([1, 0.5, 1])
    with col2:
        with st.form("kform"):
            k1 = st.text_input("Kullanıcı Adı 1", max_chars=15, key="k1")
            k2 = st.text_input("Kullanıcı Adı 2", max_chars=15, key="k2")
            submitted = st.form_submit_button("Analiz Et", use_container_width=True)

    if submitted:
        if k1 and k2:
            col1, col2, col3 = st.columns([1, 0.5, 1])
            with col2:
                with st.spinner("Profiller inceleniyor ve yapay zeka analiz yapıyor... Bu işlem biraz zaman alabilir."):
                    results = webscraping.get_user_data(k1, k2)
                    st.session_state.results = results

                    highly_rated = results.get('highly_rated_common', [])
                    watchlist = results.get('ortak_watchlist', [])
                    u1_watched = results.get('user1_watched_full', set())
                    u2_watched = results.get('user2_watched_full', set())
                    all_watched = u1_watched.union(u2_watched)

                    ai_rec = ai_prompter.get_ai_recommendations(highly_rated, watchlist, all_watched)
                    st.session_state.results['ai_recommendations'] = ai_rec

                    st.session_state.analysis_complete = True
        else:
            placeholder = st.empty()
            placeholder.markdown("""
                <style>
                @keyframes fadeInOut { 0% {opacity: 0;} 10% {opacity: 1;} 90% {opacity: 1;} 100% {opacity: 0;} }
                .fade-message { text-align: center; color: #FA6548; font-size: 30px; animation: fadeInOut 4s ease-in-out forwards; }
                </style>
                <div class="fade-message">kullanıcı adını doğru girin</div>
                """, unsafe_allow_html=True)
            sleep(3)
            placeholder.empty()

    if st.session_state.analysis_complete and menu1 == "Film Öneri Sistemi":
        st.write("---")
        st.markdown("""
        <style>
        .container-frame { border: 2px solid orange; padding: 20px; border-radius: 10px; height: 450px; overflow-y: auto; }
        </style>
        """, unsafe_allow_html=True)
        results = st.session_state.results
        col111, col222, col333, col444 = st.columns([1, 1, 1, 1.3])

        with col111:
            st.markdown("<h1 style='font-size:25px;text-align:center'>Ortak İzlenen Filmler</h1>",
                        unsafe_allow_html=True)
            st.markdown(f'<div class="container-frame">{"<br>".join(results.get("ortak_filmler", []))}</div>',
                        unsafe_allow_html=True)
        with col222:
            st.markdown("<h1 style='font-size:25px;text-align:center'>Aynı Puan Verilen Filmler</h1>",
                        unsafe_allow_html=True)
            st.markdown(f'<div class="container-frame">{"<br>".join(results.get("ayni_puanli_filmler", []))}</div>',
                        unsafe_allow_html=True)
        with col333:
            st.markdown("<h1 style='font-size:25px;text-align:center'>Ortak İzleme Listesi</h1>",
                        unsafe_allow_html=True)
            st.markdown(f'<div class="container-frame">{"<br>".join(results.get("ortak_watchlist", []))}</div>',
                        unsafe_allow_html=True)
        with col444:
            st.markdown("<h1 style='font-size:25px;text-align:center;color:purple'>Yapay Zeka Önerileri 🔮</h1>",
                        unsafe_allow_html=True)
            ai_response = results.get('ai_recommendations', "Öneri bulunamadı.")
            display_text = ai_response.replace('\n', '<br>')
            st.markdown(f'<div class="container-frame" style="border-color:purple;">{display_text}</div>',
                        unsafe_allow_html=True)

if menu1 == "Profil Analizi":
    col1, col2, col3 = st.columns([1, 0.5, 1])
    with col2:
        st.markdown("<h1 style='font-size:45px;text-align:center'>Çok yakında...</h1>", unsafe_allow_html=True)

        if st.button("Balon Patlat", use_container_width=True):
            st.balloons()
        if st.button("Kar Yağdır", use_container_width=True):
            st.snow()
