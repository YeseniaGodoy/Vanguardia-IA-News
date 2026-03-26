import streamlit as st
from groq import Groq
import pandas as pd
import psycopg2

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Vanguardia-IA News", page_icon="☀️", layout="wide")

# 2. ESTILO
st.markdown("""<style>.stApp { background: #020617; color: white; }</style>""", unsafe_allow_html=True)

# 3. FUNCIÓN PARA LEER TU BASE DE DATOS NEON
def consultar_base_datos():
    try:
        # Usa la URL de tus Secrets
        conn = psycopg2.connect(st.secrets["DB_URL"])
        query = "SELECT * FROM noticias LIMIT 10;" # O el nombre de tu tabla
        df = pd.read_sql(query, conn)
        conn.close()
        return df.to_string() # Convierte los datos en texto para la IA
    except:
        return "No hay datos disponibles en la base de datos actualmente."

# 4. SIDEBAR
with st.sidebar:
    st.title("☀️ Vanguardia-IA 🌳")
    st.success("👩‍💻 Blanca Yesenia Hernández")
    if st.button("🎉 Celebrar"): st.balloons()

# 5. LÓGICA DEL CHATBOT "HONESTO"
st.markdown("# 🤖 Analista de Base de Datos")
st.info("Solo respondo basado en lo que Blanca Yesenia ha guardado en la base de datos.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

prompt = st.chat_input("¿Qué noticia buscas en mi base de datos?")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        # PASO CLAVE: Traemos tus datos de Neon
        datos_reales = consultar_base_datos()
        
        try:
            key = "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"
            client = Groq(api_key=key)
            
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": f"Eres un analista. AQUÍ ESTÁ LA BASE DE DATOS DE BLANCA: {datos_reales}. Si el usuario pregunta algo que NO esté en ese texto, responde: 'Lo siento, esa noticia no está registrada en mi base de datos de Neon'."},
                    {"role": "user", "content": prompt}
                ],
                model="llama-3.3-70b-versatile",
            )
            res = response.choices[0].message.content
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
        except Exception as e:
            st.error(f"Error: {e}")
