import streamlit as st
import pandas as pd
from src.services.data_service import (
    carregar_custom_foods,
    salvar_custom_foods,
    carregar_receitas,
)


def render_biblioteca(df_taco):

    df_custom = carregar_custom_foods()
    df_recipes = carregar_receitas()

    if df_taco is not None:
        df_taco_copy = df_taco.copy()
        df_taco_copy["fonte"] = "TACO"

        df_custom_copy = df_custom.copy()
        df_custom_copy["fonte"] = "Personalizado"

        df_recipes_copy = df_recipes.copy()
        df_recipes_copy["fonte"] = "Receitas"

        # Consolidação
        df_total = pd.concat(
            [df_taco_copy, df_custom_copy, df_recipes_copy], ignore_index=True
        )
    else:
        df_total = df_custom

    col_titulo, col_btn = st.columns([0.9, 0.1])

    with col_titulo:
        st.header("🍎 Biblioteca TACO & Receitas")

    with col_btn:
        if st.button("⚙️", help="Atualizar Base de Dados"):
            st.session_state.show_config = not st.session_state.get(
                "show_config", False
            )

    if df_total is not None and not df_total.empty:
        st.subheader("🔍 Buscar Alimentos")
        busca = st.text_input(
            "Digite o nome do alimento:",
            placeholder="Pesquise na TACO ou nos seus personalizados...",
            key="busca_reativa",
            label_visibility="collapsed",
        )

        if busca:
            mask = df_total["alimento"].str.contains(busca, case=False, na=False)
            resultado = df_total[mask]

            matches = len(resultado)
            total = len(df_total)

            if matches > 0:
                col_info, col_bar = st.columns([1, 4])
                with col_info:
                    st.write(f"**{matches}** matches")
                with col_bar:
                    st.progress(matches / total)

                st.dataframe(resultado, width="stretch", hide_index=True)
            else:
                st.warning(f"Nenhum resultado para '{busca}'")
        else:
            st.caption("Amostra da base consolidada (100g):")
            st.dataframe(df_total.head(5), width="stretch", hide_index=True)
    else:
        st.info(
            "Sua biblioteca está vazia. Adicione um alimento personalizado abaixo ou atualize a TACO."
        )

    st.divider()

    st.header("➕ Meus Alimentos Customizados")

    df_custom = carregar_custom_foods()

    with st.expander("➕ Cadastrar Novo Alimento"):
        with st.form("form_novo_alimento", clear_on_submit=True):
            nome = st.text_input(
                "Nome do Alimento", placeholder="Ex: Whey Protein Morango"
            )

            peso_referencia = st.number_input(
                "Peso da porção no rótulo (g)",
                min_value=1.0,
                value=100.0,
                help="Qual o peso que os macros abaixo representam?",
            )

            st.write("---")
            st.caption("📏 Unidade Caseira (Ex: 1 Fatia de pão = 25g)")
            col_u1, col_u2 = st.columns(2)
            u_nome = col_u1.text_input(
                "Nome da Unidade", placeholder="Fatia, Ovo, Pote..."
            )
            u_peso = col_u2.number_input("Peso de 1 unidade (g)", min_value=0.0)

            st.write("---")
            st.caption("Insira os macros conforme aparecem no rótulo:")

            c1, c2, c3, c4 = st.columns(4)
            kcal_raw = c1.number_input("Energia (kcal)", min_value=0.0)
            prot_raw = c2.number_input("Proteína (g)", min_value=0.0)
            lip_raw = c3.number_input("Gordura (g)", min_value=0.0)
            carb_raw = c4.number_input("Carboidrato (g)", min_value=0.0)

            c5, c6, c7 = st.columns(3)
            fibra_raw = c5.number_input("Fibra (g)", min_value=0.0)
            col_raw = c6.number_input("Colesterol (mg)", min_value=0.0)
            sod_raw = c7.number_input("Sódio (mg)", min_value=0.0)
            ferro_raw = st.number_input("Ferro (mg)", min_value=0.0)

            if st.form_submit_button("💾 Salvar e Converter para 100g"):
                fator = 100 / peso_referencia

                novo_item = pd.DataFrame(
                    [
                        {
                            "alimento": nome,
                            "kcal": kcal_raw * fator,
                            "prot": prot_raw * fator,
                            "gord": lip_raw * fator,
                            "carb": carb_raw * fator,
                            "fibra": fibra_raw * fator,
                            "colesterol": col_raw * fator,
                            "sodio": sod_raw * fator,
                            "ferro": ferro_raw * fator,
                            "unidade_medida": u_nome if u_nome else None,
                            "peso_unidade": u_peso if u_peso > 0 else 0.0,
                        }
                    ]
                )

                df_custom = carregar_custom_foods()
                df_updated = pd.concat([df_custom, novo_item], ignore_index=True)
                salvar_custom_foods(df_updated)

                st.success(f"✅ {nome} salvo com sucesso!")
                st.rerun()

    if not df_custom.empty:
        st.subheader("Gerenciar itens existentes")

        edited_df = st.data_editor(
            df_custom, num_rows="dynamic", width="stretch", key="editor_custom_foods"
        )

        if st.button("💾 Salvar Alterações na Tabela"):
            salvar_custom_foods(edited_df)
            st.toast("Alterações salvas com sucesso!", icon="💾")
    else:
        st.info("Você ainda não possui alimentos cadastrados manualmente.")
