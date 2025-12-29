import os
import streamlit as st

from src.services.data_service import carregar_dados, baixar_taco, PATH_TACO
from src.services.state_service import init_session_state
from src.views.perfil_view import render_perfil
from src.views.biblioteca_view import render_biblioteca
from src.views.cardapio_view import render_cardapio


def main():
    st.set_page_config(page_title="NutriStream", layout="wide", page_icon="🥗")

    init_session_state()

    if not os.path.exists(PATH_TACO):
        if baixar_taco():
            st.toast("Base TACO baixada com sucesso!", icon="🥗")

    df_taco = carregar_dados()

    st.title("🥗 NutriStream")
    st.caption("Planejador de Dieta Inteligente - Base TACO")

    tab_metas, tab_biblioteca, tab_cardapio = st.tabs(
        ["🎯 Perfil & Metas", "🍎 Biblioteca TACO & Receitas", "📝 Meu Cardápio"]
    )

    with tab_metas:
        render_perfil()

    with tab_biblioteca:
        render_biblioteca(df_taco)

    with tab_cardapio:
        render_cardapio()


if __name__ == "__main__":
    main()
