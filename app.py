import streamlit as st
import pandas as pd
import psycopg2
from groq import Groq

# 1. Configuración de la página (Título y Icono)
st.set_page_config(page_title="Vanguardia-IA", page_icon="☀️", layout="wide")

# 2. Estilo CSS para que sea IDÉNTICO a tu captura
st.markdown("""
    <style>
    /* Fondo de la aplicación */
    .stApp {
        background-color: #f0f2f6;
    }
    
    /* Botón verde con tu nombre */
    div.stButton > button:first-child {
        background-color: #c1e1c1;
        color: #2e4a2e;
        border: none;
        font-weight: bold;
        width: 100%;
    }

    /* Botón amarillo de celebración */
    div.stButton > button:last-child {
        background-color: #f7d358;
        color: #4a3e10;
        border: none;
        font-weight: bold;
        width: 100%;
    }

    /* Estilo para los mensajes del chat */
    .stChatMessage {
        background-color: white;
        border-radius: 15px;
        padding: 10px;
        margin-bottom: 10px;
        box-shadow: 0px 2px 5px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Conexión a la base de datos Neon
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
    # Menú de navegación
    menu = st.radio("Navegación", ["🤖 Chat Inteligente", "📊 Dashboard Real"], label_visibility="collapsed")
    
    # Espaciado y botones finales como en tu imagen
    st.markdown("<br>" * 10, unsafe_allow_html=True)
    
    if st.button("🗑️ Limpiar Historial"):
        st.session_state.messages = []
        st.rerun()
        
    st.button("✨ Blanca Yesenia Hernández")
    
    if st.button("🥳 ¡Lanzar Celebración!"):
        st.balloons()
        st.snow()

# --- LÓGICA DEL CHAT ---
if "messages" not in st.session_state:
    # Mensaje inicial idéntico a tu captura
    st.session_state.messages = [
        {"role": "assistant", "content": "🤖 ☀️ 🤖 ¡Lista Blanca! Conectada a Neon y lista para el éxito. ¿Qué noticia analizamos?"}
    ]

if menu == "🤖 Chat Inteligente":
    # Mostrar el historial de mensajes
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Entrada de texto del usuario
    if prompt := st.chat_input("Escribe tu pregunta aquí..."):
        # Agregar mensaje del usuario al historial
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Lógica RAG (Recuperar datos de Neon)
        df = obtener_datos()
        contexto = df.to_string()
        
        # --- CONFIGURACIÓN DE GROQ ---
        # PEGA TU CLAVE AQUÍ:
        client = Groq(api_key="TU_CLAVE_DE_GROQ_AQUI")

        # Caso especial: Si preguntas por la última noticia (como en tu captura)
        if "ULTIMA NOTICIA" in prompt.upper() or "ÚLTIMA NOTICIA" in prompt.upper():
            with st.chat_message("assistant"):
                st.write("🤖 **Última Noticia de Vanguardia-IA**")
                st.table(df.tail(1))
            st.session_state.messages.append({"role": "assistant", "content": "Mostré la tabla de la última noticia."})
        
        else:
            # Respuesta general de la IA
            try:
                prompt_full = f"""
                Eres Vanguardia-IA. Usa estos datos de Neon: {contexto}
                Responde a: {prompt}
                Si no está en los datos, di exactamente: 
                "Blanca, busqué en Neon pero no hay registros que coincidan. ¡Aquí no inventamos datos! 😉"
                """
                
                completion = client.chat.completions.create(
                    model="llama3-8b-8192",
                    messages=[{"role": "user", "content": prompt_full}]
                )
                
                respuesta = completion.choices[0].message.content
                full_response = f"☀️ {respuesta}"
                
                with st.chat_message("assistant"):
                    st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
            except Exception as e:
                st.error("Error al conectar con Groq. Revisa tu API Key.")

# --- SECCIÓN DEL DASHBOARD ---
elif menu == "📊 Dashboard Real":
    st.title("📊 Dashboard Real de Noticias")
    df = obtener_datos()
    if not df.empty:
        st.write("### Datos actuales en la nube (Neon)")
        st.dataframe(df, use_container_width=True)
        st.write("### Frecuencia de Noticias")
        st.bar_chart(df['title'].value_counts())
    else:
        st.warning("No hay datos en la base de datos.")
