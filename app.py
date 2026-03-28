import streamlit as st
from groq import Groq
import pandas as pd
import psycopg2

# ==========================================
# 💎 CONFIGURACIÓN PREMIUM
# ==========================================
st.set_page_config(page_title="Vanguardia-IA News Pro ✨", page_icon="☀️", layout="wide")

# --- CSS PARA EL PRIMER LUGAR (TEXTO NEGRO Y DISEÑO LIMPIO) ---
st.markdown("""
<style>
    .stApp { background: linear-gradient(-45deg, #ffffff, #f0f9ff, #f0fff4); }
    
    /* FORZAR TEXTO NEGRO */
    .stMarkdown, p, li, span, h1, h2, h3, h4 { color: #000000 !important; font-family: 'Inter', sans-serif; }

    /* Burbujas de Chat elegantes */
    .stChatMessage {
        border-radius: 20px;
        padding: 15px;
        margin-bottom: 15px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }

    /* Sidebar */
    section[data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #e2e8f0; }
    
    /* Botón Celebrar */
    .stButton>button {
        border-radius: 25px;
        width: 100%;
        background-color: #fcd34d;
        color: #000 !important;
        font-weight: bold;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

# 🔌 FUNCIONES DB
def conectar_db():
    try: return psycopg2.connect(st.secrets["DB_URL"])
    except: return None

# 🌳 SIDEBAR
with st.sidebar:
    st.markdown("## ☀️ Vanguardia-IA")
    st.markdown("---")
    opcion = st.radio("Ir a:", ["🤖 Chat Inteligente", "📊 Dashboard Real"])
    st.markdown("---")
    st.success("✨ Blanca Yesenia Hernández")
    if st.button("🎉 ¡Lanzar Celebración!"): st.balloons()

# 📈 SECCIÓN 1: DASHBOARD
if opcion == "📊 Dashboard Real":
    st.title("📊 Dashboard de Noticias")
    conn = conectar_db()
    if conn:
        df = pd.read_sql("SELECT title FROM noticias_tecnologia;", conn)
        conn.close()
        st.metric("Total Noticias en Neon", len(df))
        if not df.empty:
            df['Largo'] = df['title'].apply(len)
            st.bar_chart(df.set_index('title')['Largo'])
    else: st.error("Error de conexión a la base de datos.")

# 🤖 SECCIÓN 2: CHATBOT (CORREGIDO)
else:
    st.markdown("# ☀️ Vanguardia-IA News 📰")
    st.markdown("### *Analista Experta en Noticias Reales*")
    st.write("---")

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "☀️🤖 ¡Bienvenida Blanca Yesenia! Soy tu analista de IA. He leído tu base de datos de Neon y estoy lista para responder con la verdad. 🌳"}]

    # Mostrar mensajes SIN avatares complejos para evitar el error rojo
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Escribe tu consulta aquí..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("☀️ Consultando Neon..."):
                try:
                    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                    conn = conectar_db()
                    df_ctx = pd.read_sql("SELECT title, description FROM noticias_tecnologia LIMIT 5;", conn)
                    conn.close()
                    contexto = df_ctx.to_string()

                    response = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[
                            {"role": "system", "content": f"Eres analista de Blanca Yesenia. Contexto: {contexto}. Si no está ahí, di que no lo sabes."},
                            {"role": "user", "content": prompt}
                        ]
                    )
                    res = response.choices[0].message.content
                    st.markdown(res)
                    st.session_state.messages.append({"role": "assistant", "content": res})
                except Exception as e:
                    st.error(f"Error de IA: {e}")

st.caption("🏆 Proyecto Vanguardia-IA News | Blanca Yesenia Hernández")
