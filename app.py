import streamlit as st
from groq import Groq
import pandas as pd
import psycopg2

# ==========================================
# 💎 CONFIGURACIÓN PREMIUM VANGUARDIA-IA
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

# 🔌 FUNCIONES DE CONEXIÓN
def conectar_db():
    try:
        return psycopg2.connect(st.secrets["DB_URL"])
    except:
        return None

# 🌳 BARRA LATERAL
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
        try:
            df = pd.read_sql("SELECT title FROM noticias_tecnologia;", conn)
            conn.close()
            st.metric("Total Noticias en Neon", len(df))
            if not df.empty:
                df['Largo'] = df['title'].apply(len)
                st.bar_chart(df.set_index('title')['Largo'])
        except:
            st.error("Error al leer las tablas.")
    else: 
        st.error("Error de conexión a la base de datos.")

# 🤖 SECCIÓN 2: CHATBOT ANALISTA
else:
    st.markdown("# ☀️ Vanguardia-IA News 📰")
    st.markdown("### *Analista Experta en Noticias Reales*")
    st.write("---")

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "☀️🤖 ¡Hola Blanca Yesenia! Estoy lista. Pregúntame sobre tus 92 noticias de Neon. 🌳"}]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Pregúntame sobre tus noticias en Neon..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): 
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("☀️ Analizando Neon..."):
                try:
                    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                    
                    # PASO 1: SQL
                    res_sql = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[
                            {"role": "system", "content": "Genera solo el código SQL puro para PostgreSQL. Tabla: noticias_tecnologia (columnas: title, description). Sin texto extra."},
                            {"role": "user", "content": prompt}
                        ]
                    )
                    query = res_sql.choices[0].message.content.strip().replace("```sql", "").replace("```", "")

                    # PASO 2: CONSULTA
                    conn = conectar_db()
                    df_res = pd.read_sql(query, conn)
                    conn.close()
                    
                    # PASO 3: RESPUESTA FINAL
                    ctx = df_res.to_string()
                    res_final = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[
                            {"role": "system", "content": f"Eres la Analista de Blanca Yesenia. SÍ tienes acceso. Datos de Neon: {ctx}. Úsalos para responder."},
                            {"role": "user", "content": prompt}
                        ]
                    )
                    
                    respuesta = res_final.choices[0].message.content
                    st.markdown(respuesta)
                    
                    with st.expander("🔍 Ver proceso técnico"):
                        st.code(query, language="sql")
                        st.dataframe(df_res)
                        
                    st.session_state.messages.append({"role": "assistant", "content": respuesta})

                except Exception as e:
                    st.error(f"Aviso: Intenta preguntar de forma más clara. Detalles: {e}")

st.caption("🏆 Proyecto Vanguardia-IA News | Blanca Yesenia Hernández")
