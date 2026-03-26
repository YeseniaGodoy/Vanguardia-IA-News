import streamlit as st
from groq import Groq
import pandas as pd

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Vanguardia-IA News", page_icon="☀️", layout="wide")

# 2. ESTILO OSCURO PERSONALIZADO
st.markdown("""
<style>
    .stApp { background: #020617; color: white; }
    section[data-testid="stSidebar"] { background: #020617; border-right: 1px solid #1e293b; }
    .stChatMessage { background: rgba(255,255,255,0.05); border-radius: 10px; margin-bottom: 10px; }
    .stButton>button { border-radius: 20px; width: 100%; }
</style>
""", unsafe_allow_html=True)

# 3. BARRA LATERAL (SIDEBAR) CON TUS ÍCONOS
with st.sidebar:
    st.title("☀️ Vanguardia-IA 🌳")
    st.markdown("---")
    menu = st.radio("Menú de Navegación:", ["🤖 Chatbot", "📊 Dashboard"])
    st.markdown("---")
    st.success("👩‍💻 Blanca Yesenia Hernández")
    if st.button("🎉 Lanzar Celebración"):
        st.balloons()

# 4. LÓGICA DEL CHATBOT
if menu == "🤖 Chatbot":
    st.markdown("# ☀️ Vanguardia-IA News 📰")
    st.info("Analista Experta en Noticias de El Salvador y el Mundo.")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "☀️ ¡Hola Blanca Yesenia! Soy tu analista de IA. Estoy lista para analizar noticias contigo. 🌳 ¿Qué tema te interesa hoy?"}
        ]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("Escribe tu consulta aquí...")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                # LLAVE DIRECTA PARA EVITAR ERRORES DE SECRETS
                key = "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"
                client = Groq(api_key=key)
                
                # MODELO ACTUALIZADO (PARA EVITAR ERROR 400)
                response = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama-3.3-70b-versatile",
                )
                res_text = response.choices[0].message.content
                st.markdown(res_text)
                st.session_state.messages.append({"role": "assistant", "content": res_text})
            except Exception as e:
                st.error(f"⚠️ Error: {e}")

# 5. DASHBOARD
else:
    st.title("📊 Dashboard de Noticias")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Tendencia Semanal")
        st.line_chart({"Noticias IA": [10, 50, 80, 150]})
    with col2:
        st.subheader("Temas por Categoría")
        st.bar_chart({"Tecnología": 100, "Economía": 60, "Salud": 40})
