import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Finanzas Hernán", layout="wide")

# CONEXIÓN CON GOOGLE SHEETS (Usa los datos de los Secrets)
conn = st.connection("gsheets", type=GSheetsConnection)

# LEER DATOS: Usamos el nombre de la pestaña "Hoja 1"
df = conn.read(worksheet="Hoja 1", ttl="0")

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
        
        # Unir datos viejos con el nuevo
        df_actualizado = pd.concat([df, nueva_fila], ignore_index=True)
        
        # ACTUALIZAR: Aquí le decimos que escriba en "Hoja 1"
        conn.update(worksheet="Hoja 1", data=df_actualizado)
        st.success("¡Guardado correctamente!")
        st.balloons()

# Mostrar la tabla en la pantalla principal para ver que funciona
st.write("### Últimos movimientos registrados")
st.dataframe(df)
