import streamlit as st
from groq import Groq
import pandas as pd
import psycopg2

# ==========================================
# 💎 CONFIGURACIÓN PREMIUM
# ==========================================
st.set_page_config(page_title="Vanguardia-IA News Pro ✨", page_icon="☀️", layout="wide")

# --- CSS PARA EL PRIMER LUGAR ---
st.markdown("""
<style>
    .stApp { background: linear-gradient(-45deg, #ffffff, #f0f9ff, #f0fff4); }
    .stMarkdown, p, li, span, h1, h2, h3, h4 { color: #000000 !important; font-family: 'Inter', sans-serif; }
    .stChatMessage {
        border-radius: 20px;
        padding: 15px;
        margin-bottom: 15px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    section[data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #e2e8f0; }
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
    try:
        return psycopg2.connect(st.secrets["DB_URL"])
    except:
        return None

# 🌳 SIDEBAR
with st.sidebar:
    st.markdown("## ☀️ Vanguardia-IA")
    st.markdown("---")
    opcion = st.radio("Ir a:", ["🤖 Chat Inteligente", "📊 Dashboard Real"])
    st.markdown("---")
    st.success("✨ Blanca Yesenia Hernández")
    if st.button("🎉 ¡Lanzar Celebración!"): 
        st.balloons()

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
    else: 
        st.error("Error de conexión a la base de datos.")

# 🤖 SECCIÓN 2: CHATBOT (LÓGICA SUPERIOR)
else:
    st.markdown("# ☀️ Vanguardia-IA News 📰")
    st.markdown("### *Analista Experta en Noticias Reales*")
    st.write("---")

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "☀️🤖 ¡Bienvenida Blanca Yesenia! Estoy conectada a tu base de datos Neon. ¿Qué noticia quieres que analice hoy? 🌳"}]

    # Mostrar historial
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Escribe tu consulta aquí..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): 
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("☀️ Consultando base de datos Neon..."):
                try:
                    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                    
                    # PASO 1: Generar el SQL (Igual que el otro grupo, pero más rápido)
                    prompt_sql = f"Escribe SOLAMENTE una consulta SQL de PostgreSQL para responder: '{prompt}'. La tabla se llama 'noticias_tecnologia' y tiene las columnas 'title' y 'description'."
                    
                    res_sql = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[
                            {"role": "system", "content": "Eres un experto en SQL. Solo devuelve el código SQL puro, sin explicaciones ni comillas."},
                            {"role": "user", "content": prompt_sql}
                        ]
                    )
                    query = res_sql.choices[0].message.content.strip().replace("```sql", "").replace("```", "")

                    # PASO 2: Ejecutar en Neon
                    conn = conectar_db()
                    df_resultado = pd.read_sql(query, conn)
                    conn.close()
                    
                    # PASO 3: Interpretación humana de los datos encontrados
                    contexto_datos = df_resultado.to_string()
                    
                    res_final = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[
                            {"role": "system", "content": f"Eres analista de Blanca Yesenia. Basado en estos datos de Neon: {contexto_datos}. Responde de forma profesional. Si no hay datos, di que no se encuentra en la base."},
                            {"role": "user", "content": prompt}
                        ]
                    )
                    
                    respuesta = res_final.choices[0].message.content
                    st.markdown(respuesta)
                    
                    # MOSTRAR EL SQL (Para demostrar que tu proyecto es técnico)
                    with st.expander("🔍 Ver proceso de análisis"):
                        st.code(query, language="sql")
                        st.dataframe(df_resultado)
                        
                    st.session_state.messages.append({"role": "assistant", "content": respuesta})

                except Exception as e:
                    st.error(f"Lo siento Blanca, hubo un detalle técnico: {e}")

st.caption("🏆 Proyecto Vanguardia-IA News | Blanca Yesenia Hernández")
