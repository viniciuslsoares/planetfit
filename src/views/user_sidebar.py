import streamlit as st
from src.models.user_model import get_all_usernames
from src.controllers.user_controller import UserController


def render_user_sidebar():
    with st.sidebar:
        st.title("👤 Gerenciamento de Perfil")

        with st.expander("✨ Criar Novo Perfil"):
            novo_nome = st.text_input("Nome do usuário")
            if st.button("Cadastrar"):
                UserController.create_new_user(novo_nome)

        usuarios = get_all_usernames()
        if usuarios:
            usuario_atual = st.session_state.get("usuario_ativo")
            try:
                idx = (
                    usuarios.index(usuario_atual) if usuario_atual in usuarios else None
                )
            except ValueError:
                idx = None

            escolha = st.selectbox(
                "Trocar de Perfil",
                usuarios,
                index=idx,
                placeholder="Selecione um perfil...",
            )

            if escolha and escolha != usuario_atual:
                UserController.login_user(escolha)

        st.divider()

        if st.session_state.get("usuario_ativo"):
            st.success(f"Logado: **{st.session_state.usuario_ativo}**")
            if st.button("💾 Salvar Manualmente", use_container_width=True):
                UserController.save_current_state()
                st.toast("Progresso salvo!")
        else:
            st.warning("Nenhum usuário logado. As alterações serão perdidas.")
