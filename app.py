import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Finanzas Hernán", layout="wide")

# Usamos solo el ID de la planilla para evitar errores de caracteres raros
SPREADSHEET_ID = "1itclMhNivPPL4SAWCmGWnOe4Xtx3Xvs_jM4mCzxLThs"
# Construimos la URL de exportación básica
url = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit#gid=0"

conn = st.connection("gsheets", type=GSheetsConnection)

# LEER DATOS - Si falla, creamos un DataFrame vacío para que no veas el error rojo
try:
    df = conn.read(spreadsheet=url, worksheet="Hoja 1", ttl="0")
except Exception:
    df = pd.DataFrame(columns=["Fecha", "Tipo", "Categoría", "Importe", "Medio de Pago", "Notas"])

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
            "Medio de Pago": medio,
            "Notas": "Carga desde App"
        }])
        
        df_actualizado = pd.concat([df, nueva_fila], ignore_index=True)
        
        try:
            conn.update(spreadsheet=url, worksheet="Hoja 1", data=df_actualizado)
            st.success("¡Guardado!")
            st.balloons()
            st.rerun()
        except Exception as e:
            st.error(f"Error al guardar: {e}")

# MOSTRAR TABLA
st.write("### Resumen de Movimientos")
st.dataframe(df, use_container_width=True)
