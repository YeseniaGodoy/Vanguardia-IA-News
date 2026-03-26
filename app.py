
import streamlit as st
import pandas as pd
from groq import Groq
import psycopg2

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Vanguardia-IA News", layout="wide", page_icon="🧠")

# 2. ESTILO PREMIUM (FONDO OSCURO Y TARJETAS)
st.markdown("""
    <style>
    .main { background: linear-gradient(135deg, #020617, #0f172a); color: white; }
    .stMetric { background: rgba(255,255,255,0.05); padding: 15px; border-radius: 10px; border: 1px solid #1e293b; }
    div[data-testid="stSidebar"] { background-color: #020617; border-right: 1px solid #1e293b; }
    .card { background: rgba(255,255,255,0.05); padding: 20px; border-radius: 15px; border: 1px solid rgba(255,255,255,0.1); }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR (MENÚ Y CELEBRACIÓN)
with st.sidebar:
    st.title("🌳 Vanguardia-IA")
    st.markdown("---")
    pagina = st.radio("Menú de Navegación:", ["🤖 Chatbot", "📊 Dashboard"])
    st.markdown("---")
    st.success("👩‍💻 Blanca Yesenia Hernández")
    # LOS GLOBOS QUE ME PEDISTE
    if st.button("🎉 Celebrar"):
        st.balloons()

# 4. FUNCIÓN PARA LA BASE DE DATOS NEON
def cargar_datos_neon():
    try:
        conn = psycopg2.connect(st.secrets["DB_URL"])
        query = "SELECT * FROM noticias LIMIT 10" 
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        return None

# 5. HEADER PRINCIPAL
st.title("🧠 Plataforma Inteligente de Análisis de Noticias")

# 6. PÁGINA: CHATBOT
if pagina == "🤖 Chatbot":
    st.header("🤖 Asistente Virtual")
    
    # Historial de mensajes
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Entrada del Chat
    prompt = st.chat_input("Escribe tu consulta aquí...")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                response = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama3-8b-8192",
                )
                full_response = response.choices[0].message.content
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error("⚠️ Verifica la GROQ_API_KEY en tus Secrets.")

# 7. PÁGINA: DASHBOARD
else:
    st.header("📊 Dashboard de Noticias")
    
    # Métricas de arriba
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("Noticias Totales", "150", "+12%")
    with c2: st.metric("Tendencia IA", "Alta 🔥")
    with c3: st.metric("Base de Datos", "Conectada ✅")
    
    st.markdown("---")
    
    # Mostrar tabla de Neon
    datos = cargar_datos_neon()
    if datos is not None:
        st.subheader("📋 Datos Recientes (Neon SQL)")
        st.dataframe(datos, use_container_width=True)
    else:
        st.warning("No se pudo cargar la tabla de Neon. Mostrando gráfico de ejemplo.")
        st.line_chart({"IA": [10, 25, 40, 80], "Ciberseguridad": [5, 10, 20, 35]})

    st.bar_chart({"Marzo": 50, "Abril": 80, "Mayo": 120})
