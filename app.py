import streamlit as st
from groq import Groq
import pandas as pd

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Vanguardia-IA News", page_icon="☀️", layout="wide")

# 2. ESTILO OSCURO
st.markdown("""
<style>
    .stApp { background: #020617; color: white; }
    section[data-testid="stSidebar"] { background: #020617; }
    .stChatMessage { background: rgba(255,255,255,0.05); border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# 3. SIDEBAR (CON TU SOL Y ÁRBOL)
with st.sidebar:
    st.title("☀️ Vanguardia-IA 🌳")
    st.markdown("---")
    pagina = st.radio("Menú de Navegación:", ["🤖 Chatbot", "📊 Dashboard"])
    st.markdown("---")
    st.success("👩‍💻 Blanca Yesenia Hernández")
    if st.button("🎉 Celebrar"):
        st.balloons()

# 4. LÓGICA DEL CHATBOT
if pagina == "🤖 Chatbot":
    st.markdown("# ☀️ Vanguardia-IA News 📰")
    st.markdown("### Analista Experta en Noticias Basada en Datos Reales")

    if "messages" not in st.session_state:
        # Mensaje de bienvenida igual a tu foto
        st.session_state.messages = [{"role": "assistant", "content": "☀️ ¡Bienvenida! Soy tu analista de IA. He leído tu base de datos y estoy lista para darte respuestas reales y verificadas. 🌳 ¿Qué noticias deseas analizar hoy?"}]

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
                # LLAVE DIRECTA PARA EVITAR EL ERROR
                key = "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"
                client = Groq(api_key=key)
                
                response = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama3-8b-8192",
                )
                res_text = response.choices[0].message.content
                st.markdown(res_text)
                st.session_state.messages.append({"role": "assistant", "content": res_text})
            except Exception as e:
                st.error(f"Error de conexión: {e}")

# 5. DASHBOARD
else:
    st.title("📊 Dashboard de Noticias")
    st.line_chart({"IA": [10, 40, 90, 150]})
    st.bar_chart({"Enero": 30, "Febrero": 80, "Marzo": 150})
