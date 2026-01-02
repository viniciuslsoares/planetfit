import streamlit as st
import pandas as pd
from src.controllers.cardapio_controller import CardapioController
from src.services.data_service import carregar_dados, carregar_custom_foods, carregar_receitas

def render_cardapio():
    st.header("📝 Planejador de Refeições Inteligente")
    
    # Verificação de Segurança: Usuário Ativo
    if not st.session_state.get('usuario_ativo'):
        st.warning("⚠️ Selecione um usuário na lateral para acessar seu planejamento.")
        return

    # 1. Configuração de Distribuição do Dia
    st.subheader("⚙️ Configuração do Dia")
    col_config1, col_config2 = st.columns([1, 2])
    
    with col_config1:
        n_refeicoes = st.number_input(
            "Número de refeições:", 
            min_value=1, max_value=8, 
            value=st.session_state.dieta.get('config_refeicoes', 4),
            help="O sistema dividirá as calorias totais entre essas refeições."
        )
        st.session_state.dieta['config_refeicoes'] = n_refeicoes
    
    with col_config2:
        st.info("💡 **Regra de Distribuição:** 20% no Café da Manhã e o restante dividido igualmente entre as demais refeições.")

    # 2. Preparação dos Dados
    meta_cafe, meta_outras = CardapioController.obter_metas_por_refeicao()
    
    df_taco = carregar_dados()
    df_custom = carregar_custom_foods()
    df_rec = carregar_receitas()
    # Consolidação da Biblioteca Global
    df_total = pd.concat([df_taco, df_custom, df_rec], ignore_index=True)

    st.divider()

    # 3. Renderização das Refeições
    for i in range(n_refeicoes):
        nome_ref = "☕ Café da Manhã" if i == 0 else f"🍽️ Refeição {i+1}"
        meta_atual = meta_cafe if i == 0 else meta_outras
        
        with st.expander(f"{nome_ref} - Meta: {meta_atual['kcal']:.0f} kcal", expanded=(i==0)):
            st.write(f"🎯 **Metas da Refeição:** {meta_atual['prot']:.1f}g Proteína | {meta_atual['carb']:.1f}g Carboidrato")
            
            st.divider()
            st.caption("🪄 Assistente de Otimização (Prático & Realista)")
            
            # Seleção de Alimentos
            c1, c2, c3 = st.columns(3)
            p_sel = c1.selectbox("🥩 Proteína", df_total['alimento'], key=f"p_sel_{i}")
            c_sel = c2.selectbox("🍚 Carboidrato", df_total['alimento'], key=f"c_sel_{i}")
            v_sel = c3.selectbox("🥦 Vegetal/Volume", df_total['alimento'], key=f"v_sel_{i}")

            if st.button(f"Gerar Sugestão Prática para {nome_ref}", key=f"btn_calc_{i}"):
                # Localizar dados nutricionais dos alimentos selecionados
                p_data = df_total[df_total['alimento'] == p_sel].iloc[0]
                c_data = df_total[df_total['alimento'] == c_sel].iloc[0]
                v_data = df_total[df_total['alimento'] == v_sel].iloc[0]

                # Chamar a nova lógica hierárquica do Controller
                resultado = CardapioController.gerar_sugestao_hierarquica(
                    meta_atual, p_data, c_data, v_data
                )

                if resultado:
                    gp, gc, gv, totais = resultado
                    
                    # --- Exibição das Porções ---
                    st.success(f"✅ Sugestão equilibrada para {nome_ref}:")
                    r1, r2, r3 = st.columns(3)
                    r1.metric(f"{p_sel}", f"{gp:.0f}g")
                    r2.metric(f"{c_sel}", f"{gc:.0f}g")
                    r3.metric(f"{v_sel}", f"{gv:.0f}g", help="Volume ajustado para saciedade.")

                    # --- Rodapé com Soma Exata ---
                    st.divider()
                    st.markdown("##### 📊 Balanço Nutricional Real")
                    st.caption("Valores finais após arredondamento das porções para medidas práticas:")
                    
                    f1, f2, f3, f4 = st.columns(4)
                    f1.write(f"🔥 **{totais['kcal']:.0f}** kcal")
                    f2.write(f"🥩 **{totais['prot']:.1f}g** P")
                    f3.write(f"🍚 **{totais['carb']:.1f}g** C")
                    f4.write(f"🥑 **{totais['fat']:.1f}g** G")
                    
                    # Cálculo de Variância
                    diff_kcal = totais['kcal'] - meta_atual['kcal']
                    cor_diff = "green" if abs(diff_kcal) < 50 else "orange"
                    st.markdown(f":{cor_diff}[*Variação de {diff_kcal:+.0f} kcal em relação à meta teórica.*]")

                else:
                    st.error("⚠️ Não foi possível encontrar um ajuste prático. Tente trocar os alimentos selecionados.")