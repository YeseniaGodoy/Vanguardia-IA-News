import streamlit as st
from groq import Groq
import pandas as pd
import psycopg2

# ==========================================
# 💎 CONFIGURACIÓN PREMIUM
# ==========================================
st.set_page_config(page_title="Vanguardia-IA News Pro ✨", page_icon="☀️", layout="wide")

# --- CSS PERSONALIZADO PARA EL PRIMER LUGAR (EDICIÓN DIAMANTE) ---
st.markdown("""
<style>
    /* 1. Fondo Degradado Animado (WAVES) */
    .stApp {
        background: linear-gradient(-45deg, #ffffff, #e6f7ff, #f0fff4, #f8fafc);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        color: #1e293b;
    }
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* 2. FORZAR TEXTO NEGRO Y LEGIBLE EN TODO EL CHAT */
    .stMarkdown, p, li, span, h1, h2, h3, h4, h5, h6 {
        color: #000000 !important;
        font-family: 'Inter', sans-serif;
    }

    /* 3. Títulos Especiales (Sol y Árbol) */
    h1.main-title {
        color: #fcd34d !important; /* Amarillo Sol */
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    h3.subtitle {
        color: #166534 !important; /* Verde Árbol */
    }

    /* 4. Estilo de las Burbujas de Chat (Flotantes) */
    .stChatMessage {
        border-radius: 25px;
        padding: 18px;
        margin-bottom: 18px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        transition: transform 0.2s ease-in-out, box-shadow 0.2s;
    }
    .stChatMessage:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }

    /* 5. Colores de los Mensajes con Contraste */
    [data-testid="stChatMessageAssistant"] {
        background-color: #f8fafc !important;
        border: 1px solid #e2e8f0;
    }
    [data-testid="stChatMessageUser"] {
        background-color: #e2e8f0 !important;
        border: 1px solid #cbd5e1;
    }

    /* 6. Panel Lateral Premium */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
        box-shadow: 2px 0 5px rgba(0,0,0,0.02);
    }
    section[data-testid="stSidebar"] .stMarkdown p {
        color: #1e2937 !important;
    }

    /* 7. Botón de Celebración (Grande y Centrado) */
    .stButton>button {
        border-radius: 30px;
        width: 100%;
        background-color: #fcd34d; /* Amarillo Sol */
        color: #0f172a !important;
        font-weight: bold;
        border: none;
        transition: background-color 0.3s, transform 0.2s;
        box-shadow: 0 4px 6px -1px rgba(252, 211, 77, 0.5);
    }
    .stButton>button:hover {
        background-color: #f59e0b;
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 🔌 FUNCIONES DE BASE DE DATOS
# ==========================================
def conectar_db():
    try: return psycopg2.connect(st.secrets["DB_URL"])
    except: return None

# ==========================================
# 🌳 PANEL LATERAL PREMIUM (SIDEBAR)
# ==========================================
with st.sidebar:
    st.markdown("<h2 class='main-title'>☀️ Vanguardia-IA</h2>", unsafe_allow_html=True)
    st.markdown("<h3 class='subtitle'>🌳</h3>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 📋 Panel de Control")
    opcion = st.radio("Ir a:", ["🤖 Chat Inteligente", "📊 Dashboard Real"])
    st.markdown("---")
    st.write("**Desarrollado por:**")
    st.success("✨ Blanca Yesenia Hernández")
    st.markdown("---")
    st.caption("🏆 *Hacia el primer lugar*")
    st.write("---")
    if st.button("🎉 ¡Lanzar Celebración!"): st.balloons()

# ==========================================
# 📈 SECCIÓN 1: DASHBOARD REAL
# ==========================================
if opcion == "📊 Dashboard Real":
    st.title("📊 Dashboard de Noticias Neon")
    st.markdown("### Análisis en tiempo real de tu base de datos")
    
    conn = conectar_db()
    if conn:
        df = pd.read_sql("SELECT title FROM noticias_tecnologia;", conn)
        conn.close()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Noticias en Neon", len(df))
        with col2:
            st.markdown('<div style="text-align:center;"><h3>Base de Datos</h3><h2 style="color:green;">Conectado ✅</h2></div>', unsafe_allow_html=True)
        
        st.write("---")
        
        if not df.empty:
            st.subheader("📈 Distribución de Contenido")
            # Un gráfico interactivo y elegante
            df['Letras'] = df['title'].apply(len)
            st.bar_chart(df.set_index('title')['Letras'])
    else: st.error("No se pudo conectar a Neon.")

# ==========================================
# 🤖 SECCIÓN 2: CHATBOT PREMIUM (Tu código exitoso)
# ==========================================
else:
    st.markdown("<h1 class='main-title'>☀️ Vanguardia-IA News 📰</h1>", unsafe_allow_html=True)
    st.markdown("<h4 class='subtitle'>*Analista Experta en Noticias Basada en Datos Reales*</h4>", unsafe_allow_html=True)
    st.write("---")

    if "messages" not in st.session_state:
        # Mensaje de bienvenida Premium con iconos
        st.session_state.messages = [{"role": "assistant", "content": "☀️🤖 **¡Bienvenida Blanca Yesenia!** Soy tu analista de IA. He leído tu base de datos y estoy lista para darte respuestas **reales y verificadas**. 🌳 ¿Qué noticias deseas analizar hoy?"}]

    # Mostrar historial con avatares (Usamos emojis)
    for msg in st.session_state.messages:
        avatar = "☀️🤖" if msg["role"] == "assistant" else "👩‍💻"
        with st.chat_message(msg["role"], avatar=avatar): st.markdown(msg["content"])

    if prompt := st.chat_input("Escribe tu consulta aquí..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👩‍💻"): st.markdown(prompt)

        with st.chat_message("assistant", avatar="☀️🤖"):
            # SPINNER PERSONALIZADO CON EL SOL
            with st.spinner("☀️🧠 Consultando Neon..."):
                try:
                    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                    conn = conectar_db()
                    df_ctx = pd.read_sql("SELECT title, description FROM noticias_tecnologia LIMIT 5;", conn)
                    conn.close()
                    contexto = df_ctx.to_string()

                    response = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[
                            {"role": "system", "content": f"Eres analista de Blanca Yesenia. Base de datos: {contexto}. Si no está ahí, di que no lo sabes."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.1
                    )
                    res = response.choices[0].message.content
                    st.markdown(res)
                    st.session_state.messages.append({"role": "assistant", "content": res})
                except Exception as e:
                    st.error(f"Error: {e}")

st.write("---")
# CAPTION FINAL PROFESIONAL
st.caption("🏆 Proyecto Vanguardia-IA News | Blanca Yesenia Hernández | 2026")
