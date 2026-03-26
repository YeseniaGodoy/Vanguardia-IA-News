import streamlit as st
from groq import Groq
import pandas as pd
import psycopg2

# ==========================================
# 💎 CONFIGURACIÓN PREMIUM
# ==========================================
st.set_page_config(page_title="Vanguardia-IA News Pro", page_icon="☀️", layout="wide")

# Estilos Pro
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%); color: #1e293b; }
    .metric-card { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); text-align: center; border: 1px solid #e2e8f0; }
    h1, h2, h3 { color: #0f172a !important; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 🔌 CONEXIÓN A BASE DE DATOS
# ==========================================
def conectar_db():
    try:
        return psycopg2.connect(st.secrets["DB_URL"])
    except:
        return None

# ==========================================
# 🌳 SIDEBAR (Menú de Navegación)
# ==========================================
with st.sidebar:
    st.title("🌳 Menú Principal")
    st.markdown("---")
    # OPCIONES DE NAVEGACIÓN
    opcion = st.radio("Ir a:", ["🤖 Chat Inteligente", "📊 Dashboard Real"])
    st.markdown("---")
    st.success("👩‍💻 Blanca Yesenia Hernández")
    if st.button("🎉 Celebrar"): st.balloons()

# ==========================================
# 📈 SECCIÓN 1: DASHBOARD REAL
# ==========================================
if opcion == "📊 Dashboard Real":
    st.title("📊 Dashboard de Noticias Neon")
    st.markdown("### Análisis en tiempo real de tu base de datos")
    
    conn = conectar_db()
    if conn:
        # Consulta para el gráfico
        query = "SELECT title FROM noticias_tecnologia;"
        df = pd.read_sql(query, conn)
        conn.close()
        
        # MÉTRICAS ARRIBA
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f'<div class="metric-card"><h3>Total Noticias</h3><h2>{len(df)}</h2></div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="metric-card"><h3>Estado Base de Datos</h3><h2 style="color:green;">Conectado ✅</h2></div>', unsafe_allow_html=True)
        
        st.write("---")
        
        # GRÁFICO DE BARRAS (Simulando frecuencia por palabra clave o solo listado)
        st.subheader("📈 Distribución de Contenido")
        if not df.empty:
            # Creamos un gráfico sencillo basado en la longitud de los títulos para mostrar algo visual
            df['Longitud_Titulo'] = df['title'].apply(len)
            st.bar_chart(df.set_index('title')['Longitud_Titulo'])
            st.caption("Gráfico interactivo: Longitud de caracteres por noticia guardada.")
        else:
            st.warning("No hay noticias para graficar todavía.")
    else:
        st.error("No se pudo conectar a Neon para mostrar gráficos.")

# ==========================================
# 🤖 SECCIÓN 2: CHATBOT (Tu código exitoso)
# ==========================================
else:
    st.title("☀️ Vanguardia-IA News 📰")
    st.info("Analista Experta en Noticias | Arquitectura RAG")

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "☀️ ¡Hola Blanca! Lista para analizar tus datos de Neon. 🌳"}]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Consulta tu base de datos..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("🧠 Consultando Neon..."):
                try:
                    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                    # Cargamos contexto para el RAG
                    conn = conectar_db()
                    df_ctx = pd.read_sql("SELECT title, description FROM noticias_tecnologia LIMIT 5;", conn)
                    conn.close()
                    contexto = df_ctx.to_string()

                    response = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[
                            {"role": "system", "content": f"Eres analista de Blanca Yesenia. Base de datos: {contexto}. Si no está ahí, di que no lo sabes."},
                            {"role": "user", "content": prompt}
                        ]
                    )
                    res = response.choices[0].message.content
                    st.markdown(res)
                    st.session_state.messages.append({"role": "assistant", "content": res})
                except Exception as e:
                    st.error(f"Error: {e}")
