import streamlit as st
import numpy as np
from src.controllers.user_controller import UserController

class CardapioController:
    @staticmethod
    def obter_metas_por_refeicao():
        """Divide as metas do dia: 20% Café da Manhã, o resto dividido entre as N refeições."""
        macros_alvo = st.session_state.dieta['macros_alvo']
        n_refeicoes = st.session_state.dieta.get('config_refeicoes', 4)
        
        # Café da Manhã (20%)
        meta_cafe = {k: v * 0.2 for k, v in macros_alvo.items()}
        
        # Outras (80% / N-1)
        fator_resto = 0.8 / (n_refeicoes - 1) if n_refeicoes > 1 else 0.8
        meta_outras = {k: v * fator_resto for k, v in macros_alvo.items()}
        
        return meta_cafe, meta_outras

    @staticmethod
    def solver_porcoes_pl(meta, p_data, c_data, v_data):
        """
        Resolve o Problema da Dieta via Programação Linear (Ax = B)
        A = Matriz de nutrientes (kcal, prot, carb) por 1g de alimento
        B = Vetor de metas da refeição
        """
        # Montamos a matriz A com valores por 1g (valor_taco / 100)
        A = np.array([
            [p_data['kcal']/100, c_data['kcal']/100, v_data['kcal']/100], # Kcal
            [p_data['prot']/100, c_data['prot']/100, v_data['prot']/100], # Prot
            [p_data['carb']/100, c_data['carb']/100, v_data['carb']/100]  # Carb
        ])

        # Metas desejadas para a refeição
        B = np.array([meta['kcal'], meta['prot'], meta['carb']])

        try:
            # Resolve o sistema linear
            x = np.linalg.solve(A, B)
            # Retorna as gramas, garantindo que não sejam negativas (clipping)
            return np.maximum(x, 0)
        except np.linalg.LinAlgError:
            return None
        
    def otimizar_porcoes_realistas(meta, p_data, c_data, v_data):
        """
        Trava P e C em múltiplos de 50g (100, 150, 200) e 
        ajusta o volume através dos legumes.
        """
        opcoes_peso = [100.0, 125.0, 150.0, 175.0, 200.0, 225.0, 250.0, 275.0, 300.0]
        melhor_combinacao = None
        menor_erro = float('inf')

        for g_p in opcoes_peso:
            for g_c in opcoes_peso:
                kcal_base = (p_data['kcal'] * g_p / 100) + (c_data['kcal'] * g_c / 100)
                prot_base = (p_data['prot'] * g_p / 100) + (c_data['prot'] * g_c / 100)
                
                kcal_faltante = meta['kcal'] - kcal_base
                
                if v_data['kcal'] > 0:
                    g_v = (kcal_faltante / v_data['kcal']) * 100
                else:
                    g_v = 100.0 # Default se o vegetal for quase zero caloria
                
                g_v = max(g_v, 100.0)

                prot_total = prot_base + (v_data['prot'] * g_v / 100)
                erro = abs(prot_total - meta['prot'])

                if erro < menor_erro:
                    menor_erro = erro
                    melhor_combinacao = (g_p, g_c, round(g_v, 0))

        return melhor_combinacao
    
    @staticmethod
    def gerar_sugestao_hierarquica(meta, p_data, c_data, v_data):
        # 1. Âncora de Proteína (múltiplos de 50g)
        g_p_ideal = (meta['prot'] / (p_data['prot'] / 100))
        g_p = max(100.0, round(g_p_ideal / 25) * 25)
        
        # 2. Vegetal Base (ajustado para ser volumoso)
        g_v_base = 200.0
        
        # 3. Ajuste de Carboidrato para fechar calorias
        kcal_atual = (p_data['kcal'] * g_p / 100) + (v_data['kcal'] * g_v_base / 100)
        kcal_restante = meta['kcal'] - kcal_atual
        
        if c_data['kcal'] > 0:
            g_c_ideal = (kcal_restante / (c_data['kcal'] / 100))
            g_c = max(0.0, round(g_c_ideal / 50) * 50)
        else:
            g_c = 0.0

        # 4. Ajuste fino de volume no vegetal (mín 150g, máx 500g)
        kcal_final_sem_v = (p_data['kcal'] * g_p / 100) + (c_data['kcal'] * g_c / 100)
        kcal_para_v = meta['kcal'] - kcal_final_sem_v
        g_v = max(150.0, min((kcal_para_v / (v_data['kcal'] / 100)) * 100 if v_data['kcal'] > 0 else 200, 500.0))

        totais = {
            "kcal": (p_data['kcal']*g_p/100) + (c_data['kcal']*g_c/100) + (v_data['kcal']*g_v/100),
            "prot": (p_data['prot']*g_p/100) + (c_data['prot']*g_c/100) + (v_data['prot']*g_v/100),
            "carb": (p_data['carb']*g_p/100) + (c_data['carb']*g_c/100) + (v_data['carb']*g_v/100),
            "fat": (p_data['gord']*g_p/100) + (c_data['gord']*g_c/100) + (v_data['gord']*g_v/100)
        }

        return g_p, g_c, round(g_v, 0), totais