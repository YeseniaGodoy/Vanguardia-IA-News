import streamlit as st
import pandas as pd
from groq import Groq
import os

# 1. CONFIGURACIÓN DE LA PÁGINA (Debe ser lo primero)
st.set_page_config(page_title="Vanguardia-IA News", page_icon="🧠", layout="wide")

# 2. TU ESTILO PREMIUM (El diseño oscuro que te gusta)
st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #020617, #0f172a); color: #e2e8f0; }
section[data-testid="stSidebar"] { background: #020617; border-right: 1px solid #1e293b; }
h1, h2, h3 { color: #f8fafc; }
.card { background: rgba(255,255,255,0.05); padding: 20px; border-radius: 15px; backdrop-filter: blur(12px); margin-bottom: 15px; border: 1px solid rgba(255,255,255,0.08); text-align: center; }
.user-msg { background: linear-gradient(135deg, #2563eb, #3b82f6); padding: 12px; border-radius: 12px; margin: 8px 0; text-align: right; }
.bot-msg { background: rgba(255,255,255,0.08); padding: 12px; border-radius: 12px; margin: 8px 0; }
</style>
""", unsafe_allow_html=True)

# 3. SIDEBAR CON EL SOL, EL ÁRBOL Y GLOBOS
with st.sidebar:
    st.markdown("## ☀️🌳 Vanguardia-IA") # Aquí están tus íconos
    st.caption("Análisis inteligente de noticias")
    st.markdown("---")
    pagina = st.radio("Menú", ["🤖 Chatbot", "📊 Dashboard"])
    st.markdown("---")
    st.success("✨ Blanca Yesenia Hernández")
    # EL BOTÓN DE LOS GLOBOS
    if st.button("🎉 Celebrar"):
        st.balloons()

# 4. HEADER Y MÉTRICAS (Las que ya tenías en tu diseño)
st.markdown("# 🧠 Plataforma Inteligente de Noticias")
col1, col2, col3 = st.columns(3)
with col1: st.markdown('<div class="card">📊 <h2>150</h2> Noticias Analizadas</div>', unsafe_allow_html=True)
with col2: st.markdown('<div class="card">🔥 <h2>IA</h2> Tendencia Principal</div>', unsafe_allow_html=True)
with col3: st.markdown('<div class="card">⚡ <h2>+35%</h2> Crecimiento</div>', unsafe_allow_html=True)

st.markdown("---")

# 5. LÓGICA DEL CHATBOT (Conexión real a Groq)
if pagina == "🤖 Chatbot":
    st.subheader("🤖 Asistente Virtual")

    # Inicializar historial de chat
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Mostrar historial con estilos
    for msg in st.session_state.messages:
        role_class = "user-msg" if msg["role"] == "user" else "bot-msg"
        st.markdown(f"<div class='{role_class}'>{msg['content']}</div>", unsafe_allow_html=True)

    # Entrada de texto (chat input)
    prompt = st.chat_input("Escribe tu consulta sobre noticias...")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Mostrar el mensaje del usuario inmediatamente
        st.markdown(f"<div class='user-msg'>{prompt}</div>", unsafe_allow_html=True)
        
        with st.spinner("🔍 Analizando datos en tiempo real..."):
            try:
                # Conexión real con Groq usando la clave de Secrets
                client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                
                chat_completion = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama3-8b-8192", # Modelo sugerido para la Guía 8
                )
                respuesta = chat_completion.choices[0].message.content
                
                # Mostrar la respuesta de la IA
                st.markdown(f"<div class='bot-msg'>{respuesta}</div>", unsafe_allow_html=True)
                st.session_state.messages.append({"role": "assistant", "content": respuesta})
                
            except Exception as e:
                # Error detallado si la conexión falla
                st.error(f"⚠️ Error al conectar con la IA. Verifica tu GROQ_API_KEY en los Secrets.")
                st.info("Asegúrate de haber reiniciado la app después de guardar la clave.")

# 6. DASHBOARD (Gráficas que ya tenías en tu diseño)
else:
    st.subheader("📊 Dashboard de Tendencias")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="card">📈 Crecimiento de menciones (IA vs Tradicional)</div>', unsafe_allow_html=True)
        # Datos de ejemplo para la gráfica
        chart_data = pd.DataFrame({
            'Mes': ['Ene', 'Feb', 'Mar', 'Abr', 'May'],
            'IA': [10, 30, 60, 110, 150],
            'Tradicional': [50, 48, 45, 42, 40]
        })
        st.line_chart(chart_data.set_index('Mes'))
        
    with col2:
        st.markdown('<div class="card">📊 Distribución de temas populares (Última semana)</div>', unsafe_allow_html=True)
        st.bar_chart({"Ciberseguridad": 70, "Big Data": 45, "Nube": 90, "IA": 150})
