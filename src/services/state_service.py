import streamlit as st


def init_session_state():
    """
    Inicializa todas as chaves do st.session_state necessárias para o app.
    Centralizar aqui evita erros de KeyError e facilita a manutenção.
    """
    if "dieta" not in st.session_state:
        st.session_state.dieta = {
            "macros_alvo": {"kcal": 0.0, "prot": 0.0, "carb": 0.0, "fat": 0.0},
            "perfil": {
                "peso": 92.0,
                "altura": 178.0,
                "idade": 22,
                "sexo": "Masculino",
                "atividade": "Levemente Ativo",
                "objetivo": "Cutting Leve",
            },
            "cardapio": [],
        }

    if "auth" not in st.session_state:
        st.session_state.auth = {"logado": False}
