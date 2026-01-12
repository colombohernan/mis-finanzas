import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Finanzas Hernán", layout="wide")

# URL de tu planilla (la que ya me pasaste)
url = "https://docs.google.com/spreadsheets/d/1itclMhNivPPL4SAWCmGWnOe4Xtx3Xvs_jM4mCzxLThs/edit?usp=sharing"

# CONEXIÓN
conn = st.connection("gsheets", type=GSheetsConnection)

# LEER DATOS: Usamos el link directo y el nombre de tu pestaña
df = conn.read(spreadsheet=url, worksheet="Hoja 1", ttl="0")

BANCOS = ["SANTANDER", "BBVA", "CUENTA DNI", "MERCADO PAGO", "VISA SANTANDER", "VISA BBVA", "MASTER MP", "CREDICCOP"]

st.title("💸 Mis Finanzas Pro")

with st.sidebar:
    st.header("📝 Cargar o Ajustar")
    tipo = st.radio("Tipo", ["Gasto", "Ingreso", "Ajuste"], horizontal=True)
    monto = st.number_input("Importe ($)", min_value=0.0)
    medio = st.selectbox("Banco/Tarjeta", BANCOS)
    
    if st.button("Guardar Movimiento"):
        nueva_fila = pd.DataFrame([{
            "Fecha": datetime.now().strftime("%d/%m/%Y"),
            "Tipo": "Ingreso" if tipo in ["Ingreso", "Ajuste"] else "Gasto",
            "Categoría": tipo.upper(),
            "Importe": monto,

