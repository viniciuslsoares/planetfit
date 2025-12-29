import streamlit as st


def render_cardapio():
    st.header("📝 Meu Cardápio Diário")

    macros = st.session_state.dieta.get("macros_alvo", {})
    kcal_alvo = macros.get("kcal", 0)

    if kcal_alvo == 0:
        st.warning(
            "⚠️ Você ainda não definiu suas metas. Vá na aba 'Perfil & Metas' primeiro!"
        )
    else:
        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("Refeições")
            st.info(
                "Funcionalidade em desenvolvimento: Em breve você poderá adicionar alimentos aqui."
            )

        with col2:
            st.subheader("Resumo do Dia")
            st.metric("Calorias Restantes", f"{kcal_alvo:.0f} kcal")
            st.progress(0, text="Progresso da meta: 0%")
