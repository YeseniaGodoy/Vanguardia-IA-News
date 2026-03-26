import streamlit as st
from groq import Groq
import pandas as pd
import psycopg2

# ==========================================
# 🎨 CONFIGURACIÓN Y ESTILO "GLASSMORPHISM"
# ==========================================
st.set_page_config(
    page_title="Vanguardia-IA News | Analista Pro",
    page_icon="☀️",
    layout="wide"
)

# Inyectamos CSS para el fondo degradado y las tarjetas modernas
st.markdown("""
<style>
    /* Fondo Degradado Profesional */
    .stApp {
        background: linear-gradient(135deg, #020617, #0f172a);
        color: #e2e8f0;
    }
    /* Sidebar Elegante */
    section[data-testid="stSidebar"] {
        background: #020617;
        border-right: 1px solid #1e293b;
    }
    /* Tarjetas con efecto de cristal */
    .card {
        background: rgba(255,255,255,0.05);
        padding: 20px;
        border-radius: 15px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 15px;
        text-align: center;
    }
    h1, h2, h3 { color: #f8fafc; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 🔑 SEGURIDAD Y CONEXIÓN (Tus Secrets)
# ==========================================
try:
    groq_api_key = st.secrets["GROQ_API_KEY"]
    db_url = st.secrets["DB_URL"]
    client = Groq(api_key=groq_api_key)
except Exception:
    st.error("⚠️ Error: Configura GROQ_API_KEY y DB_URL en los Secrets de Streamlit.")
    st.stop()

# ==========================================
# 💾 EXTRACCIÓN DE DATOS REALES (NEON)
# ==========================================
@st.cache_data(ttl=600)
def cargar_datos_reales():
    try:
        conn = psycopg2.connect(db_url)
        # Usamos tu tabla exacta: noticias_tecnologia
        query = "SELECT title, description FROM noticias_tecnologia LIMIT 20;"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error de base de datos: {e}")
        return pd.DataFrame()

df_noticias = cargar_datos_reales()

# Preparamos el contexto para la IA (Grounding)
contexto_ia = ""
for _, row in df_noticias.iterrows():
    contexto_ia += f"TITULO: {row['title']}\nDESCRIPCIÓN: {row['description']}\n---\n"

# ==========================================
# 🌳 PANEL LATERAL (SIDEBAR)
# ==========================================
with st.sidebar:
    st.title("🌳 Panel Vanguardia")
    st.markdown("---")
    # Menú de navegación
    opcion = st.radio("Ir a:", ["🤖 Asistente IA", "📊 Dashboard Real"])
    
    st.markdown("---")
    st.write("**Desarrolladora:**")
    st.success("✨ Blanca Yesenia Hernández")
