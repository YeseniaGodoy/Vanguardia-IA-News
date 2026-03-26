import streamlit as st
import pandas as pd
import requests
import psycopg2

# Configuración basada en la Guía de Groq (Pág. 3)
API_URL = "https://api.groq.com/openai/v1/chat/completions"

# 1. Interfaz tipo Chatbot (Paso 1 del ingeniero)
st.set_page_config(page_title="Vanguardia-IA", page_icon="🤖")
st.title("🤖 Vanguardia-IA News")
st.write("Analista inteligente de noticias desde la base de datos.")

# 2. Función para obtener el DataFrame (Paso de la pizarra)
def obtener_contexto_db():
    try:
        # Se conecta a Neon usando los secretos de la web
        conn = psycopg2.connect(st.secrets["DB_URL"])
        query = "SELECT title, description FROM noticias_tecnologia LIMIT 10"
        df = pd.read_sql(query, conn)
        conn.close()
        return df.to_string(index=False)
    except:
        return "Error al conectar con la base de datos de noticias."

# Inicializar historial de mensajes
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "¡Hola! Soy tu analista IA. ¿Qué quieres saber sobre tus noticias?"}]

# Mostrar mensajes
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 3. Caja de texto tipo WhatsApp (Input del usuario)
if prompt := st.chat_input("Escribe tu consulta..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # 4. Enviar a la API de Groq (Paso 2 del ingeniero / Pág. 4 de la guía)
    with st.spinner("IA analizando datos de Neon..."):
        contexto = obtener_contexto_db()
        headers = {
            "Authorization": f"Bearer {st.secrets['GROQ_API_KEY']}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "system", "content": f"Eres un analista. Responde solo basado en estos datos: {contexto}"},
                {"role": "user", "content": prompt}
            ]
        }
        
        response = requests.post(API_URL, headers=headers, json=data)
        res_json = response.json()
        
        # Extraer respuesta según formato de la guía (Pág. 4)
        if "choices" in res_json:
            respuesta = res_json["choices"][0]["message"]["content"]
        else:
            respuesta = "Lo siento, tuve un problema al procesar la información."

        st.session_state.messages.append({"role": "assistant", "content": respuesta})
        st.chat_message("assistant").write(respuesta)
