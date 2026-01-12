import streamlit as st
import pandas as pd
from datetime import datetime

# CONFIGURACIÓN DE LA PLANILLA (Pegá tu link acá)
# Reemplaza el link de abajo por el tuyo de Google Sheets
SHEET_URL = "TU_LINK_DE_GOOGLE_SHEETS_AQUI/export?format=csv"

st.set_page_config(page_title="Finanzas Hernán", layout="wide")

# Función para leer datos
def leer_datos():
    try:
        return pd.read_csv(SHEET_URL)
    except:
        return pd.DataFrame(columns=["Fecha", "Tipo", "Categoría", "Importe", "Medio de Pago", "Notas"])

df = leer_datos()

# --- EL RESTO DEL CÓDIGO QUE YA TENÍAS ---
st.title("💸 Mis Finanzas Pro")
# (Aquí va el resto de la lógica de saldos y carga)
