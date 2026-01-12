import streamlit as st
import pandas as pd
from datetime import datetime

# --- CONFIGURACIÓN DE LA PLANILLA ---
# REEMPLAZA ESTE LINK por el que copiaste de tu Google Sheets
# Importante: El link debe terminar en /export?format=csv para que funcione
URL_ORIGINAL = "TU_LINK_DE_GOOGLE_SHEETS_AQUI"
SHEET_URL = URL_ORIGINAL.split('/edit')[0] + "/export?format=csv"

st.set_page_config(page_title="Finanzas Hernán", layout="wide")

# Función para leer datos desde Google Sheets
def leer_datos():
    try:
        # Forzamos a pandas a leer el CSV desde la nube
        return pd.read_csv(SHEET_URL)
    except Exception as e:
        st.error(f"Error al conectar con la planilla: {e}")
        return pd.DataFrame(columns=["Fecha", "Tipo", "Categoría", "Importe", "Medio de Pago", "Notas"])

# Cargar datos
df = leer_datos()

# Listas de configuración
BANCOS = ["SANTANDER", "BBVA", "CUENTA DNI", "MERCADO PAGO", "VISA SANTANDER", "VISA BBVA", "MASTER MP", "CREDICCOP"]
CAT_GASTOS = ["COMIDA", "COMBUSTIBLE", "PEAJE", "SEGUROS", "MUTUAL", "STREAMING", "TELEFONIA", "IMPUESTOS", "ROPA", "REGALOS", "PAGO TARJETA", "OTROS"]
CAT_INGRESOS = ["SUELDO", "OTROS INGRESOS", "AJUSTE", "PAGO TARJETA"]

def formata_moneda(valor):
    return f"$ {float(valor):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

st.title("💸 Mis Finanzas Pro (Nube)")

# --- MOSTRAR SALDOS ---
c1, c2, c3, c4 = st.columns(4)
c5, c6, c7, c8 = st.columns(4)
cols = [c1, c2, c3, c4, c5, c6, c7, c8]

for i, banco in enumerate(BANCOS):
    d_b = df[df["Medio de Pago"] == banco]
    ing = pd.to_numeric(d_b[d_b["Tipo"] == "Ingreso"]["Importe"], errors='coerce').sum()
    gas = pd.to_numeric(d_b[d_b["Tipo"] == "Gasto"]["Importe"], errors='coerce').sum()
    cols[i].metric(banco, formata_moneda(ing - gas))

st.divider()

# --- FORMULARIO DE CARGA ---
col_izq, col_der = st.columns([1, 1.2])

with col_izq:
    tipo = st.radio("Tipo", ["Gasto", "Ingreso"], horizontal=True)
    cat = st.selectbox("Categoría", CAT_GASTOS if tipo == "Gasto" else CAT_INGRESOS)
    monto = st.number_input("Importe ($)", min_value=0.0, step=100.0)
    medio = st.selectbox("Medio de Pago", BANCOS)
    nota = st.text_input("Nota")
    
    if st.button("Guardar Movimiento", use_container_width=True):
        st.warning("Para guardar datos permanentemente desde Streamlit Cloud se requiere configuración de 'Secrets' o usar la API de Google. Por ahora, registra este gasto manualmente en tu Google Sheet y la app lo mostrará al actualizar.")

with col_der:
    st.subheader("Historial (Desde Google Sheets)")
    st.dataframe(df.sort_index(ascending=False).head(15), use_container_width=True, hide_index=True)
