
import streamlit as st
import pandas as pd
import psycopg2
from groq import Groq

# 1. Configuración de la página
st.set_page_config(page_title="Vanguardia-IA", page_icon="☀️", layout="wide")

# 2. Estilo CSS para que sea IDÉNTICO a tu captura (Botones de colores)
st.markdown("""
    <style>
    /* Fondo gris claro de la app */
    .stApp { background-color: #f0f2f6; }
    
    /* Botón Limpiar Historial (Gris claro) */
    div.stButton > button:contains("Limpiar Historial") {
        background-color: #e9ecef !important;
        color: #495057 !important;
        border: none !important;
    }

    /* Botón del nombre (Verde claro) */
    div.stButton > button:contains("Blanca Yesenia Hernández") {
        background-color: #d4f1d4 !important;
        color: #155724 !important;
        border: none !important;
        font-weight: bold;
    }
    
    /* Botón de celebración (Amarillo) */
    div.stButton > button:contains("¡Lanzar Celebración!") {
        background-color: #f7d74a !important;
        color: #856404 !important;
        border: none !important;
        font-weight: bold;
    }

    /* Burbujas del chat blancas con sombra */
    [data-testid="stChatMessage"] {
        background-color: white !important;
        border-radius: 15px !important;
        box-shadow: 0px 2px 5px rgba(0,0,0,0.05) !important;
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
    st.write("Ir a:")
    menu = st.radio("Menú", ["🤖 Chat Inteligente", "📊 Dashboard Real"], label_visibility="collapsed")
    
    # Espaciado para bajar los botones
    st.markdown("<br>" * 12, unsafe_allow_html=True)
    
    # BOTÓN DE LIMPIAR HISTORIAL
    if st.button("🗑️ Limpiar Historial"):
        st.session_state.messages = []
        st.rerun()
    
    # BOTÓN DE TU NOMBRE
    st.button("✨ Blanca Yesenia Hernández")
    
    # BOTÓN DE CELEBRACIÓN
    if st.button("🥳 ¡Lanzar Celebración!"):
        st.balloons()
        st.snow()

# --- LÓGICA DEL CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "🤖 ☀️ 🤖 ¡Lista Blanca! Conectada a Neon y lista para el éxito. ¿Qué noticia analizamos?"}
    ]

if menu == "🤖 Chat Inteligente":
    # Mostrar mensajes
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Entrada del chat
    if prompt := st.chat_input("Escribe tu pregunta aquí..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Lógica de respuesta (RAG)
        df = obtener_datos()
        contexto = df.to_string()
        
        # --- AQUÍ PEGA TU CLAVE DE GROQ ---
        client = Groq(api_key="TU_CLAVE_GSK_AQUI") 

        # Si pides la última noticia como en tu imagen
        if "ULTIMA NOTICIA" in prompt.upper() or "ÚLTIMA NOTICIA" in prompt.upper():
            with st.chat_message("assistant"):
                st.write("🤖 **Última Noticia de Vanguardia-IA**")
                st.table(df.tail(1))
            st.session_state.messages.append({"role": "assistant", "content": "Mostré la tabla de la última noticia."})
        else:
            try:
                response = client.chat.completions.create(
                    messages=[{"role": "user", "content": f"Basado en estos datos: {contexto}. Responde a: {prompt}. Si no sabes, di exactamente: Blanca, busqué en Neon pero no hay registros que coincidan. ¡Aquí no inventamos datos! 😉"}],
                    model="llama3-8b-8192",
                )
                answer = response.choices[0].message.content
                with st.chat_message("assistant"):
                    st.write(f"☀️ {answer}")
                st.session_state.messages.append({"role": "assistant", "content": f"☀️ {answer}"})
            except:
                st.error("Revisa tu API Key de Groq.")

# --- SECCIÓN DEL DASHBOARD ---
elif menu == "📊 Dashboard Real":
    st.title("📊 Dashboard Real de Noticias")
    df = obtener_datos()
    if not df.empty:
        st.write("### Datos actuales en Neon")
        st.dataframe(df, use_container_width=True)
        st.write("### Estadísticas")
        st.bar_chart(df['title'].value_counts())
