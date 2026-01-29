import streamlit as st
import pandas as pd
from pathlib import Path
import streamlit.components.v1 as components
import plotly.graph_objects as go

st.set_page_config(layout="wide")

# ====== ARQUIVOS ======
base = Path(__file__).parent
xlsx = base / "resumo_receita_liquida.xlsx"

# Logo BMW está na raiz do repo (conforme seu print)
logo_bmw = base / "bmw.png"
logo_url = "https://raw.githubusercontent.com/jhjota23/Testes-Dashboards/main/bmw.png"

# ====== HEADER ======
def render_header():
    left, mid, right = st.columns([1.2, 6, 3])

    with left:
        if logo_bmw.exists():
            st.image(str(logo_bmw), width=120)
        else:
            st.image(logo_url, width=120)

    with mid:
        st.markdown(
            """
            <div style="padding-top:6px;">
                <div style="font-size:38px; font-weight:900; line-height:1;">DDI PÓS VENDAS</div>
                <div style="font-size:14px; opacity:0.75; margin-top:6px;">Grupo IESA</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with right:
        c1, c2 = st.columns(2)
        with c1:
            st.selectbox("ANO", [2025], index=0, disabled=True, key="filtro_ano")
        with c2:
            st.selectbox("MÊS", ["Novembro"], index=0, disabled=True, key="filtro_mes")

    st.caption("⚠️ Por enquanto este dashboard está carregando apenas 1 mês. Quando tiver histórico, eu ligo os filtros para mudar os dados.")
    st.divider()

# CHAME APENAS UMA VEZ (logo após definir)
render_header()
        
# ====== HELPERS ======
def br_int(x):
    if pd.isna(x):
        return "—"
    return f"{int(round(x)):,}".replace(",", ".")

def br_pct(x, decimals=0):
    if pd.isna(x):
        return "—"
    return f"{x:.{decimals}%}".replace(".", ",")

def kpi_cards(items, cols=6):
    # Ajuste se cortar (pro seu layout atual ficou bem)
    height = 360

    css = f"""
    <style>
      .kpi-wrap {{
        width: 100%;
      }}
      .kpi-grid {{
        display: grid;
        grid-template-columns: repeat({cols}, minmax(0, 1fr));
        gap: 16px;
        margin: 10px 0 10px 0;
      }}
      .kpi-card {{
        border-radius: 16px;
        padding: 18px 18px;
        border: 1px solid rgba(255,255,255,0.10);
        background: rgba(255,255,255,0.06);
        box-shadow: 0 2px 10px rgba(0,0,0,0.10);
        min-height: 110px;
        display: flex;
        flex-direction: column;
        justify-content: center;
      }}
      .kpi-card.dark {{
        background: rgba(255,255,255,0.18);
        border: 1px solid rgba(255,255,255,0.20);
      }}
      .kpi-value {{
        font-size: 40px;
        font-weight: 800;
        line-height: 1.05;
        letter-spacing: -0.5px;
        margin-bottom: 8px;
        color: white;
      }}
      .kpi-label {{
        font-size: 14px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        opacity: 0.85;
        color: white;
      }}
      @media (max-width: 1200px) {{
        .kpi-grid {{ grid-template-columns: repeat(3, minmax(0, 1fr)); }}
      }}
      @media (max-width: 700px) {{
        .kpi-grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
        .kpi-value {{ font-size: 34px; }}
      }}
    </style>
    """

    cards = ""
    for it in items:
        variant = "dark" if it.get("variant") == "dark" else ""
        cards += f"""
          <div class="kpi-card {variant}">
            <div class="kpi-value">{it["value"]}</div>
            <div class="kpi-label">{it["label"]}</div>
          </div>
        """

    html = f"""
    {css}
    <div class="kpi-wrap">
      <div class="kpi-grid">
        {cards}
      </div>
    </div>
    """

    components.html(html, height=height, scrolling=False)

# ====== HEADER (logo + título + filtros visuais) ======
left, mid, right = st.columns([1.2, 6, 3])

with left:
    if logo_bmw.exists():
        st.image(str(logo_bmw), width=120)

with mid:
    st.markdown(
        """
        <div style="padding-top:6px;">
            <div style="font-size:38px; font-weight:900; line-height:1;">DDI PÓS VENDAS</div>
            <div style="font-size:14px; opacity:0.75; margin-top:6px;">Grupo IESA</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with right:
    c1, c2 = st.columns(2)
    with c1:
        ano = st.selectbox("ANO", [2025], index=0, disabled=True)
    with c2:
        mes = st.selectbox("MÊS", ["Novembro"], index=0, disabled=True)

st.caption("⚠️ Por enquanto este dashboard está carregando apenas 1 mês. Quando tiver histórico, eu ligo os filtros para mudar os dados.")
st.divider()

# ====== LEITURA EXCEL ======
df = pd.read_excel(xlsx, sheet_name="Resumo", skiprows=1).dropna(axis=1, how="all")

# ====== TIPOS ======
num_cols = [
    "TOTAL", "PEÇAS", "SERVIÇO", "CMV", "PASS.", "OS ABT.", "OS ABT. (R$)",
    "CONTÁBIL", "FÍSICO", "TRÂN.", "REC. PROJ.", "VALOR", "REC. LIQ."
]
for c in num_cols:
    if c in df.columns:
        df[c] = pd.to_numeric(df[c], errors="coerce")

# % OBJ. (Excel em número normal: 64,56 -> 0,6456)
if "% OBJ." in df.columns:
    s = pd.to_numeric(df["% OBJ."], errors="coerce")
    df["% OBJ."] = ss = s.where(s <= 1, s / 100)

# ====== LINHA TOTAL ======
total_row = df.loc[df["LOJA"].astype(str).str.strip().str.lower() == "total"]
total = total_row.iloc[0] if not total_row.empty else df.iloc[-1]

# ====== CARDS ======
items = [
    {"value": br_int(total.get("TOTAL")),         "label": "REC. LIQ. TOTAL",     "variant": "light"},
    {"value": br_int(total.get("PEÇAS")),         "label": "REC. LIQ. PEÇAS",     "variant": "light"},
    {"value": br_int(total.get("SERVIÇO")),       "label": "REC. LIQ. SERVIÇOS",  "variant": "light"},
    {"value": br_int(total.get("CMV")),           "label": "CMV",                 "variant": "light"},
    {"value": br_int(total.get("VALOR")),         "label": "VALOR OBJETIVO",      "variant": "light"},
    {"value": br_int(total.get("CONTÁBIL")),      "label": "ESTOQUE CONTÁBIL",    "variant": "dark"},

    {"value": br_int(total.get("OS ABT. (R$)")),  "label": "OS EM ABERTO (R$)",   "variant": "light"},
    {"value": br_pct((total.get("PEÇAS") / total.get("TOTAL")) if total.get("TOTAL") else pd.NA, 1),
     "label": "% MARGEM LIQ. PEÇAS", "variant": "light"},
    {"value": br_int(total.get("PASS.")),         "label": "PASSAGENS FECHADAS",  "variant": "light"},
    {"value": br_int(total.get("TRÂN.")),         "label": "VALOR COMPRAS",       "variant": "light"},
    {"value": br_pct(total.get("% OBJ."), 0),     "label": "% ATING. OBJ. PROJ.", "variant": "light"},
    {"value": br_int(total.get("FÍSICO")),        "label": "ESTOQUE FÍSICO",      "variant": "dark"},
]

kpi_cards(items, cols=6)
st.divider()

# ====== TABELA ======
format_map = {c: "{:,.0f}" for c in num_cols if c in df.columns}
if "% OBJ." in df.columns:
    format_map["% OBJ."] = "{:.2%}"

st.dataframe(
    df.style.format(format_map, na_rep=""),
    use_container_width=True,
    hide_index=True
)

st.divider()

# ====== GRÁFICOS (abaixo da tabela) ======
periodo = "Nov 2025"  # depois você liga aos filtros quando tiver histórico

rec_pecas = float(total.get("PEÇAS", 0) or 0)
rec_serv  = float(total.get("SERVIÇO", 0) or 0)
rec_total = float(total.get("TOTAL", rec_pecas + rec_serv) or (rec_pecas + rec_serv))

cmv = float(total.get("CMV", 0) or 0)
compras = float(total.get("TRÂN.", 0) or 0)  # ajuste aqui se sua coluna compras for outra

g1, g2 = st.columns(2)

with g1:
    st.markdown("### REC. LIQ. TOTAL (PEÇAS E SERVIÇOS)")

    fig1 = go.Figure()
    fig1.add_trace(go.Bar(
        x=[periodo], y=[rec_pecas],
        name="Rec. Liq. Peças",
        text=[f"{rec_pecas:,.0f}".replace(",", ".")],
        textposition="inside"
    ))
    fig1.add_trace(go.Bar(
        x=[periodo], y=[rec_serv],
        name="Rec. Liq. Serviço",
        text=[f"{rec_serv:,.0f}".replace(",", ".")],
        textposition="inside"
    ))
    fig1.add_annotation(
        x=periodo, y=rec_total,
        text=f"<b>{rec_total:,.0f}</b>".replace(",", "."),
        showarrow=False, yshift=18
    )
    fig1.update_layout(
        barmode="stack",
        height=420,
        margin=dict(l=10, r=10, t=50, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        xaxis=dict(title=""),
        yaxis=dict(title="", showgrid=False, zeroline=False),
    )
    st.plotly_chart(fig1, use_container_width=True)

with g2:
    st.markdown("### CMV (COM INTERNA) x VALOR COMPRADO")

    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        x=[periodo], y=[cmv],
        name="CMV (COM INTERNA)",
        text=[f"{cmv:,.0f}".replace(",", ".")],
        textposition="outside"
    ))
    fig2.add_trace(go.Bar(
        x=[periodo], y=[compras],
        name="VALOR COMPRADO",
        text=[f"{compras:,.0f}".replace(",", ".")],
        textposition="outside"
    ))
    fig2.update_layout(
        barmode="group",
        height=420,
        margin=dict(l=10, r=10, t=50, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        xaxis=dict(title=""),
        yaxis=dict(title="", showgrid=False, zeroline=False),
    )
    st.plotly_chart(fig2, use_container_width=True)










