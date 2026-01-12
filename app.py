import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Finanzas Hernán", layout="wide")

# CONEXIÓN CON GOOGLE SHEETS
conn = st.connection("gsheets", type=GSheetsConnection)

# Leer datos
df = conn.read(spreadsheet="https://docs.google.com/spreadsheets/d/1itclMhNivPPL4SAWCmGWnOe4Xtx3Xvs_jM4mCzxLThs/edit?usp=sharing", ttl="0")

BANCOS = ["SANTANDER", "BBVA", "CUENTA DNI", "MERCADO PAGO", "VISA SANTANDER", "VISA BBVA", "MASTER MP", "CREDICCOP"]

st.title("💸 Mis Finanzas Pro")

with st.sidebar:
    st.header("📝 Cargar o Ajustar")
    tipo = st.radio("Tipo", ["Gasto", "Ingreso", "Ajuste"], horizontal=True)
    monto = st.number_input("Importe ($)", min_value=0.0)
    medio = st.selectbox("Banco/Tarjeta", BANCOS)
    
    if st.button("Guardar Movimiento"):
        # AQUÍ EL CÓDIGO CREARÁ LA NUEVA FILA
        nueva_fila = pd.DataFrame([{
            "Fecha": datetime.now().strftime("%d/%m/%Y"),
            "Tipo": "Ingreso" if tipo in ["Ingreso", "Ajuste"] else "Gasto",
            "Categoría": tipo.upper(),
            "Importe": monto,
            "Medio de Pago": medio,
            "Notas": "Carga desde App"
        }])
        df_actualizado = pd.concat([df, nueva_fila], ignore_index=True)
        conn.update(spreadsheet="https://docs.google.com/spreadsheets/d/1itclMhNivPPL4SAWCmGWnOe4Xtx3Xvs_jM4mCzxLThs/edit?usp=sharing", data=df_actualizado)
        st.success("¡Guardado! Refrescá la página.")
