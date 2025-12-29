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
                "peso": 70.0,
                "altura": 170.0,
                "idade": 25,
                "sexo": "Masculino",
                "atividade": "Sedentário",
            },
            "cardapio": [],
        }

    if "auth" not in st.session_state:
        st.session_state.auth = {"logado": False}
