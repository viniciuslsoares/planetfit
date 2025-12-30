import os
import streamlit as st

from src.services.data_service import carregar_dados, baixar_taco, PATH_TACO
from src.services.state_service import init_session_state
from src.controllers.user_controller import UserController

from src.views.user_sidebar import render_user_sidebar
from src.views.perfil_view import render_perfil
from src.views.biblioteca_view import render_biblioteca
from src.views.receitas_view import render_receitas
from src.views.cardapio_view import render_cardapio


def main():
    st.set_page_config(
        page_title="NutriStream",
        layout="wide",
        page_icon="🥗",
        initial_sidebar_state="expanded",
    )

    init_session_state()

    if not os.path.exists(PATH_TACO):
        if baixar_taco():
            st.toast("Base TACO baixada com sucesso!", icon="🥗")

    df_taco = carregar_dados()

    render_user_sidebar()

    st.title("🥗 NutriStream")
    st.caption(f"Usuário Ativo: **{st.session_state.get('usuario_ativo', 'Nenhum')}**")

    tab_perfil, tab_biblioteca, tab_receitas, tab_cardapio = st.tabs(
        [
            "🎯 Perfil & Metas",
            "🍎 Biblioteca Global",
            "👨‍🍳 Criar Receitas",
            "📝 Meu Cardápio",
        ]
    )

    with tab_perfil:
        render_perfil()

    with tab_biblioteca:
        render_biblioteca(df_taco)

    with tab_receitas:
        render_receitas(df_taco)

    with tab_cardapio:
        render_cardapio()

    st.sidebar.markdown("---")
    st.sidebar.caption("v1.0.0 | Arquitetura MVC")


if __name__ == "__main__":
    main()
