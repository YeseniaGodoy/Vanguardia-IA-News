import streamlit as st
from groq import Groq
import pandas as pd
import psycopg2
import os

# ==========================================
# 🏆 CONFIGURACIÓN DE ALTO NIVEL (UI/UX)
# ==========================================
st.set_page_config(
    page_title="Vanguardia-IA News | Analista Pro",
    page_icon="☀️",
    layout="wide"
)

# Estilo visual profesional
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stChatMessage { border-radius: 15px; padding: 10px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 🌳 PANEL LATERAL PROFESIONAL (SIDEBAR)
# ==========================================
with st.sidebar:
    st.title("🌳 Panel de Control")
    st.markdown("---")
    st.subheader("☀️ Vanguardia-IA News")
    st.info("Arquitectura **RAG** (Generación Aumentada por Recuperación) conectada a Neon.")
    
    st.markdown("---")
    st.write("**Desarrollado por:**")
    st.success("✨ Blanca Yesenia Hernández")
    st.write("---")
    st.caption("☀️ *'Datos reales, respuestas verdaderas.'* 🌳")
    
    if st.button("🎈 ¡Celebrar Victoria!"):
        st.balloons()

# ==========================================
# 📰 ENCABEZADO PRINCIPAL
# ==========================================
st.title("☀️ Vanguardia-IA News 📰")
st.markdown("#### *Analista Experta en Noticias Basada en Datos Reales*")
st.write("---")

# ==========================================
# 🔑 SEGURIDAD Y CONEXIÓN
# ==========================================
try:
    # Usamos la librería oficial de Groq (más profesional)
    groq_api_key = st.secrets["GROQ_API_KEY"]
    db_url = st.secrets["DB_URL"]
    client = Groq(api_key=groq_api_key)
except Exception:
    st.error("⚠️ Error: Configura GROQ_API_KEY y DB_URL en los Secrets de Streamlit.")
    st.stop()

# ==========================================
# 💾 EXTRACCIÓN DE DATOS (ANTIALUCINACIÓN)
# ==========================================
@st.cache_data(ttl=600)
def cargar_datos_reales():
    try:
        conn = psycopg2.connect(db_url)
        # AJUSTADO: Usamos exactamente tus nombres de tabla y columnas
        query = "SELECT title, description FROM noticias_tecnologia LIMIT 15;"
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        texto_contexto = ""
        for _, row in df.iterrows():
            texto_contexto += f"NOTICIA: {row['title']}\nDESCRIPCIÓN: {row['description']}\n---\n"
        return texto_contexto
    except Exception as e:
        return f"Error de conexión con la base de datos: {e}"

# Cargamos las noticias reales de tu base Neon
contexto_db = cargar_datos_reales()

# ==========================================
# 💬 CHAT INTELIGENTE (MODO GANADOR)
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "☀️ **¡Bienvenida!** Soy tu analista de IA. He leído tu base de datos y estoy lista para darte respuestas **reales y verificadas**. 🌳 ¿Qué noticias deseas analizar hoy?"}
    ]

# Mostrar historial con avatares
for message in st.session_state.messages:
    avatar = "🤖" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Captura de pregunta del usuario
if prompt := st.chat_input("Escribe tu consulta aquí..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("🧠 Consultando base de datos Neon..."):
            # INSTRUCCIONES ESTRICTAS (Grounding)
            system_instruction = f"""
            Eres una IA analista profesional de alto nivel. 
            REGLA DE ORO: Responde ÚNICAMENTE basándote en el CONTEXTO DE NOTICIAS que te doy. 
            Si la respuesta no está ahí, di: 'Lo siento, esa información no está en mi base de datos de noticias actual.'
            No inventes nada (Prohibido alucinar). Usa negritas, emojis y listas.
            
            CONTEXTO DE NOTICIAS:
            {contexto_db}
            """
            
            try:
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": system_instruction},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.1 # Precisión máxima
                )
                full_response = response.choices[0].message.content
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"Error al procesar con la IA: {e}")

st.write("---")
st.caption("🏆 Proyecto Vanguardia-IA News | Blanca Yesenia Hernández")
