import streamlit as st
import pandas as pd
from groq import Groq
import psycopg2

# Configuración básica
st.set_page_config(page_title="Vanguardia IA News", layout="wide")

# Estilo Premium
st.markdown("""
    <style>
    .main { background: linear-gradient(135deg, #1e3a8a, #000000); color: white; }
    .stButton>button { background-color: #10b981; color: white; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# Sidebar con tu nombre
with st.sidebar:
    st.title("🚀 Panel Control")
    st.success("👤 Blanca Yesenia Hernández")
    menu = st.radio("Ir a:", ["🤖 Chatbot IA", "📊 Dashboard Real"])

# Conexión Segura a la Base de Datos
def get_data():
    try:
        conn = psycopg2.connect(st.secrets["DB_URL"])
        query = "SELECT * FROM noticias LIMIT 10" # Asegúrate que tu tabla se llame 'noticias'
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        return str(e)

# Lógica del Chat
if menu == "🤖 Chatbot IA":
    st.header("👩‍💻 Chat de Noticias IA")
    
    # Tarjetas de estado
    c1, c2 = st.columns(2)
    with c1: st.metric("Estado DB", "Conectado ✅")
    with c2: st.metric("Motor IA", "Groq Llama-3 🔥")

    prompt = st.chat_input("Escribe tu consulta aquí...")
    if prompt:
        with st.chat_message("user"): st.write(prompt)
        with st.chat_message("assistant"):
            try:
                client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                response = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama3-8b-8192",
                )
                st.write(f"🤖 {response.choices[0].message.content}")
            except:
                st.error("Error en la llave de Groq")

else:
    st.header("📊 Dashboard de Datos")
    datos = get_data()
    if isinstance(datos, str):
        st.error(f"Error de conexión: {datos}")
    else:
        st.dataframe(datos)
