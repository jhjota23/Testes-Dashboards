# import streamlit as st

# st.title("Hello Thais 👋")
# st.markdown(
#     """ 
#     This is a playground for you to try Streamlit and have fun. 

#     **There's :rainbow[so much] you can build!**
    
#     We prepared a few examples for you to get started. Just 
#     click on the buttons above and discover what you can do 
#     with Streamlit. 
#     """
# )

# if st.button("Send balloons!"):
#     st.balloons()

import streamlit as st

st.title("Manuella!! Boa noite, amor!! 👋")

st.markdown(
    """ 
    <p style="font-size:24px;">
    Fiz esse site teste como um convite pra te chamar pra sair.
    Para que os Americanos não te tirem mais do sério!  
    Como você é uma mulher séria e quase uma diplomata, preciso de convites formais!
    </p>
    
    <p style="font-size:20px;"><b>Ainda estamos em fase de teste</b></p>

    <p style="font-size:24px;">
    Existe uma ideia para que possamos nos ver, agora que moramos perto,  
    para tomarmos uma cerveja (ou qualquer drink que exista) juntos.
    </p>

    <p style="font-size:24px;">
    Estava pensando em criar um formulário mas vou fazer isso no chat mesmo.
    </p>

    <p style="font-size:24px;">
    Preciso somente do seu aval!
    </p>
    
    <p style="font-size:20px;"><b>Os botões de resposta são interativos...</b></p>
    
      <style>
    div.stButton > button {
        font-size: 24px !important;
        padding: 15px 30px;
        width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)  # Criando duas colunas para os botões

with col1:
    if st.button("Sim, vida, vamos!!! 😊"):
        st.image("https://i.pinimg.com/originals/6e/c4/27/6ec427a589efc2de3fdf3a47123fe5c5.gif", width=800)   
        st.success("Que bom! Vamos continuar juntos 🚀")
        st.balloons()

with col2:
    if st.button("Não, seu otario!! 😢"):
        st.error("Poxa, que pena!")
        st.snow()  # Efeito de neve para variar um pouco
        st.image("https://pbs.twimg.com/media/FMFEuJVWYAYtq9E.jpg", width=800)  

st.image ("https://i.gifer.com/CNJy.gif", width=300)

  
        