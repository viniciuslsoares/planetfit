import streamlit as st
from src.services.data_service import baixar_taco


def render_biblioteca(df_taco):
    st.header("🍎 Biblioteca TACO & Receitas")

    if df_taco is not None:
        st.subheader("🔍 Buscar Alimentos")

        busca = st.text_input(
            "Digite o nome do alimento:",
            placeholder="Comece a digitar (ex: Arroz)...",
            key="busca_reativa",
        )

        if busca:
            mask = df_taco["alimento"].str.contains(busca, case=False, na=False)
            resultado = df_taco[mask]

            matches = len(resultado)
            total = len(df_taco)

            if matches > 0:
                col_info, col_bar = st.columns([1, 4])
                with col_info:
                    st.write(f"**{matches}** matches")
                with col_bar:
                    st.progress(matches / total)

                st.dataframe(resultado, use_container_width=True, hide_index=True)
            else:
                st.warning(f"Nenhum resultado para '{busca}'")
        else:
            st.caption("Amostra da base de dados:")
            st.dataframe(df_taco.head(5), use_container_width=True, hide_index=True)

        st.divider()

        with st.expander("⚙️ Gerenciar Base de Dados"):
            if st.button("🔄 Atualizar Tabela TACO"):
                with st.spinner("Sincronizando..."):
                    if baixar_taco():
                        st.success("Dados atualizados!")
                        st.rerun()
    else:
        st.error("Base de dados não carregada.")
