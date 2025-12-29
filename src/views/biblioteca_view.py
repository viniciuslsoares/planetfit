import streamlit as st
from src.services.data_service import baixar_taco


def render_biblioteca(df_taco):
    st.header("🍎 Biblioteca TACO & Receitas")

    if df_taco is not None:
        st.subheader("🔍 Buscar Alimentos")
        busca = st.text_input(
            "Digite o nome do alimento para filtrar:",
            placeholder="Ex: Frango, Arroz, Ovo...",
        )

        if busca:
            resultado = df_taco[
                df_taco["alimento"].str.contains(busca, case=False, na=False)
            ]
            st.write(f"Encontrados {len(resultado)} resultados:")
            st.dataframe(resultado, width="stretch")
        else:
            st.subheader("📊 Prévia da Base de Dados")
            st.dataframe(df_taco.head(5), width="stretch")
            st.caption(
                "Mostrando os 10 primeiros itens. Use a busca acima para encontrar alimentos específicos."
            )

        st.divider()

        with st.expander("⚙️ Gerenciar Base de Dados"):
            st.write(
                "Se os dados estiverem desatualizados, você pode forçar um novo download."
            )
            if st.button("🔄 Atualizar Tabela TACO"):
                with st.spinner("Sincronizando com o servidor..."):
                    if baixar_taco():
                        st.success("Dados atualizados! Reiniciando aplicação...")
                        st.rerun()
    else:
        st.error(
            "Não foi possível carregar a base de dados. Verifique sua conexão e tente atualizar."
        )
