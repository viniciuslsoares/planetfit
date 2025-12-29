import streamlit as st
from src.services.nutri_calculos import calcular_tmb, calcular_get


def render_perfil():
    st.header("🎯 Definição de Perfil e Metas")

    niveis_atividade = {
        "Sedentário": {"desc": "Pouco ou nenhum exercício, trabalho de escritório."},
        "Levemente Ativo": {"desc": "Exercício leve (1-3 dias/semana)."},
        "Moderadamente Ativo": {"desc": "Exercício moderado (3-5 dias/semana)."},
        "Muito Ativo": {"desc": "Exercício pesado (6-7 dias/semana)."},
        "Extremamente Ativo": {"desc": "Trabalho físico intenso ou atleta."},
    }

    col_input1, col_input2 = st.columns(2)
    with col_input1:
        peso = st.number_input(
            "Peso (kg)", value=float(st.session_state.dieta["perfil"]["peso"]), step=0.1
        )
        altura = st.number_input(
            "Altura (cm)", value=int(st.session_state.dieta["perfil"]["altura"]), step=1
        )
    with col_input2:
        idade = st.number_input(
            "Idade", value=int(st.session_state.dieta["perfil"]["idade"]), step=1
        )
        sexo = st.selectbox(
            "Sexo Biológico",
            ["Masculino", "Feminino"],
            index=(0 if st.session_state.dieta["perfil"]["sexo"] == "Masculino" else 1),
        )

    col_atv, col_obj = st.columns(2)
    with col_atv:
        atividade = st.selectbox("Nível de Atividade", list(niveis_atividade.keys()))
    with col_obj:
        objetivo = st.selectbox(
            "Objetivo",
            ["Perda de Peso (Cutting)", "Manutenção", "Ganho de Massa (Bulking)"],
        )

    if st.button("🚀 Calcular Metas Diárias", use_container_width=True):
        tmb = calcular_tmb(peso, altura, idade, sexo)
        get = calcular_get(tmb, atividade)

        ajuste = -500 if "Perda" in objetivo else 300 if "Ganho" in objetivo else 0
        calorias_alvo = get + ajuste

        # Atualiza State
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
        st.session_state["calculo_realizado"] = {
            "tmb": tmb,
            "get": get,
            "alvo": calorias_alvo,
        }

    # Exibição dos Cards (HTML/CSS)
    if "calculo_realizado" in st.session_state:
        res = st.session_state["calculo_realizado"]
        st.divider()
        c1, c2, c3 = st.columns(3)

        cards = [
            (c1, "⚡ TMB", res["tmb"], "#ff4b4b"),
            (c2, "🏃 Gasto (GET)", res["get"], "#2e7d32"),
            (c3, "🎯 Calorias Alvo", res["alvo"], "#1a73e8"),
        ]

        for col, label, valor, cor in cards:
            with col:
                st.markdown(
                    f"""
                    <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid {cor}; height: 120px;">
                        <p style="margin:0; font-size:14px; color:#555;">{label}</p>
                        <h2 style="margin:0; color:{cor};">{valor:.0f} <span style="font-size:16px;">kcal</span></h2>
                    </div>""",
                    unsafe_allow_html=True,
                )
