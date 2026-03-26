import streamlit as st
from groq import Groq
import pandas as pd

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Vanguardia-IA News", page_icon="☀️", layout="wide")

# 2. ESTILO OSCURO
st.markdown("""
<style>
    .stApp { background: #020617; color: white; }
    section[data-testid="stSidebar"] { background: #020617; border-right: 1px solid #1e293b; }
    .stChatMessage { background: rgba(255,255,255,0.05); border-radius: 10px; margin-bottom: 10px; }
    .stButton>button { border-radius: 20px; width: 100%; background-color: #1e293b; color: white; }
</style>
""", unsafe_allow_html=True)

# 3. SIDEBAR (SOL Y ÁRBOL)
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
    st.info("Analista Experta: Si no tengo la información en mi base de datos, te diré que no la conozco.")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "☀️ ¡Hola Blanca Yesenia! Soy tu analista. Estoy configurada para ser honesta: si me preguntas algo que no está en mis registros, te diré que no lo sé. 🌳"}
        ]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("Hazme una pregunta difícil...")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                # LLAVE DIRECTA
                key = "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"
                client = Groq(api_key=key)
                
                # MODELO NUEVO CON INSTRUCCIÓN DE HONESTIDAD
                response = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "Eres el asistente de Blanca Yesenia. Debes ser honesto. Si el usuario te pregunta por algo inventado o que no existe en las noticias reales, responde: 'Lo siento, no tengo esa información en mi base de datos actual'."},
                        {"role": "user", "content": prompt}
                    ],
                    model="llama-3.3-70b-versatile",
                )
                res_text = response.choices[0].message.content
                st.markdown(res_text)
                st.session_state.messages.append({"role": "assistant", "content": res_text})
            except Exception as e:
                st.error(f"⚠️ Error: {e}")

else:
    st.title("📊 Dashboard")
    st.line_chart({"Noticias": [10, 50, 150]})
