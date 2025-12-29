def calcular_tmb(peso, altura, idade, sexo):
    """
    Calcula a Taxa Metabólica Basal usando Harris-Benedict.
    Altura em cm, Peso em kg.
    """
    if sexo == "Masculino":
        return 66.5 + (13.75 * peso) + (5.003 * altura) - (6.75 * idade)
    else:
        return 655.1 + (9.563 * peso) + (1.85 * altura) - (4.676 * idade)


def calcular_get(tmb, nivel_atividade):
    """
    Calcula o Gasto Energético Total baseado no nível de atividade.
    """
    fatores = {
        "Sedentário": 1.2,
        "Levemente Ativo": 1.375,
        "Moderadamente Ativo": 1.55,
        "Muito Ativo": 1.725,
        "Extremamente Ativo": 1.9,
    }
    return tmb * fatores.get(nivel_atividade, 1.2)


def calcular_macros_por_gkg(peso, kcal_alvo, g_kg_prot, g_kg_fat):
    g_prot = peso * g_kg_prot
    g_fat = peso * g_kg_fat

    kcal_prot = g_prot * 4
    kcal_fat = g_fat * 9

    kcal_carb = kcal_alvo - (kcal_prot + kcal_fat)

    g_carb = max(0, kcal_carb / 4)

    return {
        "proteina": {"g": g_prot, "kcal": kcal_prot},
        "gordura": {"g": g_fat, "kcal": kcal_fat},
        "carboidrato": {"g": g_carb, "kcal": max(0, kcal_carb)},
    }
