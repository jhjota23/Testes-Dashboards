import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Teste Dashboard", layout="wide")

st.title("✅ Streamlit funcionando")

base = Path(__file__).parent
st.write("📁 Pasta atual:", base)
st.write("📄 Arquivos:", [p.name for p in base.iterdir()])

xlsx = base / "resumo_receita_liquida.xlsx"

if xlsx.exists():
    st.success("Excel encontrado!")
    df = pd.read_excel(xlsx, sheet_name="Resumo", skiprows=1)
    st.dataframe(df, use_container_width=True)
else:
    st.error("Excel NÃO encontrado na pasta.")
