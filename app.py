import os
import streamlit as st

from src.services.data_service import carregar_dados, baixar_taco, PATH_TACO


def main():
    st.set_page_config(page_title="NutriStream", layout="wide", page_icon="🥗")

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
        st.header("Seu Perfil")

    with tab_biblioteca:
        st.header("Consulta de Alimentos")
        if df_taco is not None:
            st.subheader("📊 Prévia da Base de Dados")
            # Exibindo as 3 primeiras linhas como solicitado
            st.dataframe(df_taco.head(3), use_container_width=True)
            st.toast("Tabela carregada!", icon="✅")
        else:
            st.error("Base de dados ausente.")

        with st.expander("  ⚙️ Configurações do Sistema"):
            if st.button("🔄 Forçar Atualização da Base TACO"):
                with st.spinner("Atualizando..."):
                    if baixar_taco():
                        st.success("Dados atualizados com sucesso! 🚀")
                        st.rerun()

    with tab_cardapio:
        st.header("Montagem do Cardápio Diário")


if __name__ == "__main__":
    main()
