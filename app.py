import streamlit as st

# Importe aqui futuramente suas Views e Controllers
# from src.views.perfil_view import render_perfil
# from src.views.biblioteca_view import render_biblioteca

def main():
    st.set_page_config(page_title="NutriStream", layout="wide", page_icon="🥗")

    st.title("🥗 NutriStream")
    st.caption("Planejador de Dieta Inteligente - Base TACO")

    # Inicialização do Session State (O "C" do MVC)
    if 'dieta' not in st.session_state:
        st.session_state.dieta = {
            "objetivo": "Manutenção",
            "macros_alvo": {"kcal": 0, "prot": 0, "carb": 0, "fat": 0},
            "cardapio": []
        }

    # CRIAÇÃO DAS ABAS (As "páginas" do seu navegador)
    tab_metas, tab_biblioteca, tab_cardapio = st.tabs([
        "🎯 Perfil & Metas", 
        "🍎 Biblioteca TACO & Receitas", 
        "📝 Meu Cardápio"
    ])

    with tab_metas:
        st.header("Definição de Perfil e Macronutrientes")
        st.info("Aqui você calculará sua TMB e definirá seus alvos diários.")
        # Chamada da View: render_perfil()

    with tab_biblioteca:
        st.header("Consulta de Alimentos (Base TACO)")
        st.info("Importe alimentos da tabela oficial ou crie suas próprias receitas.")
        # Chamada da View: render_biblioteca()

    with tab_cardapio:
        st.header("Montagem do Cardápio Diário")
        st.info("Combine alimentos e acompanhe seus macros em tempo real.")
        # Chamada da View: render_cardapio()

if __name__ == "__main__":
    main()