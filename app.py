import os
import pandas as pd
import streamlit as st

from src.services.data_service import carregar_dados, baixar_taco, PATH_TACO
from src.services.nutri_calculos import calcular_tmb, calcular_get
from src.services.state_service import init_session_state


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
        st.header("🎯 Definição de Perfil e Metas")

        # Dicionário explicativo para ajudar na escolha da atividade
        niveis_atividade = {
            "Sedentário": {
                "fator": 1.2,
                "desc": "Pouco ou nenhum exercício, trabalho de escritório.",
            },
            "Levemente Ativo": {
                "fator": 1.375,
                "desc": "Exercício leve (1-3 dias por semana).",
            },
            "Moderadamente Ativo": {
                "fator": 1.55,
                "desc": "Exercício moderado (3-5 dias por semana).",
            },
            "Muito Ativo": {
                "fator": 1.725,
                "desc": "Exercício pesado (6-7 dias por semana).",
            },
            "Extremamente Ativo": {
                "fator": 1.9,
                "desc": "Trabalho físico intenso ou treino de atleta (2x por dia).",
            },
        }

        # Inputs do usuário
        col_input1, col_input2 = st.columns(2)

        with col_input1:
            peso = st.number_input(
                "Peso (kg)",
                value=float(st.session_state.dieta["perfil"]["peso"]),
                step=0.1,
            )
            altura = st.number_input(
                "Altura (cm)",
                value=int(st.session_state.dieta["perfil"]["altura"]),
                step=1,
            )

        with col_input2:
            idade = st.number_input(
                "Idade", value=int(st.session_state.dieta["perfil"]["idade"]), step=1
            )
            sexo = st.selectbox(
                "Sexo Biológico",
                ["Masculino", "Feminino"],
                index=(
                    0 if st.session_state.dieta["perfil"]["sexo"] == "Masculino" else 1
                ),
            )

        col_atv, col_obj = st.columns(2)
        with col_atv:
            atividade = st.selectbox(
                "Nível de Atividade",
                [
                    "Sedentário",
                    "Levemente Ativo",
                    "Moderadamente Ativo",
                    "Muito Ativo",
                    "Extremamente Ativo",
                ],
            )
        with col_obj:
            objetivo = st.selectbox(
                "Objetivo",
                ["Perda de Peso (Cutting)", "Manutenção", "Ganho de Massa (Bulking)"],
            )

        if st.button("🚀 Calcular Metas Diárias", use_container_width=True):
            # Lógica de cálculo
            tmb = calcular_tmb(peso, altura, idade, sexo)
            get = calcular_get(tmb, atividade)

            # Ajuste conforme objetivo
            ajuste = 0
            if "Perda" in objetivo:
                ajuste = -500
            elif "Ganho" in objetivo:
                ajuste = 300

            calorias_alvo = get + ajuste

            # Salvando no State
            st.session_state.dieta["perfil"].update(
                {
                    "peso": peso,
                    "altura": altura,
                    "idade": idade,
                    "sexo": sexo,
                    "atividade": atividade,
                }
            )
            st.session_state.dieta["macros_alvo"]["kcal"] = calorias_alvo

            # Marca que o cálculo foi feito nesta sessão
            st.session_state["calculo_realizado"] = {
                "tmb": tmb,
                "get": get,
                "alvo": calorias_alvo,
            }

        # Seleção de Atividade com ajuda visual
        st.subheader("🏃 Nível de Atividade")
        escolha_atividade = st.selectbox(
            "Como é sua rotina?",
            options=list(niveis_atividade.keys()),
            help="Escolha o que melhor descreve seu nível de movimentação semanal.",
        )

        if "calculo_realizado" in st.session_state:
            res = st.session_state["calculo_realizado"]
            st.divider()

            c1, c2, c3 = st.columns(3)

            # Container TMB
            with c1:
                st.markdown(
                    f"""
                    <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #ff4b4b; height: 120px;">
                        <p style="margin:0; font-size:14px; color:#555;">⚡ TMB</p>
                        <h2 style="margin:0; color:#ff4b4b;">{res['tmb']:.0f} <span style="font-size:16px;">kcal</span></h2>
                    </div>""",
                    unsafe_allow_html=True,
                )

            # Container GET
            with c2:
                st.markdown(
                    f"""
                    <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #2e7d32; height: 120px;">
                        <p style="margin:0; font-size:14px; color:#555;">🏃 Gasto (GET)</p>
                        <h2 style="margin:0; color:#2e7d32;">{res['get']:.0f} <span style="font-size:16px;">kcal</span></h2>
                    </div>""",
                    unsafe_allow_html=True,
                )

            # Container CALORIAS ALVO (Destaque)
            with c3:
                st.markdown(
                    f"""
                    <div style="background-color: #e8f0fe; padding: 20px; border-radius: 10px; border-left: 5px solid #1a73e8; height: 120px;">
                        <p style="margin:0; font-size:14px; color:#555;">🎯 Calorias Alvo</p>
                        <h2 style="margin:0; color:#1a73e8;">{res['alvo']:.0f} <span style="font-size:16px;">kcal</span></h2>
                    </div>""",
                    unsafe_allow_html=True,
                )

    with tab_biblioteca:
        st.header("Consulta de Alimentos")
        if df_taco is not None:
            st.subheader("📊 Prévia da Base de Dados")
            # Exibindo as 3 primeiras linhas como solicitado
            st.dataframe(df_taco.head(3), width="stretch")
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
