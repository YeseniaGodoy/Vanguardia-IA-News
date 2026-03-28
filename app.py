
import streamlit as st
import pandas as pd
import psycopg2
from groq import Groq

# 1. Configuración de la página
st.set_page_config(page_title="Vanguardia-IA", page_icon="☀️", layout="wide")

# 2. Estilo CSS para Contraste de Letras y Botones
st.markdown("""
    <style>
    /* Fondo gris claro */
    .stApp { background-color: #f0f2f6; }

    /* FORZAR COLOR DE LETRAS EN TODA LA PAGINA */
    html, body, [class*="st-"] {
        color: #1a1a1a !important; /* Negro fuerte para que se lea bien */
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Estilo de los mensajes del chat */
    [data-testid="stChatMessage"] {
        background-color: white !important;
        border-radius: 15px !important;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.1) !important;
        border: 1px solid #d1d5db !important;
        color: #1a1a1a !important;
    }

    /* Botón Limpiar Historial (Gris) */
    div.stButton > button:contains("Limpiar Historial") {
        background-color: #e2e8f0 !important;
        color: #1a202c !important;
        border: 1px solid #cbd5e1 !important;
    }

    /* Botón Blanca (Verde Fuerte para lectura) */
    div.stButton > button:contains("Blanca Yesenia Hernández") {
        background-color: #c3e6cb !important;
        color: #155724 !important;
        border: 1px solid #b1dfbb !important;
        font-weight: bold !important;
    }
    
    /* Botón Celebración (Amarillo Fuerte) */
    div.stButton > button:contains("¡Lanzar Celebración!") {
        background-color: #ffe082 !important;
        color: #856404 !important;
        border: 1px solid #ffd54f !important;
        font-weight: bold !important;
    }

    /* Títulos de la barra lateral */
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] p {
        color: #1a1a1a !important;
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Conexión a Neon
def conectar_db():
    try:
        conn = psycopg2.connect("postgresql://neondb_owner:npg_W9Yof7aAnGgF@ep-round-sun-a5v5pbe9-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require")
        return conn
    except Exception as e:
        return None

def obtener_datos():
    conn = conectar_db()
    if conn:
        df = pd.read_sql_query("SELECT * FROM noticias_tecnologia", conn)
        conn.close()
        return df
    return pd.DataFrame()

# --- BARRA LATERAL (SIDEBAR) ---
with st.sidebar:
    st.title("☀️ Vanguardia-IA")
    st.write("### Panel de Control")
    menu = st.radio("Menú", ["🤖 Chat Inteligente", "📊 Dashboard Real"], label_visibility="collapsed")
    
    st.markdown("<br>" * 10, unsafe_allow_html=True)
    
    if st.button("🗑️ Limpiar Historial"):
        st.session_state.messages = []
        st.rerun()
    
    st.button("✨ Blanca Yesenia Hernández")
    
    if st.button("🥳 ¡Lanzar Celebración!"):
        st.balloons()
        st.snow()

# --- LÓGICA DEL CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "🤖 ☀️ 🤖 ¡Lista Blanca! Conectada a Neon y lista para el éxito. ¿Qué noticia analizamos?"}
    ]

if menu == "🤖 Chat Inteligente":
    # Mostrar mensajes con mejor contraste
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(f'<p style="color: black; font-size: 16px;">{message["content"]}</p>', unsafe_allow_html=True)

    # El buscador (Input del chat)
    if prompt := st.chat_input("🔍 Buscar noticia o hacer una pregunta..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Lógica RAG
        df = obtener_datos()
        contexto = df.to_string()
        
        # --- PEGA TU CLAVE DE GROQ AQUÍ ---
        client = Groq(api_key="TU_CLAVE_GSK_AQUI") 

        if "ULTIMA NOTICIA" in prompt.upper() or "ÚLTIMA NOTICIA" in prompt.upper():
            with st.chat_message("assistant"):
                st.write("🤖 **Última Noticia Encontrada:**")
                st.table(df.tail(1))
            st.session_state.messages.append({"role": "assistant", "content": "Mostré la tabla de la última noticia."})
        else:
            try:
                response = client.chat.completions.create(
                    messages=[{"role": "user", "content": f"Contexto: {contexto}. Pregunta: {prompt}. Si no sabes, di que no hay registros en Neon."}],
                    model="llama3-8b-8192",
                )
                answer = response.choices[0].message.content
                with st.chat_message("assistant"):
                    st.markdown(f"☀️ {answer}")
                st.session_state.messages.append({"role": "assistant", "content": f"☀️ {answer}"})
            except:
                st.error("Error de conexión con Groq.")

# --- DASHBOARD ---
elif menu == "📊 Dashboard Real":
    st.title("📊 Análisis de Datos Real")
    df = obtener_datos()
    if not df.empty:
        st.write("### Registros en Neon")
        st.dataframe(df)
        st.bar_chart(df['title'].value_counts())
