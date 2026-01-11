import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. Configuración de página
st.set_page_config(page_title="Mis Finanzas Pro", layout="wide", initial_sidebar_state="collapsed")

FILE_NAME = "mis_finanzas.csv"

BANCOS = ["SANTANDER", "BBVA", "CUENTA DNI", "MERCADO PAGO", "VISA SANTANDER", "VISA BBVA", "MASTER MP", "CREDICCOP"]
CATEGORIAS_GASTOS = ["COMIDA", "COMBUSTIBLE", "PEAJE", "SEGUROS", "MUTUAL", "SERVICIOS STREAMING", "TELEFONIA/INTERNET", "IMPUESTOS/EXPENSAS", "ROPA", "REGALOS", "PAGO DE TARJETA", "OTROS GASTOS"]
CATEGORIAS_INGRESOS = ["SUELDO", "OTROS INGRESOS", "AJUSTE DE SALDO", "PAGO DE TARJETA"]

def cargar_datos():
    if os.path.exists(FILE_NAME):
        try:
            df_cargado = pd.read_csv(FILE_NAME)
            df_cargado['Fecha'] = pd.to_datetime(df_cargado['Fecha'], errors='coerce')
            df_cargado['Fecha'] = df_cargado['Fecha'].fillna(datetime.now())
            df_cargado['Importe'] = pd.to_numeric(df_cargado['Importe'], errors='coerce').fillna(0.0)
            return df_cargado
        except:
            return pd.DataFrame(columns=["Fecha", "Tipo", "Categoría", "Importe", "Medio de Pago", "Notas"])
    return pd.DataFrame(columns=["Fecha", "Tipo", "Categoría", "Importe", "Medio de Pago", "Notas"])

def formata_moneda(valor):
    try:
        return f"$ {float(valor):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    except:
        return "$ 0,00"

df = cargar_datos()
if "Notas" not in df.columns: df["Notas"] = ""

# --- BARRA LATERAL (SIDEBAR) ---
with st.sidebar:
    st.header("⚙️ Ajustar Saldo")
    st.write("Sincronizá el saldo de la app con tu saldo bancario real.")
    b_aj = st.selectbox("Cuenta a corregir", BANCOS, key="sb_b")
    m_aj = st.number_input("Saldo Real ($)", min_value=0.0, key="sb_m")
    
    if st.button("Aplicar Ajuste", use_container_width=True):
        d_b = df[df["Medio de Pago"] == b_aj]
        actual = d_b[d_b["Tipo"] == "Ingreso"]["Importe"].sum() - d_b[d_b["Tipo"] == "Gasto"]["Importe"].sum()
        dif = m_aj - actual
        if dif != 0:
            nuevo_aj = {
                "Fecha": datetime.now(), 
                "Tipo": "Ingreso" if dif >= 0 else "Gasto", 
                "Categoría": "AJUSTE DE SALDO", 
                "Importe": abs(dif), 
                "Medio de Pago": b_aj, 
                "Notas": "Ajuste manual de saldo"
            }
            df = pd.concat([df, pd.DataFrame([nuevo_aj])], ignore_index=True)
            df.to_csv(FILE_NAME, index=False)
            st.success("¡Saldo ajustado!")
            st.rerun()

# --- CUERPO PRINCIPAL ---
st.title("💸 Mis Finanzas Pro")

# 2. SALDOS EN MÉTRICTAS
st.subheader("Saldos por Entidad")
c1, c2, c3, c4 = st.columns(4)
c5, c6, c7, c8 = st.columns(4)
cols = [c1, c2, c3, c4, c5, c6, c7, c8]

for i, banco in enumerate(BANCOS):
    d_banco = df[df["Medio de Pago"] == banco]
    ing = d_banco[d_banco["Tipo"] == "Ingreso"]["Importe"].sum()
    gas = d_banco[d_banco["Tipo"] == "Gasto"]["Importe"].sum()
    cols[i].metric(banco, formata_moneda(ing - gas))

st.divider()

# 3. CARGA Y TABLA
col_izq, col_der = st.columns([1, 1.2])

with col_izq:
    tab1, tab2 = st.tabs(["➕ Nuevo Movimiento", "🔄 Transferir / Pagar"])
    
    with tab1:
        t = st.radio("Tipo", ["Gasto", "Ingreso"], horizontal=True)
        cat = st.selectbox("Categoría", CATEGORIAS_GASTOS if t == "Gasto" else CATEGORIAS_INGRESOS)
        m = st.number_input("Importe ($)", min_value=0.0, step=100.0)
        med = st.selectbox("Medio de Pago", BANCOS)
        n = st.text_input("Nota")
        if st.button("Guardar", use_container_width=True):
            nuevo = {"Fecha": datetime.now(), "Tipo": t, "Categoría": cat, "Importe": m, "Medio de Pago": med, "Notas": n}
            df = pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True)
            df.to_csv(FILE_NAME, index=False)
            st.rerun()

    with tab2:
        origen = st.selectbox("Desde", BANCOS, key="t_o")
        destino = st.selectbox("Hacia", BANCOS, key="t_d")
        m_t = st.number_input("Monto ($)", min_value=0.0, step=1000.0, key="t_m")
        if st.button("Confirmar", use_container_width=True):
            if m_t > 0 and origen != destino:
                f = datetime.now()
                r1 = {"Fecha": f, "Tipo": "Gasto", "Categoría": "PAGO DE TARJETA", "Importe": m_t, "Medio de Pago": origen, "Notas": f"A {destino}"}
                r2 = {"Fecha": f, "Tipo": "Ingreso", "Categoría": "PAGO DE TARJETA", "Importe": m_t, "Medio de Pago": destino, "Notas": f"De {origen}"}
                df = pd.concat([df, pd.DataFrame([r1, r2])], ignore_index=True)
                df.to_csv(FILE_NAME, index=False)
                st.rerun()

    with st.expander("📊 Reporte de Gastos"):
        gastos_df = df[df["Tipo"] == "Gasto"]
        if not gastos_df.empty:
            resumen = gastos_df.groupby("Categoría")["Importe"].sum().sort_values(ascending=False)
            st.bar_chart(resumen)
            st.table(resumen.apply(formata_moneda))

with col_der:
    st.subheader("Historial")
    if not df.empty:
        df_v = df.copy().sort_values("Fecha", ascending=False).head(20)
        df_v["Fecha"] = df_v["Fecha"].dt.strftime("%d/%m/%Y %H:%M")
        df_v["Importe"] = df_v["Importe"].apply(formata_moneda)
        st.dataframe(df_v[["Fecha", "Categoría", "Importe", "Medio de Pago", "Notas"]], use_container_width=True, hide_index=True)