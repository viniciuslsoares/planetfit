import streamlit as st
import pandas as pd
from src.services.data_service import baixar_taco, carregar_custom_foods, salvar_custom_foods


def render_biblioteca(df_taco):
    
    col_titulo, col_btn = st.columns([0.9, 0.1])
    
    with col_titulo:
        st.header("🍎 Biblioteca TACO & Receitas")
        
    with col_btn:
        if st.button("⚙️", help="Atualizar Base de Dados"):
            st.session_state.show_config = not st.session_state.get('show_config', False)

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


    else:
        st.error("Base de dados não carregada.")
    
    st.divider()
    
    
    st.header("➕ Meus Alimentos Customizados")
    
    df_custom = carregar_custom_foods()

    with st.expander("➕ Cadastrar Novo Alimento"):
        with st.form("form_novo_alimento", clear_on_submit=True):
            nome = st.text_input("Nome do Alimento", placeholder="Ex: Whey Protein Morango")
            
            peso_referencia = st.number_input("Peso da porção no rótulo (g)", min_value=1.0, value=100.0, help="Qual o peso que os macros abaixo representam?")
            
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
                # Lógica de Normalização para 100g
                fator = 100 / peso_referencia
                
                novo_item = pd.DataFrame([{
                    "alimento": nome,
                    "kcal": kcal_raw * fator,
                    "prot": prot_raw * fator,
                    "gord": lip_raw * fator,
                    "carb": carb_raw * fator,
                    "fibra": fibra_raw * fator,
                    "colesterol": col_raw * fator,
                    "sodio": sod_raw * fator,
                    "ferro": ferro_raw * fator
                }])
                
                df_custom = carregar_custom_foods()
                df_updated = pd.concat([df_custom, novo_item], ignore_index=True)
                salvar_custom_foods(df_updated)
                
                st.success(f"✅ {nome} salvo com sucesso!")
                st.rerun()

    if not df_custom.empty:
        st.subheader("Gerenciar itens existentes")
        
        edited_df = st.data_editor(
            df_custom, 
            num_rows="dynamic", 
            use_container_width=True,
            key="editor_custom_foods"
        )
        
        if st.button("💾 Salvar Alterações na Tabela"):
            salvar_custom_foods(edited_df)
            st.toast("Alterações salvas com sucesso!", icon="💾")
    else:
        st.info("Você ainda não possui alimentos cadastrados manualmente.")