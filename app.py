import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.title("Gestión de Finanzas - 4GO Academy")

# Conectamos usando la cuenta de servicio (Secrets)
conn = st.connection("gsheets", type=GSheetsConnection)

# Leemos los datos de la pestaña "BD"
# Cambiamos 'BD' por el nombre exacto de tu pestaña si es necesario
df = conn.read(worksheet="BD", ttl=0)

st.write("### Últimos registros")
st.dataframe(df.tail())

st.sidebar.header("Agregar Nuevo Registro")
with st.sidebar.form("formulario"):
    fecha = st.date_input("Fecha")
    detalle = st.text_input("Concepto")
    punto_venta = st.selectbox("Punto de Venta", ["MEDELLÍN", "BOGOTÁ"])
    valor = st.number_input("Valor ($)", min_value=0)
    
    boton = st.form_submit_button("Guardar Registro")

if boton:
    # Creamos la nueva fila con los nombres exactos de tus columnas
    # Según tu archivo son: FECHATRA, VLR, P. VENTA, CONCEPTO
    nueva_fila = {
        "FECHATRA": str(fecha),
        "VLR": valor,
        "P. VENTA": punto_venta,
        "CONCEPTO": detalle
    }
    
    # Agregamos la fila al final
    df = df._append(nueva_fila, ignore_index=True)
    
    # SUBIMOS LOS DATOS A GOOGLE SHEETS
    conn.update(worksheet="BD", data=df)
    st.success("¡Registro guardado exitosamente!")
    st.rerun()
