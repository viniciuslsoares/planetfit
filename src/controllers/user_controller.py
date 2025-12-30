import streamlit as st
from src.models.user_model import save_user_data, load_user_data, get_all_usernames


class UserController:
    @staticmethod
    def create_new_user(username):
        if not username:
            st.error("Nome de usuário não pode ser vazio.")
            return

        # Estrutura padrão para novos usuários
        default_data = {
            "perfil": {
                "peso": 92.0,
                "altura": 178,
                "idade": 22,
                "sexo": "Masculino",
                "atividade": "Moderadamente Ativo",
                "objetivo": "Cutting Leve",
            },
            "macros_alvo": {"kcal": 0, "prot": 0, "carb": 0, "fat": 0},
            "cardapio": [],
        }
        save_user_data(username, default_data)
        UserController.login_user(username)

    @staticmethod
    def login_user(username):
        data = load_user_data(username)
        if data:
            st.session_state.dieta = data
            st.session_state.usuario_ativo = username
            st.rerun()

    @staticmethod
    def save_current_state():
        if st.session_state.get("usuario_ativo"):
            save_user_data(st.session_state.usuario_ativo, st.session_state.dieta)

    @staticmethod
    def update_profile_and_save(new_profile_data, kcal_alvo):
        if st.session_state.get("usuario_ativo"):
            # Atualiza os dados no session_state
            st.session_state.dieta["perfil"].update(new_profile_data)
            st.session_state.dieta["macros_alvo"]["kcal"] = kcal_alvo

            # Persiste no arquivo JSON
            UserController.save_current_state()
            return True
        return False
