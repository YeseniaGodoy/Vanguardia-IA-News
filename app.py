import streamlit as st
from groq import Groq
import pandas as pd
import psycopg2

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Vanguardia-IA News Pro", page_icon="☀️", layout="wide")

# 2. ESTILO CORREGIDO (PARA QUE SE VEA EL TEXTO)
st.markdown("""
<style>
    /* Fondo general */
    .stApp { background-color: #ffffff; }
    
    /* FORZAR TEXTO NEGRO EN TODO EL CHAT */
    .stMarkdown, p, li, span, h1, h2, h3, h4 {
        color: #000000 !important;
    }

    /* Burbujas de chat con colores que contrasten */
    [data-testid="stChatMessageAssistant"] {
        background-color: #f0f2f6 !important;
        border: 1px solid #d1d5db;
    }
    [data-testid="stChatMessageUser"] {
        background-color: #e5e7eb !important;
        border: 1px solid #d1d5db;
    }

    /* Sidebar con texto legible */
    section[data-testid="stSidebar"] .stMarkdown p {
        color: #1f2937 !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. FUNCIONES DE BASE DE DATOS
def conectar_db():
    try: return psycopg2.connect(st.secrets["DB_URL"])
    except: return None

# 4. SIDEBAR
with st.sidebar:
    st.title("☀️ Vanguardia-IA 🌳")
    st.markdown("---")
    opcion = st.radio("Menú Principal:", ["🤖 Chat Inteligente", "📊 Dashboard Real"])
    st.markdown("---")
    st.success("👩‍💻 Blanca Yesenia Hernández")
    if st.button("🎉 Celebrar"): st.balloons()

# 5. LÓGICA DE NAVEGACIÓN
if opcion == "📊 Dashboard Real":
    st.title("📊 Análisis de Datos Neon")
    conn = conectar_db()
    if conn:
        df = pd.read_sql("SELECT title FROM noticias_tecnologia;", conn)
        conn.close()
        st.metric("Total de Noticias en Base de Datos", len(df))
        if not df.empty:
            df['Letras'] = df['title'].apply(len)
            st.bar_chart(df.set_index('title')['Letras'])
    else: st.error("Error de conexión.")

else:
    st.title("☀️ Vanguardia-IA News 📰")
    st.markdown("#### Analista Experta en Noticias | Arquitectura RAG")

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "☀️ ¡Hola Blanca! Lista para analizar tus datos. El texto ahora se ve perfecto. 🌳"}]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Consulta tu base de datos aquí..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                conn = conectar_db()
                df_ctx = pd.read_sql("SELECT title, description FROM noticias_tecnologia LIMIT 5;", conn)
                conn.close()
                contexto = df_ctx.to_string()

                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": f"Eres analista de Blanca Yesenia. Usa este contexto: {contexto}. Si no está ahí, di que no lo sabes."},
                        {"role": "user", "content": prompt}
                    ]
                )
                res = response.choices[0].message.content
                st.markdown(res)
                st.session_state.messages.append({"role": "assistant", "content": res})
            except Exception as e:
                st.error(f"Error: {e}")
