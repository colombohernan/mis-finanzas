import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Finanzas Hernán", layout="wide")

# URL de tu planilla
url = "https://docs.google.com/spreadsheets/d/1itclMhNivPPL4SAWCmGWnOe4Xtx3Xvs_jM4mCzxLThs/edit?usp=sharing"

# CONEXIÓN
conn = st.connection("gsheets", type=GSheetsConnection)

# LEER DATOS
try:
    df = conn.read(spreadsheet=url, worksheet="Hoja 1", ttl="0")
except Exception as e:
    st.error(f"Error al leer la planilla: {e}")
    df = pd.DataFrame()

BANCOS = ["SANTANDER", "BBVA", "CUENTA DNI", "MERCADO PAGO", "VISA SANTANDER", "VISA BBVA", "MASTER MP", "CREDICCOP"]

st.title("💸 Mis Finanzas Pro")

with st.sidebar:
    st.header("📝 Cargar o Ajustar")
    tipo = st.radio("Tipo", ["Gasto", "Ingreso", "Ajuste"], horizontal=True)
    monto = st.number_input("Importe ($)", min_value=0.0)
    medio = st.selectbox("Banco/Tarjeta", BANCOS)
    
    if st.button("Guardar Movimiento"):
        # CREAR LA NUEVA FILA
        nueva_fila = pd.DataFrame([{
            "Fecha": datetime.now().strftime("%d/%m/%Y"),
            "Tipo": "Ingreso" if tipo in ["Ingreso", "Ajuste"] else "Gasto",
            "Categoría": tipo.upper(),
            "Importe": monto,
            "Medio de Pago": medio,
            "Notas": "Carga desde App"
        }])
        
        # UNIR DATOS
        df_actualizado = pd.concat([df, nueva_fila], ignore_index=True)
        
        # GUARDAR EN GOOGLE SHEETS
        try:
            conn.update(spreadsheet=url, worksheet="Hoja 1", data=df_actualizado)
            st.success("¡Movimiento guardado con éxito!")
            st.balloons()
            st.rerun()
        except Exception as e:
            st.error(f"Error al guardar: {e}")

# MOSTRAR TABLA PRINCIPAL
st.write("### Resumen de Movimientos")
if not df.empty:
    st.dataframe(df, use_container_width=True)
else:
    st.info("La planilla está vacía o no se pudo leer. Si cargás un movimiento aparecerá aquí.")
