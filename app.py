import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.title("Gestión de Finanzas - 4GO Academy")

# 1. Conexión con Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. Leer los datos (Aquí le pusimos la URL de tu planilla para que no se pierda)
url = "https://docs.google.com/spreadsheets/d/1itclMhNivPPL4SAWCmGWnOe4Xtx3Xvs_jM4mCzxLThs/edit"
df = conn.read(spreadsheet=url, worksheet="BD")

# 3. Mostrar los datos en la pantalla
st.write("### Datos actuales en la pestaña BD")
st.dataframe(df)


