import os
import requests
import pandas as pd
import streamlit as st


URL_TACO = "https://raw.githubusercontent.com/machine-learning-mocha/taco/main/formatados/alimentos.csv"
DATA_DIR = "data"
PATH_TACO = os.path.join(DATA_DIR, "taco.csv")


def baixar_taco():
    """Baixa a tabela TACO e salva localmente."""
    try:
        response = requests.get(URL_TACO, timeout=15)
        response.raise_for_status()

        os.makedirs(DATA_DIR, exist_ok=True)

        with open(PATH_TACO, "wb") as f:
            f.write(response.content)

        st.cache_data.clear()
        st.toast("Tabela TACO atualizada com sucesso!", icon="✅")

    except requests.RequestException as e:
        st.error(f"❌ Erro ao baixar a tabela TACO: {e}")


@st.cache_data
def carregar_dados() -> pd.DataFrame | None:
    """Carrega os dados locais da tabela TACO."""
    if not os.path.exists(PATH_TACO):
        st.warning("⚠️ Arquivo da TACO não encontrado. Faça o download primeiro.")
        return None

    return pd.read_csv(
        PATH_TACO,
        sep=",",
        na_values=["NA"],
        encoding="utf-8"
    )
