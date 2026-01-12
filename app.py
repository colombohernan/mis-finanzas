import streamlit as st
import pandas as pd
from datetime import datetime

# --- CONFIGURACIÓN ---
URL_ORIGINAL = "https://docs.google.com/spreadsheets/d/1itclMhNivPPL4SAWCmGWnOe4Xtx3Xvs_jM4mCzxLThs/edit?usp=sharing"
SHEET_URL = URL_ORIGINAL.split('/edit')[0] + "/export?format=csv"

st.set_page_config(page_title="Finanzas Hernán", layout="wide")

def leer_datos():
    try:
        return pd.read_csv(SHEET_URL)
    except:
        return pd.DataFrame(columns=["Fecha", "Tipo", "Categoría", "Importe", "Medio de Pago", "Notas"])

df = leer_datos()

BANCOS = ["SANTANDER", "BBVA", "CUENTA DNI", "MERCADO PAGO", "VISA SANTANDER", "VISA BBVA", "MASTER MP", "CREDICCOP"]
CAT_GASTOS = ["COMIDA", "COMBUSTIBLE", "PEAJE", "SEGUROS", "MUTUAL", "STREAMING", "TELEFONIA", "IMPUESTOS", "ROPA", "REGALOS", "PAGO TARJETA", "OTROS"]
CAT_INGRESOS = ["SUELDO", "OTROS INGRESOS", "AJUSTE"]

def formata_moneda(valor):
    return f"$ {float(valor):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("📝 Cargar Movimiento")
    tipo = st.radio("Tipo", ["Gasto", "Ingreso"], horizontal=True)
    fecha = st.date_input("Fecha", datetime.now())
    cat = st.selectbox("Categoría", CAT_GASTOS if tipo == "Gasto" else CAT_INGRESOS)
    monto = st.number_input("Importe ($)", min_value=0.0, step=100.0)
    medio = st.selectbox("Medio de Pago", BANCOS)
    nota = st.text_input("Nota")
    
    st.divider()
    
    # ESTO ES LO QUE EXTRAÑABAS: Ajuste rápido
    st.header("⚙️ Ajuste de Saldo")
    st.write("Si el saldo no coincide, anotá el monto real aquí:")
    banco_ajuste = st.selectbox("Banco a ajustar", BANCOS)
    nuevo_saldo = st.number_input("Saldo Actual Real ($)", min_value=0.0)
    
    st.info("Para que este cambio quede guardado, anotalo en tu Google Sheets como 'Tipo: Ingreso' y 'Categoría: AJUSTE'.")

# --- PANTALLA PRINCIPAL ---
st.title("💸 Mis Finanzas Pro")

# --- MOSTRAR SALDOS ---
st.subheader("Saldos Actuales")
c1, c2, c3, c4 = st.columns(4)
c5, c6, c7, c8 = st.columns(4)
cols = [c1, c2, c3, c4, c5, c6, c7, c8]

for i, banco in enumerate(BANCOS):
    d_b = df[df["Medio de Pago"] == banco]
    ing = pd.to_numeric(d_b[d_b["Tipo"] == "Ingreso"]["Importe"], errors='coerce').sum()
    gas = pd.to_numeric(d_b[d_b["Tipo"] == "Gasto"]["Importe"], errors='coerce').sum()
    
    saldo_calculado = ing - gas
    
    # Si estamos ajustando este banco, mostramos la diferencia
    if banco == banco_ajuste and nuevo_saldo > 0:
        diferencia = nuevo_saldo - saldo_calculado
        st.sidebar.warning(f"Diferencia para {banco}: {formata_moneda(diferencia)}")
    
    cols[i].metric(banco, formata_moneda(saldo_calculado))

st.divider()
st.subheader("Últimos Movimientos")
st.dataframe(df.sort_index(ascending=False).head(20), use_container_width=True, hide_index=True)
