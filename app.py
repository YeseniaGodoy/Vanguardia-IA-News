import streamlit as st
import pandas as pd
import psycopg2
from groq import Groq

# 1. Configuración de la página
st.set_page_config(page_title="Vanguardia-IA News", layout="wide")

# 2. Conexión a la Base de Datos (Neon)
def conectar_db():
    try:
        # Tu cadena de conexión a Neon
        conn = psycopg2.connect("postgresql://neondb_owner:npg_W9Yof7aAnGgF@ep-round-sun-a5v5pbe9-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require")
        return conn
    except Exception as e:
        st.error(f"Error al conectar con la base de datos: {e}")
        return None

# 3. Función para obtener las noticias (OLAP)
def obtener_noticias():
    conn = conectar_db()
    if conn:
        query = "SELECT title, description FROM noticias_tecnologia"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    return pd.DataFrame()

# --- DISEÑO DE LA PÁGINA (UI) ---
st.title("Vanguardia-IA News ☀️")
st.markdown("### Innovación y Verdad en cada Noticia")
st.write("---")

# Barra lateral con el Panel de Control y el Árbol
st.sidebar.title("🌳 Panel de Control")
st.sidebar.write("Bienvenida, Blanca Yesenia")
opcion = st.sidebar.radio("Selecciona una sección:", ["Chat con IA", "Dashboard de Noticias"])

# --- SECCIÓN: CHAT CON IA (RAG) ---
if opcion == "Chat con IA":
    st.subheader("🤖 Pregúntale a nuestra IA sobre Tecnología")
    st.write("Esta IA consulta directamente nuestra base de datos en Neon.")
    
    pregunta = st.text_input("Escribe tu duda aquí (Ejemplo: ¿Qué hay de Seagate?):")

    if pregunta:
        df_noticias = obtener_noticias()
        
        # Unimos las noticias para darle contexto a la IA (Arquitectura RAG)
        contexto = ""
        for index, row in df_noticias.iterrows():
            contexto += f"Título: {row['title']}\nDescripción: {row['description']}\n\n"
        
        # Configuración de Groq
        # ¡RECUERDA PEGAR TU CLAVE gsk_ AQUÍ ABAJO!
        client = Groq(api_key="TU_CLAVE_DE_GROQ_AQUI")
        
        prompt_final = f"""
        Eres un asistente de noticias llamado Vanguardia-IA. 
        Tu base de datos es la siguiente información:
        {contexto}
        
        Usa SOLO esa información para responder de forma clara. 
        Si la pregunta no tiene relación con los datos, responde exactamente esto:
        "Blanca, busqué en Neon pero no hay registros que coincidan. ¡Aquí no inventamos datos! 😉"
        
        Pregunta del usuario: {pregunta}
        """

        try:
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt_final}],
                model="llama3-8b-8192",
            )
            respuesta = chat_completion.choices[0].message.content
            st.info(respuesta)
        except Exception as e:
            st.warning("Asegúrate de configurar tu API Key de Groq correctamente.")

# --- SECCIÓN: DASHBOARD (VISUALIZACIÓN) ---
elif opcion == "Dashboard de Noticias":
    st.subheader("📊 Análisis de Noticias en Tiempo Real")
    df = obtener_noticias()
    
    if not df.empty:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Noticias Totales", len(df))
        with col2:
            st.success("Base de Datos: Conectada ✅")
            
        st.write("### Lista de Noticias en Neon")
        st.dataframe(df, use_container_width=True)
        
        st.write("### Gráfico de Frecuencia")
        st.bar_chart(df['title'].value_counts())
    else:
        st.warning("No hay noticias registradas todavía en la base de datos.")

# Botón de globos para el cierre de la defensa
st.sidebar.write("---")
if st.sidebar.button("Celebrar éxito 🎈"):
    st.balloons()
    st.toast("¡Felicidades por tu defensa, Blanca!")
