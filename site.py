import streamlit as st
from pathlib import Path

# ✅ set_page_config deve vir logo após os imports
st.set_page_config(page_title="Pietra 💖", page_icon="💘")

# ====== PATH DA IMAGEM (robusto p/ Cloud e Windows) ======
IMG = Path(__file__).parent / "assets" / "foto_casal_pietra.jpeg"

# ====== ESTADO ======
if "step" not in st.session_state:
    st.session_state.step = 0

def next_step():
    st.session_state.step += 1

def prev_step():
    st.session_state.step = max(0, st.session_state.step - 1)

# ====== ESTILO ======
st.markdown(
    """
    <style>
    div.stButton > button {
        font-size: 24px !important;
        padding: 15px 30px;
        width: 100%;
        border-radius: 14px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ====== UI AUX ======
total_steps = 4
st.progress(min(st.session_state.step, total_steps) / total_steps)

# ====== ETAPA 0 ======
if st.session_state.step == 0:
    st.title("Pietra!! Boa noite, amor!! 👋")
    st.markdown('<p style="font-size:24px;">Fiz só esse teste, prometo</p>', unsafe_allow_html=True)

    # ✅ Debug + fallback (pra você enxergar o que tá acontecendo no Cloud)
    st.caption(f"🖼️ Procurando imagem em: {IMG}")
    if IMG.exists():
        # leitura em bytes é ainda mais “blindada” no Cloud
        st.image(IMG.read_bytes(), width=800)
    else:
        st.error("Não encontrei a imagem no deploy.")
        # lista o que existe na pasta e em assets/ pra diagnosticar rápido
        try:
            st.write("Arquivos na pasta do app:", sorted([p.name for p in Path(__file__).parent.iterdir()]))
        except Exception as e:
            st.write("Não consegui listar a pasta do app:", e)

        assets_dir = Path(__file__).parent / "assets"
        if assets_dir.exists():
            st.write("Arquivos em assets/:", sorted([p.name for p in assets_dir.iterdir()]))
        else:
            st.write("A pasta assets/ não existe no deploy.")

    # 🎵 Botão da música (YouTube Music – funciona sempre)
    st.markdown(
        """
        <a href="https://music.youtube.com/watch?v=mRNcPbCJNJ8" target="_blank" style="text-decoration:none;">
            <button style="
                font-size:22px;
                padding:14px 28px;
                border-radius:14px;
                background:#ff4b4b;
                color:white;
                border:none;
                cursor:pointer;
                width:100%;
                margin-bottom:20px;
                ">
                ▶️ Pra ouvir enquanto responde
            </button>
        </a>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Começar 😊"):
            next_step()
            st.rerun()
    with col2:
        st.write("")

# ====== ETAPA 1 ======
elif st.session_state.step == 1:
    st.markdown('<p style="font-size:22px;"><b>Posso propor algo? 👀</b></p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Sim, vida!"):
            st.session_state.resposta1 = "sim"
            next_step()
            st.rerun()

    if st.button("⬅️ Voltar"):
        prev_step()
        st.rerun()

# ====== ETAPA 2 ======
elif st.session_state.step == 2:
    if st.session_state.get("resposta1") == "sim":
        st.image(
            "https://i.pinimg.com/originals/6e/c4/27/6ec427a589efc2de3fdf3a47123fe5c5.gif",
            width=300
        )
        st.success("😭💖")
        st.balloons()
    else:
        st.error("Poxa 😢 (tô dramatizando)")
        st.snow()
        st.image("https://pbs.twimg.com/media/FMFEuJVWYAYtq9E.jpg", width=300)

    st.markdown(
        '<p style="font-size:22px;"><b>Próxima etapa:</b> Escolhe o nosso próximo passeio 👇</p>',
        unsafe_allow_html=True
    )

    opcao = st.radio(
        "Qual você prefere?",
        [
            "Pizza 🍕 (Glória Pizza Bar)",
            "Cinema 🎬 (Bugônia ou Foi Apenas um Acidente)",
            "Tour prepara o BYD pra mim pelo Centro + Baguete da Metrópole",
        ],
        index=0
    )

    if st.button("Continuar ➡️"):
        st.session_state.role = opcao
        next_step()
        st.rerun()

    if st.button("⬅️ Voltar"):
        prev_step()
        st.rerun()

# ====== ETAPA 3 ======
elif st.session_state.step == 3:
    role = st.session_state.get("role", "—")

    if "bora_clicked" not in st.session_state:
        st.session_state.bora_clicked = False

    if "Glória Pizza Bar" in role:
        titulo = "Pizza, vinho e risada fácil 🍕🍷"
        mensagem = "Então fechou: Mesa no Glória, pizza e a gente julga os vinhos!"
    elif "Cinema" in role:
        titulo = "Cinema juntinhos 🎬🍿"
        mensagem = "Então fechou: filme e pipoca MANTEIGUDA."
    else:
        titulo = "Passeio gostosinho pelo Centro 🏙️🥖"
        mensagem = "Então fechou: Baguete da Metrópole e a gente conhece uns brechós ruins"

    st.markdown(f'<p style="font-size:26px;"><b>{titulo}</b></p>', unsafe_allow_html=True)
    st.success(mensagem)

    if not st.session_state.bora_clicked:
        st.markdown('<p style="font-size:20px;">Se é isso mesmo, aperta “Bora!” 👇</p>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Bora! 🚀"):
                st.session_state.bora_clicked = True
                st.rerun()

        with col2:
            if st.button("Quero trocar 😅"):
                prev_step()
                st.rerun()
    else:
        st.markdown('<p style="font-size:32px; text-align:center;">Te amo ❤️</p>', unsafe_allow_html=True)

        if st.button("Continuar 😊"):
            st.session_state.bora_clicked = False
            next_step()
            st.rerun()

# ====== ETAPA 4 (FINAL) ======
else:
    st.success("Prontinho 😎💘 Formulário finalizado!")
    st.write("Resumo:")
    st.write("- Resposta 1:", st.session_state.get("resposta1"))
    st.write("- Rolê:", st.session_state.get("role"))

    if st.button("🔁 Recomeçar"):
        st.session_state.step = 0
        for k in ["resposta1", "role", "bora_clicked"]:
            if k in st.session_state:
                del st.session_state[k]
        st.rerun()
