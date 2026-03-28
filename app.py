import streamlit as st
import pandas as pd
import psycopg2
from groq import Groq

# 1. Configuración de la página
st.set_page_config(page_title="Vanguardia-IA News", layout="wide")

# 2. Conexión a la Base de Datos (Neon)
def conectar_db():
    try:
        # Tu cadena de conexión actual
        conn = psycopg2.connect("postgresql://neondb_owner:npg_W9Yof7aAnGgF@ep-round-sun-a5v5pbe9-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require")
        return conn
    except Exception as e:
        st.error(f"Error al conectar con la base de datos: {e}")
        return None

# 3. Función para obtener las noticias
def obtener_noticias():
    conn = conectar_db()
    if conn:
        query = "SELECT title, description FROM noticias_tecnologia"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    return pd.DataFrame()

# --- DISEÑO DE LA PÁGINA ---
st.title("Vanguardia-IA News ☀️")
st.write("---")

# Barra lateral con el Panel de Control
st.sidebar.title("🌳 Panel de Control")
opcion = st.sidebar.radio("Selecciona una sección:", ["Chat con IA", "Dashboard de Noticias"])

# --- SECCIÓN: CHAT CON IA ---
if opcion == "Chat con IA":
    st.subheader("Pregúntale a nuestra IA sobre Tecnología")
    
    pregunta = st.text_input("Escribe tu duda aquí:")

    if pregunta:
        df_noticias = obtener_noticias()
        
        # Unimos las noticias para darle contexto a la IA
        contexto = ""
        for index, row in df_noticias.iterrows():
            contexto += f"Título: {row['title']}\nDescripción: {row['description']}\n\n"
        
        # Configuración de Groq
        # RECUERDA: Aquí va tu clave gsk_...
        client = Groq(api_key="TU_CLAVE_DE_GROQ_AQUI")
        
        prompt_final = f"""
        Eres un asistente de noticias llamado Vanguardia-IA. 
        Tu base de datos es la siguiente información:
        {contexto}
        
        Usa SOLO esa información para responder. 
        Si la pregunta no tiene relación con los datos, responde exactamente esto:
        "Blanca, busqué en Neon pero no hay registros que coincidan. ¡Aquí no inventamos datos! 😉"
        
        Pregunta del usuario: {pregunta}
        """

        try:
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt_final}],
                model="llama3-8b-8192",
