import streamlit as st
import pandas as pd
import psycopg2
from groq import Groq

# 1. Configuración de la página y Estilo
st.set_page_config(page_title="Vanguardia-IA News ☀️", layout="wide")

# Estilo personalizado para que se vea profesional
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #007bff; color: white; }
    .stTextInput>div>div>input { border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Conexión a la Base de Datos (Neon - OLTP)
def conectar_db():
    try:
        # Reemplaza con tus datos reales de Neon si son diferentes
        conn = psycopg2.connect("postgresql://neondb_owner:npg_W9Yof7aAnGgF@ep-round-sun-a5v5pbe9-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require")
        return conn
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return None

# 3. Función para obtener noticias (Análisis OLAP rápido)
def obtener_noticias():
    conn = conectar_db()
    if conn:
        df = pd.read_sql_query("SELECT title, description FROM noticias_tecnologia", conn)
        conn.close()
        return df
    return pd.DataFrame()

# --- BARRA LATERAL (EL MENÚ DEL ÁRBOL) ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3858/3858693.png", width=100)
st.sidebar.title("🌳 Panel de Control")
st.sidebar.markdown("---")
opcion = st.sidebar.radio("Ir a:", ["🤖 Chat Inteligente", "📊 Dashboard Real", "✨ Créditos"])

# --- SECCIÓN 1: CHAT INTELIGENTE (IA con RAG) ---
if opcion == "🤖 Chat Inteligente":
    st.title("Vanguardia-IA News ☀️")
    st.subheader("Tu IA honesta que no alucina")
    
    pregunta = st.text_input("Hazme una pregunta sobre las noticias en Neon:")

    if pregunta:
        df_noticias = obtener_noticias()
        # Creamos el contexto (RAG)
        contexto = "\n".join([f"- {t}: {d}" for t, d in zip(df_noticias['title'], df_noticias['description'])])
        
        client = Groq(api_key="TU_API_KEY_AQUI") # Asegúrate de poner tu clave de Groq
        
        prompt = f"""
        Eres una IA honesta llamada Vanguardia-IA. 
        Solo puedes responder basándote en esta información:
        {contexto}
        
        Si la respuesta no está en el texto anterior, responde exactamente: 
        "Blanca, busqué en Neon pero no hay registros que coincidan. ¡Aquí no inventamos datos! 😉"
        
        Pregunta: {pregunta}
        """
        
        try:
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.1-8b-instant",
            )
            respuesta = chat_completion.choices[0].message.content
            st.info(respuesta)
        except:
            st.warning("Configura tu API Key de Groq para que la IA responda.")

# --- SECCIÓN 2: DASHBOARD (Visualización de datos) ---
elif opcion == "📊 Dashboard Real":
    st.title("📊 Análisis de Datos (OLAP)")
    df = obtener_noticias()
    
    if not df.empty:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total de Noticias", len(df))
        with col2:
            st.write("Estado de la Nube: **Conectado a Neon ✅**")
            
        st.write("### Gráfico de Noticias por Título")
        # Gráfica sencilla para impresionar
        st.bar_chart(df['title'].value_counts())
        
        st.write("### Tabla de Datos Directa de Neon")
        st.dataframe(df, use_container_width=True)
    else:
        st.error("No se encontraron datos en Neon.")

# --- SECCIÓN 3: CRÉDITOS ---
else:
    st.title("✨ Presentación Final")
    st.balloons() # ¡Globos automáticos al entrar aquí!
    st.success("### Proyecto Creado por: Blanca Yesenia Hernández")
    st.write("Herramientas utilizadas:")
    st.write("- **Neon**: Base de Datos Cloud")
    st.write("- **Groq**: Motor de IA ultra rápido")
    st.write("- **Streamlit**: Interfaz de Usuario")
    
    if st.button("¡Lanzar Celebración! 🎈"):
        st.snow() # Efecto de nieve/estrellas
