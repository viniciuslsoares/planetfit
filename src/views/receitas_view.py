import streamlit as st
import pandas as pd
from src.services.data_service import carregar_custom_foods, salvar_receita


def render_receitas(df_taco):
    st.header("🍳 Criar Nova Receita")

    df_custom = carregar_custom_foods()
    df_base = pd.concat([df_taco, df_custom], ignore_index=True)

    if "ingredientes_receita" not in st.session_state:
        st.session_state.ingredientes_receita = []

    with st.expander("➕ Adicionar Ingrediente à Receita", expanded=True):
        busca_ing = st.text_input("Pesquisar ingrediente:")
        if busca_ing:
            matches = df_base[
                df_base["alimento"].str.contains(busca_ing, case=False, na=False)
            ]
            escolha = st.selectbox(
                "Selecione o alimento:", matches["alimento"].tolist()
            )

            col_q, col_btn = st.columns([3, 1])
            quantidade = col_q.number_input(
                "Quantidade (g)", min_value=1.0, value=100.0
            )

            if col_btn.button("Adicionar"):
                alimento_dados = df_base[df_base["alimento"] == escolha].iloc[0]
                # Cálculo proporcional à quantidade digitada
                fator = quantidade / 100
                item = {
                    "nome": escolha,
                    "peso": quantidade,
                    "kcal": alimento_dados["kcal"] * fator,
                    "prot": alimento_dados["prot"] * fator,
                    "gord": alimento_dados["gord"] * fator,
                    "carb": alimento_dados["carb"] * fator,
                    "fibra": alimento_dados.get("fibra", 0) * fator,
                }
                st.session_state.ingredientes_receita.append(item)

    # 3. Listagem e Resumo
    if st.session_state.ingredientes_receita:
        st.subheader("Ingredientes da Receita")
        df_temp = pd.DataFrame(st.session_state.ingredientes_receita)
        st.table(df_temp[["nome", "peso", "kcal", "prot", "carb", "gord"]])

        if st.button("Limpar Receita"):
            st.session_state.ingredientes_receita = []
            st.rerun()

        # 4. Finalização e Normalização para 100g
        st.divider()
        nome_receita = st.text_input("Nome da Receita (ex: Meu Shake Hipercalórico)")

        if st.button("💾 Finalizar e Salvar Receita"):
            peso_total = df_temp["peso"].sum()
            fator_norm = 100 / peso_total

            nova_rec = pd.DataFrame(
                [
                    {
                        "alimento": f"REC: {nome_receita}",
                        "kcal": df_temp["kcal"].sum() * fator_norm,
                        "prot": df_temp["prot"].sum() * fator_norm,
                        "gord": df_temp["gord"].sum() * fator_norm,
                        "carb": df_temp["carb"].sum() * fator_norm,
                        "fibra": df_temp["fibra"].sum() * fator_norm,
                        "fonte": "Receita",
                    }
                ]
            )

            salvar_receita(nova_rec)
            st.success(f"Receita '{nome_receita}' salva e disponível na busca!")
            st.session_state.ingredientes_receita = []
            st.rerun()
