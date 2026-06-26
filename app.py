import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import streamlit.components.v1 as components
import os

# Configuração da página
st.set_page_config(layout="wide", page_title="MATRIZ-VITRUVIANA-INTEGRADA")

# Inicialização segura do Firebase
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(cred)
    except Exception as e:
        st.error(f"Erro ao inicializar Firebase: {e}")

db = firestore.client()

st.title("🩺 MATRIZ-VITRUVIANA-INTEGRADA")

# Renderização do arquivo HTML consolidado
# Certifique-se de que o ficheiro gemini-code-1782418389976.html está na pasta raiz
arquivo_html = "gemini-code-1782418389976.html"

if os.path.exists(arquivo_html):
    with open(arquivo_html, "r", encoding="utf-8") as f:
        html_code = f.read()
    
    # Renderiza o componente interativo
    components.html(html_code, height=950, scrolling=True)
else:
    st.error(f"Erro: O arquivo '{arquivo_html}' não foi encontrado na pasta raiz.")

# Exibição do banco de dados (Histórico)
st.divider()
st.subheader("📋 Registro de Consultas no Firebase")
try:
    docs = db.collection('Pacientes').stream()
    data = [d.to_dict() for d in docs]
    if data:
        st.table(data)
    else:
        st.info("Nenhum dado registrado no Firebase ainda.")
except Exception as e:
    st.warning("Aguardando conexão com banco de dados.")