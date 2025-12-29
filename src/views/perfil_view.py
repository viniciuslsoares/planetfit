import streamlit as st
from src.services.nutri_calculos import (
    calcular_tmb,
    calcular_get,
    calcular_macros_por_gkg,
)


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
    lista_atividades = list(niveis_atividade.keys())
    try:
        index_atv = lista_atividades.index(
            st.session_state.dieta["perfil"]["atividade"]
        )
    except ValueError:
        index_atv = 2

    with col_atv:
        atividade = st.selectbox(
            "Nível de Atividade", options=lista_atividades, index=index_atv
        )

    dict_objetivos = {
        "Cutting Forte": -500,
        "Cutting Leve": -350,
        "Manutenção": 0,
        "Bulking Limpo": 350,
        "Bulking Sujo": 500,
    }
    lista_objetivos = list(dict_objetivos.keys())

    objetivo_salvo = st.session_state.dieta["perfil"].get("objetivo", "Manutenção")
    try:
        index_obj = lista_objetivos.index(objetivo_salvo)
    except ValueError:
        index_obj = 2

    with col_obj:
        objetivo = st.selectbox("Objetivo", options=lista_objetivos, index=index_obj)

    if st.button("🚀 Calcular Metas Diárias", width="stretch"):
        tmb = calcular_tmb(peso, altura, idade, sexo)
        get = calcular_get(tmb, atividade)

        ajuste = dict_objetivos.get(objetivo, 0)
        calorias_alvo = get + ajuste

        st.session_state.dieta["perfil"].update(
            {
                "peso": peso,
                "altura": altura,
                "idade": idade,
                "sexo": sexo,
                "atividade": atividade,
                "objetivo": objetivo,
            }
        )

        st.session_state.dieta["macros_alvo"]["kcal"] = calorias_alvo

        st.session_state["calculo_realizado"] = {
            "tmb": tmb,
            "get": get,
            "alvo": calorias_alvo,
        }

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

    if "calculo_realizado" in st.session_state:
        res = st.session_state["calculo_realizado"]
        peso_atual = st.session_state.dieta["perfil"]["peso"]

        st.subheader("🥪 Ajuste de Macronutrientes")
        st.info(
            "Defina a quantidade de Proteína e Gordura por quilo. O Carboidrato preencherá o restante das calorias."
        )

        col_p, col_g = st.columns(2)
        with col_p:
            g_kg_prot = st.slider("Proteína (g/kg)", 1.0, 3.0, 2.0, 0.1)
        with col_g:
            g_kg_fat = st.slider("Gordura (g/kg)", 0.5, 1.5, 1.0, 0.1)

        # Cálculo em tempo real
        macros = calcular_macros_por_gkg(peso_atual, res["alvo"], g_kg_prot, g_kg_fat)

        # Exibição dos Macros
        st.divider()
        m1, m2, m3 = st.columns(3)
        m1.metric(
            "Proteína",
            f"{macros['proteina']['g']:.0f}g",
            f"{macros['proteina']['kcal']:.0f} kcal",
        )
        m2.metric(
            "Gordura",
            f"{macros['gordura']['g']:.0f}g",
            f"{macros['gordura']['kcal']:.0f} kcal",
        )
        m3.metric(
            "Carboidrato",
            f"{macros['carboidrato']['g']:.0f}g",
            f"{macros['carboidrato']['kcal']:.0f} kcal",
        )

        # Salva no estado para o cardápio usar
        st.session_state.dieta["macros_alvo"].update(
            {
                "prot": macros["proteina"]["g"],
                "fat": macros["gordura"]["g"],
                "carb": macros["carboidrato"]["g"],
            }
        )
