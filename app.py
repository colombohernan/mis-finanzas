import streamlit as st
import pandas as pd
from datetime import datetime

# --- CONFIGURACIÓN ---
# Tu link de Google Sheets ya está configurado
URL_ORIGINAL = "https://docs.google.com/spreadsheets/d/1itclMhNivPPL4SAWCmGWnOe4Xtx3Xvs_jM4mCzxLThs/edit?usp=sharing"
SHEET_URL = URL_ORIGINAL.split('/edit')[0] + "/export?format=csv"

st.set_page_config(page_title="Finanzas Hernán", layout="wide")

# Función para leer datos
def leer_datos():
    try:
        # Agregamos un parámetro para evitar que guarde caché y ver los datos al instante
        return pd.read_csv(SHEET_URL)
    except:
        return pd.DataFrame(columns=["Fecha", "Tipo", "Categoría", "Importe", "Medio de Pago", "Notas"])

df = leer_datos()

# Listas de configuración
BANCOS = ["SANTANDER", "BBVA", "CUENTA DNI", "MERCADO PAGO", "VISA SANTANDER", "VISA BBVA", "MASTER MP", "CREDICCOP"]
CAT_GASTOS = ["COMIDA", "COMBUSTIBLE", "PEAJE", "SEGUROS", "MUTUAL", "STREAMING", "TELEFONIA", "IMPUESTOS", "ROPA", "REGALOS", "PAGO TARJETA", "OTROS"]
CAT_INGRESOS = ["SUELDO", "OTROS INGRESOS", "AJUSTE"]

def formata_moneda(valor):
    return f"$ {float(valor):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

# --- BARRA LATERAL (SIDEBAR) ---
with st.sidebar:
    st.header("📝 Cargar Movimiento")
    tipo = st.radio("Tipo", ["Gasto", "Ingreso"], horizontal=True)
    fecha = st.date_input("Fecha", datetime.now())
    cat = st.selectbox("Categoría", CAT_GASTOS if tipo == "Gasto" else CAT_INGRESOS)
    monto = st.number_input("Importe ($)", min_value=0.0, step=100.0)
    medio = st.selectbox("Medio de Pago", BANCOS)
    nota = st.text_input("Nota")
    
    st.info("Nota: Por ahora, anotá el gasto en tu Google Sheet y la app lo mostrará al actualizar.")
    if st.button("Actualizar Datos", use_container_width=True):
        st.rerun()

# --- PANTALLA PRINCIPAL ---
st.title("💸 Mis Finanzas Pro")

# --- MOSTRAR SALDOS ---
st.subheader("Saldos Actuales")
c1, c2, c3, c4 = st.columns(4)
c5, c6, c7, c8 = st.columns(4)
cols = [c1, c2, c3, c4, c5, c6, c7, c8]

for i, banco in enumerate(BANCOS):
    # Filtramos por banco
    d_b = df[df["Medio de Pago"] == banco]
    # Calculamos ingresos y gastos convirtiendo a número por las dudas
    ing = pd.to_numeric(d_b[d_b["Tipo"] == "Ingreso"]["Importe"], errors='coerce').sum()
    gas = pd.to_numeric(d_b[d_b["Tipo"] == "Gasto"]["Importe"], errors='coerce').sum()
    
    saldo = ing - gas
    cols[i].metric(banco, formata_moneda(saldo))

st.divider()

# --- TABLA DE HISTORIAL ---
st.subheader("Últimos Movimientos")
# Mostramos los últimos 20 movimientos, los más nuevos arriba
if not df.empty:
    st.dataframe(df.sort_index(ascending=False).head(20), use_container_width=True, hide_index=True)
else:
    st.write("No hay datos en la planilla de Google todavía.")
