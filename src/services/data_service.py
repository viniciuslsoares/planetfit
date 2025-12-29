import os
import requests
import pandas as pd
import streamlit as st


URL_TACO = "https://raw.githubusercontent.com/machine-learning-mocha/taco/main/formatados/alimentos.csv"
DATA_DIR = "data"
PATH_TACO = os.path.join(DATA_DIR, "taco.csv")
PATH_CUSTOM = "data/custom_foods.csv"


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


def limpar_tabela(df):
    """Aplica as regras de negócio para limpar a tabela TACO."""

    # 1. Mapeamento de colunas (De -> Para)
    colunas_foco = {
        "Descrição dos alimentos": "alimento",
        "Energia..kcal.": "kcal",
        "Proteína..g.": "prot",
        "Lipídeos..g.": "gord",
        "Carboidrato..g.": "carb",
        "Fibra.Alimentar..g.": "fibra",
        "Colesterol..mg.": "colesterol",
        "Sódio..mg.": "sodio",
        "Ferro..mg.": "ferro",
    }

    df = df[list(colunas_foco.keys())].copy()

    df = df.rename(columns=colunas_foco)

    df["alimento"] = (
        df["alimento"]
        .str.replace(",", " ", regex=False)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )

    for col in [
        "kcal",
        "prot",
        "gord",
        "carb",
        "fibra",
        "colesterol",
        "sodio",
        "ferro",
    ]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    return df


@st.cache_data
def carregar_dados() -> pd.DataFrame | None:
    """Lê, limpa e retorna os dados."""
    if not os.path.exists(PATH_TACO):
        st.warning("⚠️ Arquivo da TACO não encontrado. Faça o download primeiro.")
        return None
    else:
        df_bruto = pd.read_csv(PATH_TACO)
        df_limpo = limpar_tabela(df_bruto)
        return df_limpo


def carregar_custom_foods():
    if os.path.exists(PATH_CUSTOM):
        return pd.read_csv(PATH_CUSTOM)
    # Se não existir, retorna um DataFrame vazio com as colunas corretas
    return pd.DataFrame(columns=["alimento", "kcal", "prot", "lip", "carb", "fibra", "colesterol", "sodio", "ferro"])


def salvar_custom_foods(df):
    os.makedirs("data", exist_ok=True)
    df.to_csv(PATH_CUSTOM, index=False)