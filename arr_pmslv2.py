# arr_pmslv2.py

from datetime import datetime
import pandas as pd
import requests
import streamlit as st
import plotly.express as px
import plotly.io as pio
import numpy as np


# ---------------------------
# Config / Constants
# ---------------------------
URL_TRANSPARENCIA = "https://grp.saoleopoldo.rs.gov.br/infra/apigw/transparencia/service/contabilidade/transparencia/receita/receitaArrecadada/"
pio.templates.default = "plotly"

# ---------------------------
# Mapeamento PCASP
# ---------------------------
MAPEAMENTO_ANUAL = {
    "IPTU - Dívida Ativa": {
        2024: {"principais": ["1.1.1.2.50.0.3.00.00.00"], "deducoes": ["9.1.1.1.2.50.0.3.00.00.00"]},
        2025: {"principais": ["1.1.1.2.50.0.3.00.00.00"], "deducoes": ["9.1.1.1.2.50.0.3.00.00.00"]},
        2026: {"principais": ["1.1.1.2.50.0.3.00.00.00"], "deducoes": ["9.1.1.1.2.50.0.3.00.00.00"]},
    },
    "IPTU - Principal": {
        2024: {"principais": ["1.1.1.2.50.0.1.00.00.00"], "deducoes": ["9.1.1.1.2.50.0.1.00.00.00"]},
        2025: {"principais": ["1.1.1.2.50.0.1.00.00.00"], "deducoes": ["9.1.1.1.2.50.0.1.00.00.00"]},
        2026: {"principais": ["1.1.1.2.50.0.1.00.00.00"], "deducoes": ["9.1.1.1.2.50.0.1.00.00.00"]},
    },
    "ISS - Dívida Ativa": {
        2024: {"principais": ["1.1.1.4.51.1.3.00.00.00"], "deducoes": ["9.1.1.1.4.51.1.3.00.00.00"]},
        2025: {"principais": ["1.1.1.4.51.1.3.00.00.00"], "deducoes": ["9.1.1.1.4.51.1.3.00.00.00"]},
        2026: {"principais": ["1.1.1.4.51.1.3.00.00.00"], "deducoes": ["9.1.1.1.4.51.1.3.00.00.00"]},
    },
    "ISS - Principal": {
        2024: {"principais": ["1.1.1.4.51.1.1.00.00.00"], "deducoes": ["9.1.1.1.4.51.1.1.00.00.00"]},
        2025: {"principais": ["1.1.1.4.51.1.1.00.00.00"], "deducoes": ["9.1.1.1.4.51.1.1.00.00.00"]},
        2026: {"principais": ["1.1.1.4.51.1.1.00.00.00"], "deducoes": ["9.1.1.1.4.51.1.1.00.00.00"]},
    },
    "ITBI - Dívida Ativa": {
        2024: {"principais": ["1.1.1.2.53.0.3.00.00.00"], "deducoes": ["9.1.1.1.2.53.0.3.00.00.00"]},
        2025: {"principais": ["1.1.1.2.53.0.3.00.00.00"], "deducoes": ["9.1.1.1.2.53.0.3.00.00.00"]},
        2026: {"principais": ["1.1.1.2.53.0.3.00.00.00"], "deducoes": ["9.1.1.1.2.53.0.3.00.00.00"]},
    },
    "ITBI - Principal": {
        2024: {"principais": ["1.1.1.2.53.0.1.00.00.00"], "deducoes": ["9.1.1.1.2.53.0.1.00.00.00"]},
        2025: {"principais": ["1.1.1.2.53.0.1.00.00.00"], "deducoes": ["9.1.1.1.2.53.0.1.00.00.00"]},
        2026: {"principais": ["1.1.1.2.53.0.1.00.00.00"], "deducoes": ["9.1.1.1.2.53.0.1.00.00.00"]},
    },
    "TACL - Dívida Ativa": {
        2024: {"principais": ["1.1.2.2.53.0.3.00.00.00"], "deducoes": ["9.1.1.2.2.53.0.3.00.00.00"]},
        2025: {"principais": ["1.1.2.2.53.0.3.00.00.00"], "deducoes": ["9.1.1.2.2.53.0.3.00.00.00"]},
        2026: {"principais": ["1.1.2.2.53.0.3.00.00.00"], "deducoes": ["9.1.1.2.2.53.0.3.00.00.00"]},
    },
    "TACL - Principal": {
        2024: {"principais": ["1.1.2.2.53.0.1.00.00.00"], "deducoes": ["9.1.1.2.2.01.0.1.00.00.00"]},
        2025: {"principais": ["1.1.2.2.53.0.1.00.00.00"], "deducoes": ["9.1.1.2.2.53.0.1.00.00.00"]},
        2026: {"principais": ["1.1.2.2.53.0.1.00.00.00"], "deducoes": ["9.1.1.2.2.53.0.1.00.00.00"]},
    },
    "ICMS": {
        2024: {"principais": ["1.7.2.1.50.0.0.00.00.00"], "deducoes": ["9.1.7.2.1.50.0.0.00.00.00"]},
        2025: {"principais": ["1.7.2.1.50.0.0.00.00.00"], "deducoes": ["9.1.7.2.1.50.0.0.00.00.00"]},
        2026: {"principais": ["1.7.2.1.50.0.0.00.00.00"], "deducoes": ["9.1.7.2.1.50.0.0.00.00.00"]},
    },
    "IPVA": {
        2024: {"principais": ["1.7.2.1.51.0.0.00.00.00"], "deducoes": ["9.1.7.2.1.51.0.0.00.00.00"]},
        2025: {"principais": ["1.7.2.1.51.0.0.00.00.00"], "deducoes": ["9.1.7.2.1.51.0.0.00.00.00"]},
        2026: {"principais": ["1.7.2.1.51.0.0.00.00.00"], "deducoes": ["9.1.7.2.1.51.0.0.00.00.00"]},
    },
    "FPM": {
        2024: {"principais": ["1.7.1.1.51.0.0.00.00.00"], "deducoes": ["9.1.7.1.1.51.0.0.00.00.00"]},
        2025: {"principais": ["1.7.1.1.51.0.0.00.00.00"], "deducoes": ["9.1.7.1.1.51.0.0.00.00.00"]},
        2026: {"principais": ["1.7.1.1.51.0.0.00.00.00"], "deducoes": ["9.1.7.1.1.51.0.0.00.00.00"]},
    },
    "Receitas Correntes": {
        2024: {"principais": ["1.0.0.0.00.0.0.00.00.00"], "deducoes": ["9.1.0.0.0.00.0.0.00.00.00"]},
        2025: {"principais": ["1.0.0.0.00.0.0.00.00.00"], "deducoes": ["9.1.0.0.0.00.0.0.00.00.00"]},
        2026: {"principais": ["1.0.0.0.00.0.0.00.00.00"], "deducoes": ["9.1.0.0.0.00.0.0.00.00.00"]},
    },
    "Impostos, Taxas e Contribuições de Melhoria": {
        2024: {"principais": ["1.1.0.0.00.0.0.00.00.00"], "deducoes": ["9.1.1.0.0.00.0.0.00.00.00"]},
        2025: {"principais": ["1.1.0.0.00.0.0.00.00.00"], "deducoes": ["9.1.1.0.0.00.0.0.00.00.00"]},
        2026: {"principais": ["1.1.0.0.00.0.0.00.00.00"], "deducoes": ["9.1.1.0.0.00.0.0.00.00.00"]},
    },
    "Transferências Correntes": {
        2024: {"principais": ["1.7.0.0.00.0.0.00.00.00"], "deducoes": ["9.1.7.0.0.00.0.0.00.00.00"]},
        2025: {"principais": ["1.7.0.0.00.0.0.00.00.00"], "deducoes": ["9.1.7.0.0.00.0.0.00.00.00"]},
        2026: {"principais": ["1.7.0.0.00.0.0.00.00.00"], "deducoes": ["9.1.7.0.0.00.0.0.00.00.00"]},
    },
}


COLUNAS_SERIES = [
    "IPTU",
    "ITBI",
    "ISS",
    "TACL",
    "D.A. IPTU",
    "D.A. ITBI",
    "D.A. ISS",
    "D.A. TACL",
    "ICMS",
    "IPVA",
    "FPM",
    "RECEITAS CORRENTES",
    "IMPOSTOS, TAXAS E CONTRIBUIÇÕES DE MELHORIA",
    "TRANSFERÊNCIAS CORRENTES",
]

MESES_PT = {
    1: "Jan", 2: "Fev", 3: "Mar", 4: "Abr", 5: "Mai", 6: "Jun",
    7: "Jul", 8: "Ago", 9: "Set", 10: "Out", 11: "Nov", 12: "Dez"
}

# ---------------------------
# Funções Auxiliares
# ---------------------------

def obter_valor_acumulado_ate_competencia(df: pd.DataFrame, competencia: pd.Timestamp, coluna: str) -> float:
    ano = competencia.year
    mes = competencia.month

    mask = (
        (df["Competência"].dt.year == ano) &
        (df["Competência"].dt.month <= mes)
    )

    if coluna not in df.columns:
        return 0.0

    return float(df.loc[mask, coluna].sum())

def gerar_insights_analise(df_analise: pd.DataFrame, df_corrigido: pd.DataFrame, contexto: dict):
    insights = []

    atual = contexto["atual"]
    anterior = contexto["anterior"]
    ano_anterior = contexto["ano_anterior"]

    rot_atual = contexto["rot_atual"]
    rot_anterior = contexto["rot_anterior"]
    rot_ano_anterior = contexto["rot_ano_anterior"]

    rot_acum_atual = contexto.get("rot_acum_atual")
    rot_acum_ano_ant = contexto.get("rot_acum_ano_ant")
    rot_var_acum = contexto.get("rot_var_acum")

    col_nom_mensal = f"∆% Nominal {rot_atual}/{rot_anterior}"
    col_nom_anual = f"∆% Nominal {rot_atual}/{rot_ano_anterior}"
    col_real_mensal = f"∆% Real {rot_atual}/{rot_anterior}"
    col_real_anual = f"∆% Real {rot_atual}/{rot_ano_anterior}"

    # -------------------------
    # Receita própria x transferências
    # -------------------------
    base_pizza_atual = montar_base_pizzas(df_corrigido, contexto)[rot_atual]

    propria = float(
        base_pizza_atual.loc[
            base_pizza_atual["Grupo"] == "Receita Própria", "Valor"
        ].iloc[0]
    )
    transf = float(
        base_pizza_atual.loc[
            base_pizza_atual["Grupo"] == "Receita de Transferências", "Valor"
        ].iloc[0]
    )
    total_escopo = propria + transf

    if total_escopo > 0:
        perc_propria = propria / total_escopo
        perc_transf = transf / total_escopo

        insights.append(
            f"No período {rot_atual}, a receita própria representa {formatar_pct(perc_propria)} do total analisado."
        )
        insights.append(
            f"No período {rot_atual}, as transferências representam {formatar_pct(perc_transf)} do total analisado."
        )

        if perc_transf > 0.50:
            insights.append("Há elevada dependência de transferências intergovernamentais.")
        elif perc_transf > 0.40:
            insights.append("As transferências têm peso relevante na composição da arrecadação.")
        else:
            insights.append("A arrecadação analisada apresenta predominância relativa de receita própria.")

    # -------------------------
    # Receita corrente - mensal e anual
    # -------------------------
    linha_rc = df_analise[df_analise["Item"] == "Receita Corrente"]
    if not linha_rc.empty:
        linha_rc = linha_rc.iloc[0]

        if pd.notna(linha_rc.get(col_nom_mensal)):
            insights.append(
                f"A receita corrente variou {formatar_pct(linha_rc[col_nom_mensal])} nominalmente em relação a {rot_anterior}."
            )

        if pd.notna(linha_rc.get(col_real_mensal)):
            insights.append(
                f"A variação real da receita corrente em relação a {rot_anterior} foi de {formatar_pct(linha_rc[col_real_mensal])}."
            )

        if pd.notna(linha_rc.get(col_nom_anual)):
            insights.append(
                f"Em comparação com {rot_ano_anterior}, a receita corrente variou {formatar_pct(linha_rc[col_nom_anual])} nominalmente."
            )

        if pd.notna(linha_rc.get(col_real_anual)):
            insights.append(
                f"Em termos reais, a receita corrente variou {formatar_pct(linha_rc[col_real_anual])} frente a {rot_ano_anterior}."
            )

    # -------------------------
    # Maiores altas e quedas - escopo detalhado
    # -------------------------
    df_var = df_analise[
        (df_analise["Item"] != "Total")
        & (df_analise["Grupo"] != "Receitas")
    ].copy()

    if not df_var.empty and col_real_mensal in df_var.columns:
        df_var_valid = df_var.dropna(subset=[col_real_mensal]).copy()

        if not df_var_valid.empty:
            maior = df_var_valid.loc[df_var_valid[col_real_mensal].idxmax()]
            menor = df_var_valid.loc[df_var_valid[col_real_mensal].idxmin()]

            insights.append(
                f"O maior crescimento real mensal ocorreu em {rotulo_grupo_item(maior)} ({formatar_pct(maior[col_real_mensal])})."
            )
            insights.append(
                f"A maior retração real mensal ocorreu em {rotulo_grupo_item(menor)} ({formatar_pct(menor[col_real_mensal])})."
            )

    # -------------------------
    # Peso da dívida ativa
    # -------------------------
    colunas_da = ["D.A. IPTU", "D.A. ISS", "D.A. ITBI", "D.A. TACL"]
    colunas_prop = ["IPTU", "ISS", "ITBI", "TACL"]

    total_da = somar_competencia(df_corrigido, atual, colunas_da)
    total_prop_sem_da = somar_competencia(df_corrigido, atual, colunas_prop)
    total_prop_com_da = total_da + total_prop_sem_da

    if total_prop_com_da > 0:
        perc_da_total_prop = total_da / total_prop_com_da
        insights.append(
            f"A dívida ativa representa {formatar_pct(perc_da_total_prop)} do conjunto de receitas próprias analisadas."
        )

    if total_prop_sem_da > 0:
        perc_da_sobre_principal = total_da / total_prop_sem_da
        insights.append(
            f"Em relação às receitas próprias principais, a dívida ativa equivale a {formatar_pct(perc_da_sobre_principal)}."
        )

    # -------------------------
    # Alertas crescimento e retração
    # -------------------------
    grupos_alerta = [
        "Receitas Próprias",
        "Receitas Próprias Dívida Ativa",
        "Receitas de Transferências"
    ]

    df_alertas = df_analise[
        (df_analise["Grupo"].isin(grupos_alerta))
        & (df_analise["Item"] != "Total")
    ].copy()

    if not df_alertas.empty and col_real_mensal in df_alertas.columns:
        fortes_altas = df_alertas[df_alertas[col_real_mensal] > 0.10].sort_values(col_real_mensal, ascending=False)
        quedas_relevantes = df_alertas[df_alertas[col_real_mensal] < -0.05].sort_values(col_real_mensal)

        for _, row in fortes_altas.iterrows():
            insights.append(
                f"Alerta de crescimento: {rotulo_grupo_item(row)} apresentou alta real mensal de {formatar_pct(row[col_real_mensal])}."
            )

        for _, row in quedas_relevantes.iterrows():
            insights.append(
                f"Alerta de retração: {rotulo_grupo_item(row)} apresentou queda real mensal de {formatar_pct(row[col_real_mensal])}."
            )

    # -------------------------
    # Ranking das receitas do período
    # -------------------------
    df_rank = ranking_receitas_periodo(df_corrigido, atual)

    if not df_rank.empty:
        top3 = df_rank.head(3)
        ranking_txt = "; ".join(
            f"{row['Item']} ({formatar_num(row['Valor'])}, {formatar_pct(row['Participação'])})"
            for _, row in top3.iterrows()
        )
        insights.append(f"As três maiores rubricas do período {rot_atual} foram: {ranking_txt}.")

    # -------------------------
    # Concentração de arrecadação
    # -------------------------
    if not df_rank.empty:
        top1 = df_rank.iloc[0]
        top3_part = df_rank.head(3)["Participação"].sum()

        if top1["Participação"] > 0.40:
            insights.append(
                f"Há concentração relevante da arrecadação em {top1['Item']}, que responde por {formatar_pct(top1['Participação'])} do total analisado."
            )

        insights.append(
            f"As três maiores rubricas concentram {formatar_pct(top3_part)} do total analisado."
        )

    # -------------------------
    # Receita própria x transferências - comparação com mês anterior
    # -------------------------
    base_pizzas = montar_base_pizzas(df_corrigido, contexto)

    if rot_anterior in base_pizzas:
        base_ant = base_pizzas[rot_anterior]
        propria_ant = float(base_ant.loc[base_ant["Grupo"] == "Receita Própria", "Valor"].iloc[0])
        transf_ant = float(base_ant.loc[base_ant["Grupo"] == "Receita de Transferências", "Valor"].iloc[0])

        total_ant = propria_ant + transf_ant
        if total_escopo > 0 and total_ant > 0:
            perc_prop_ant = propria_ant / total_ant
            perc_transf_ant = transf_ant / total_ant

            delta_prop = (propria / total_escopo) - perc_prop_ant
            delta_transf = (transf / total_escopo) - perc_transf_ant

            insights.append(
                f"A participação da receita própria mudou {formatar_pct(delta_prop)} em relação a {rot_anterior}."
            )
            insights.append(
                f"A participação das transferências mudou {formatar_pct(delta_transf)} em relação a {rot_anterior}."
            )

    # -------------------------
    # INSIGHTS DE ACUMULADO
    # -------------------------
    linha_rc_acum = df_analise[df_analise["Item"] == "Receita Corrente"]

    if (
        not linha_rc_acum.empty
        and rot_var_acum is not None
        and rot_var_acum in linha_rc_acum.columns
    ):
        linha_rc_acum = linha_rc_acum.iloc[0]

        if pd.notna(linha_rc_acum[rot_var_acum]):
            insights.append(
                f"No acumulado até {rot_atual}, a receita corrente apresenta variação de {formatar_pct(linha_rc_acum[rot_var_acum])} em relação ao mesmo período do exercício anterior."
            )

    # -------------------------
    # Maior contribuição e maior pressão no acumulado
    # -------------------------
    df_acum = df_analise[
        (df_analise["Item"] != "Total") &
        (df_analise["Grupo"] != "Receitas")
    ].copy()

    if (
        rot_acum_atual is not None
        and rot_acum_ano_ant is not None
        and rot_acum_atual in df_acum.columns
        and rot_acum_ano_ant in df_acum.columns
    ):
        df_acum["Delta"] = df_acum[rot_acum_atual] - df_acum[rot_acum_ano_ant]
        df_acum_valid = df_acum.dropna(subset=["Delta"]).copy()

        if not df_acum_valid.empty:
            maior_pos = df_acum_valid.loc[df_acum_valid["Delta"].idxmax()]
            maior_neg = df_acum_valid.loc[df_acum_valid["Delta"].idxmin()]

            insights.append(
                f"O principal fator de crescimento acumulado foi {rotulo_grupo_item(maior_pos)}."
            )

            if maior_neg["Delta"] < 0:
                insights.append(
                    f"A maior pressão negativa no acumulado decorre de {rotulo_grupo_item(maior_neg)}."
                )

    # Remover duplicidades preservando ordem
    insights_unicos = list(dict.fromkeys(insights))
    return insights_unicos, df_rank

def rotulo_grupo_item(row) -> str:
    return f"{row['Grupo']} > {row['Item']}"

def somar_competencia(df: pd.DataFrame, competencia: pd.Timestamp, colunas: list[str]) -> float:
    return sum(obter_valor_competencia(df, competencia, c) for c in colunas)

def formatar_pct(valor) -> str:
    if pd.isna(valor):
        return "-"
    return f"{valor:.2%}".replace(".", ",")

def formatar_num(valor) -> str:
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def ranking_receitas_periodo(df_corrigido: pd.DataFrame, competencia: pd.Timestamp) -> pd.DataFrame:
    colunas_ranking = [
        "IPTU", "ISS", "ITBI", "TACL",
        "D.A. IPTU", "D.A. ISS", "D.A. ITBI", "D.A. TACL",
        "IPVA", "FPM", "ICMS"
    ]

    dados = []
    for col in colunas_ranking:
        val = obter_valor_competencia(df_corrigido, competencia, col)
        dados.append({"Item": col, "Valor": val})

    df_rank = pd.DataFrame(dados).sort_values("Valor", ascending=False).reset_index(drop=True)
    total = df_rank["Valor"].sum()
    df_rank["Participação"] = df_rank["Valor"] / total if total > 0 else 0.0
    return df_rank

def rotulo_competencia(ts: pd.Timestamp) -> str:
    meses = {
        1: "Jan", 2: "Fev", 3: "Mar", 4: "Abr", 5: "Mai", 6: "Jun",
        7: "Jul", 8: "Ago", 9: "Set", 10: "Out", 11: "Nov", 12: "Dez"
    }
    return f"{meses[ts.month]}/{str(ts.year)[-2:]}"

def obter_valor_competencia(df: pd.DataFrame, competencia: pd.Timestamp, coluna: str) -> float:
    linha = df.loc[df["Competência"] == competencia, coluna]
    if linha.empty:
        return 0.0
    valor = linha.iloc[0]
    return float(valor) if pd.notna(valor) else 0.0

def calcular_variacao(atual: float, base: float):
    if base in (0, None) or pd.isna(base):
        return np.nan
    return (atual / base) - 1

def montar_tabela_analise_mensal(df_nominal: pd.DataFrame, df_corrigido: pd.DataFrame, competencia_ref: pd.Timestamp):
    atual = pd.Timestamp(competencia_ref).replace(day=1)
    anterior = (atual - pd.DateOffset(months=1)).replace(day=1)
    ano_anterior = (atual - pd.DateOffset(years=1)).replace(day=1)

    rot_atual = rotulo_competencia(atual)
    rot_anterior = rotulo_competencia(anterior)
    rot_ano_anterior = rotulo_competencia(ano_anterior)

    rot_acum_atual = f"Acum. até {rot_atual}"
    rot_acum_ano_ant = f"Acum. até {rot_ano_anterior}"
    rot_var_acum = f"∆% Acum. {rot_atual}/{rot_ano_anterior}"

    estrutura = [
        ("Receitas", "Receita Corrente", "RECEITAS CORRENTES"),
        ("Receitas", "Receita Tributária", "IMPOSTOS, TAXAS E CONTRIBUIÇÕES DE MELHORIA"),
        ("Receitas", "Receita de Transferência Corrente", "TRANSFERÊNCIAS CORRENTES"),

        ("Receitas Próprias", "IPTU", "IPTU"),
        ("Receitas Próprias", "ISS", "ISS"),
        ("Receitas Próprias", "ITBI", "ITBI"),
        ("Receitas Próprias", "TACL", "TACL"),

        ("Receitas Próprias Dívida Ativa", "IPTU", "D.A. IPTU"),
        ("Receitas Próprias Dívida Ativa", "ISS", "D.A. ISS"),
        ("Receitas Próprias Dívida Ativa", "ITBI", "D.A. ITBI"),
        ("Receitas Próprias Dívida Ativa", "TACL", "D.A. TACL"),

        ("Receitas de Transferências", "IPVA", "IPVA"),
        ("Receitas de Transferências", "FPM", "FPM"),
        ("Receitas de Transferências", "ICMS", "ICMS"),
    ]

    linhas = []

    for grupo, item, coluna in estrutura:
        n_atual = obter_valor_competencia(df_nominal, atual, coluna)
        n_anterior = obter_valor_competencia(df_nominal, anterior, coluna)
        n_ano_anterior = obter_valor_competencia(df_nominal, ano_anterior, coluna)

        r_atual = obter_valor_competencia(df_corrigido, atual, coluna)
        r_anterior = obter_valor_competencia(df_corrigido, anterior, coluna)
        r_ano_anterior = obter_valor_competencia(df_corrigido, ano_anterior, coluna)

        acum_atual = obter_valor_acumulado_ate_competencia(df_nominal, atual, coluna)
        acum_ano_anterior = obter_valor_acumulado_ate_competencia(df_nominal, ano_anterior, coluna)

        linhas.append({
            "Grupo": grupo,
            "Item": item,
            rot_atual: n_atual,
            rot_anterior: n_anterior,
            rot_ano_anterior: n_ano_anterior,
            f"∆% Nominal {rot_atual}/{rot_anterior}": calcular_variacao(n_atual, n_anterior),
            f"∆% Nominal {rot_atual}/{rot_ano_anterior}": calcular_variacao(n_atual, n_ano_anterior),
            f"∆% Real {rot_atual}/{rot_anterior}": calcular_variacao(r_atual, r_anterior),
            f"∆% Real {rot_atual}/{rot_ano_anterior}": calcular_variacao(r_atual, r_ano_anterior),
            rot_acum_atual: acum_atual,
            rot_acum_ano_ant: acum_ano_anterior,
            rot_var_acum: calcular_variacao(acum_atual, acum_ano_anterior),
        })

    df = pd.DataFrame(linhas)

    totais = []
    grupos_totalizar = [
        "Receitas Próprias",
        "Receitas Próprias Dívida Ativa",
        "Receitas de Transferências"
    ]

    for grupo in grupos_totalizar:
        sub = df[df["Grupo"] == grupo]

        totais.append({
            "Grupo": grupo,
            "Item": "Total",
            rot_atual: sub[rot_atual].sum(),
            rot_anterior: sub[rot_anterior].sum(),
            rot_ano_anterior: sub[rot_ano_anterior].sum(),
            f"∆% Nominal {rot_atual}/{rot_anterior}": calcular_variacao(
                sub[rot_atual].sum(), sub[rot_anterior].sum()
            ),
            f"∆% Nominal {rot_atual}/{rot_ano_anterior}": calcular_variacao(
                sub[rot_atual].sum(), sub[rot_ano_anterior].sum()
            ),
            f"∆% Real {rot_atual}/{rot_anterior}": np.nan,
            f"∆% Real {rot_atual}/{rot_ano_anterior}": np.nan,
            rot_acum_atual: sub[rot_acum_atual].sum(),
            rot_acum_ano_ant: sub[rot_acum_ano_ant].sum(),
            rot_var_acum: calcular_variacao(
                sub[rot_acum_atual].sum(), sub[rot_acum_ano_ant].sum()
            ),
        })

    df_totais = pd.DataFrame(totais)

    df_final = pd.concat(
        [
            df[df["Grupo"] == "Receitas"],
            df[df["Grupo"] == "Receitas Próprias"],
            df_totais[df_totais["Grupo"] == "Receitas Próprias"],
            df[df["Grupo"] == "Receitas Próprias Dívida Ativa"],
            df_totais[df_totais["Grupo"] == "Receitas Próprias Dívida Ativa"],
            df[df["Grupo"] == "Receitas de Transferências"],
            df_totais[df_totais["Grupo"] == "Receitas de Transferências"],
        ],
        ignore_index=True
    )

    return df_final, {
        "atual": atual,
        "anterior": anterior,
        "ano_anterior": ano_anterior,
        "rot_atual": rot_atual,
        "rot_anterior": rot_anterior,
        "rot_ano_anterior": rot_ano_anterior,
        "rot_acum_atual": rot_acum_atual,
        "rot_acum_ano_ant": rot_acum_ano_ant,
        "rot_var_acum": rot_var_acum,
    }

def montar_base_pizzas(df_corrigido: pd.DataFrame, contexto: dict):
    def receita_propria(comp):
        return (
            obter_valor_competencia(df_corrigido, comp, "IPTU") +
            obter_valor_competencia(df_corrigido, comp, "ISS") +
            obter_valor_competencia(df_corrigido, comp, "ITBI") +
            obter_valor_competencia(df_corrigido, comp, "TACL") +
            obter_valor_competencia(df_corrigido, comp, "D.A. IPTU") +
            obter_valor_competencia(df_corrigido, comp, "D.A. ISS") +
            obter_valor_competencia(df_corrigido, comp, "D.A. ITBI") +
            obter_valor_competencia(df_corrigido, comp, "D.A. TACL")
        )

    def receita_transferencias(comp):
        return (
            obter_valor_competencia(df_corrigido, comp, "IPVA") +
            obter_valor_competencia(df_corrigido, comp, "FPM") +
            obter_valor_competencia(df_corrigido, comp, "ICMS")
        )

    periodos = [
        ("Atual", contexto["atual"], contexto["rot_atual"]),
        ("Anterior", contexto["anterior"], contexto["rot_anterior"]),
        ("Ano Anterior", contexto["ano_anterior"], contexto["rot_ano_anterior"]),
    ]

    saida = {}
    for _, comp, rotulo in periodos:
        propria = receita_propria(comp)
        transf = receita_transferencias(comp)
        saida[rotulo] = pd.DataFrame({
            "Grupo": ["Receita Própria", "Receita de Transferências"],
            "Valor": [propria, transf]
        })

    return saida

def formatar_tabela_analise(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    for col in out.columns:
        if col in ["Grupo", "Item"]:
            continue

        if "∆%" in col:
            out[col] = out[col].map(
                lambda x: "-" if pd.isna(x) else f"{x:.2%}".replace(".", ",")
            )
        else:
            out[col] = out[col].map(
                lambda x: f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            )

    return out

# ---------------------------
# Funções API Transparência
# ---------------------------
def get_receita(exercicio: int, mes: int):
    payload = {
        "exercicio": str(exercicio),
        "mes": f"{mes:02d}",
        "administracao": "1",
        "recurso": "",
        "destinacao": "",
        "tipoRecurso": "",
        "grau": "10",
        "sequencia": None
    }
    headers = {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
    r = requests.post(URL_TRANSPARENCIA, headers=headers, json=payload, timeout=30)
    r.raise_for_status()
    return r.json().get("resultado", [])

@st.cache_data(show_spinner=False)
def load_balancete_api(data_inicio: str, data_fim: str) -> pd.DataFrame:
    dt_inicio = datetime.strptime(data_inicio, "%Y-%m-%d")
    dt_fim = datetime.strptime(data_fim, "%Y-%m-%d")

    registros = []
    ano = dt_inicio.year
    while ano <= dt_fim.year:
        for mes in range(1, 13):
            data_ref = datetime(ano, mes, 1)
            if data_ref < dt_inicio.replace(day=1) or data_ref > dt_fim.replace(day=1):
                continue

            dados = get_receita(ano, mes)
            for item in dados:
                registros.append({
                    "ano": ano,
                    "mes": mes,
                    "codigo": item.get("codigoFormatado"),
                    "nome": item.get("nome"),
                    "valor": float(item.get("valorArrecadadoMensal") or 0),
                    "data": datetime(ano, mes, 1)
                })
        ano += 1

    return pd.DataFrame(registros)

# ---------------------------
# Funções IPCA
# ---------------------------
@st.cache_data(show_spinner=False)
def fetch_ipca_series(limit_months: int = 240) -> pd.Series:
    url = "https://apisidra.ibge.gov.br/values/t/1737/n1/1/v/2266/p/all?formato=json"
    headers = {"User-Agent": "Mozilla/5.0"}

    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()
    data = r.json()

    if not isinstance(data, list) or len(data) < 2:
        return pd.Series(dtype=float)

    df = pd.DataFrame(data[1:])
    df["valor"] = pd.to_numeric(df["V"], errors="coerce")

    df["periodo"] = pd.to_datetime(df["D3C"], format="%Y%m", errors="coerce").dt.to_period("M")
    df = df[df["periodo"].notna() & df["valor"].notna()].sort_values("periodo")

    s = df.set_index("periodo")["valor"].astype(float)

    if limit_months and len(s) > limit_months:
        s = s.iloc[-limit_months:]

    return s

# ---------------------------
# Consolidação
# ---------------------------
def consolidar_liquido_periodo(df: pd.DataFrame) -> pd.DataFrame:
    resultados = []

    if df.empty:
        return pd.DataFrame(columns=["grupo", "ano", "mes", "valor_liquido", "data"])

    for grupo, anos in MAPEAMENTO_ANUAL.items():
        for ano in sorted(df["ano"].unique()):
            if ano not in anos:
                continue

            codigos_principais = anos[ano].get("principais", [])
            codigos_deducoes = anos[ano].get("deducoes", [])

            for mes in sorted(df.loc[df["ano"] == ano, "mes"].unique()):
                valor_bruto = df.loc[
                    (df["codigo"].isin(codigos_principais)) &
                    (df["ano"] == ano) &
                    (df["mes"] == mes),
                    "valor"
                ].sum()

                valor_deducao_raw = df.loc[
                    (df["codigo"].isin(codigos_deducoes)) &
                    (df["ano"] == ano) &
                    (df["mes"] == mes),
                    "valor"
                ].sum()

                valor_deducao = -abs(valor_deducao_raw) if valor_deducao_raw else 0.0
                liquido = valor_bruto + valor_deducao

                resultados.append({
                    "grupo": grupo,
                    "ano": ano,
                    "mes": mes,
                    "valor_liquido": liquido,
                    "data": datetime(ano, mes, 1)
                })

    return pd.DataFrame(resultados)

def montar_tabela_nominal(df_consolidado: pd.DataFrame) -> pd.DataFrame:
    if df_consolidado.empty:
        return pd.DataFrame()

    pivot = df_consolidado.pivot_table(
        index="data",
        columns="grupo",
        values="valor_liquido",
        aggfunc="sum",
        fill_value=0.0
    ).reset_index()

    rename_map = {
        "data": "Competência",
        "IPTU - Principal": "IPTU",
        "ITBI - Principal": "ITBI",
        "ISS - Principal": "ISS",
        "TACL - Principal": "TACL",
        "IPTU - Dívida Ativa": "D.A. IPTU",
        "ITBI - Dívida Ativa": "D.A. ITBI",
        "ISS - Dívida Ativa": "D.A. ISS",
        "TACL - Dívida Ativa": "D.A. TACL",
        "ICMS": "ICMS",
        "IPVA": "IPVA",
        "FPM": "FPM",
        "Receitas Correntes": "RECEITAS CORRENTES",
        "Impostos, Taxas e Contribuições de Melhoria": "IMPOSTOS, TAXAS E CONTRIBUIÇÕES DE MELHORIA",
        "Transferências Correntes": "TRANSFERÊNCIAS CORRENTES"
    }

    pivot = pivot.rename(columns=rename_map)

    colunas_finais = ["Competência"] + COLUNAS_SERIES

    for col in colunas_finais:
        if col not in pivot.columns:
            pivot[col] = 0.0

    pivot = pivot[colunas_finais].sort_values("Competência").reset_index(drop=True)
    pivot["Competência"] = pd.to_datetime(pivot["Competência"])
    return pivot

def montar_indices_correcao(ipca: pd.Series) -> pd.DataFrame:
    if ipca.empty:
        return pd.DataFrame(columns=["Competência", "IPCA Número-Índice", "Fator p/ valor presente"])

    ultimo_indice = ipca.iloc[-1]
    df_ipca = ipca.reset_index()
    df_ipca.columns = ["Competência", "IPCA Número-Índice"]
    df_ipca["Competência"] = df_ipca["Competência"].astype(str)
    df_ipca["Fator p/ valor presente"] = ultimo_indice / df_ipca["IPCA Número-Índice"]
    return df_ipca

def corrigir_tabela_por_ipca(df_nominal: pd.DataFrame, ipca: pd.Series) -> pd.DataFrame:
    if df_nominal.empty or ipca.empty:
        return pd.DataFrame()

    ultimo_indice = ipca.iloc[-1]
    df = df_nominal.copy()
    df["PeriodoIPCA"] = df["Competência"].dt.to_period("M").astype(str)

    mapa_ipca = ipca.copy()
    mapa_ipca.index = mapa_ipca.index.astype(str)

    df["IPCA_Competência"] = df["PeriodoIPCA"].map(mapa_ipca)
    df["FatorCorrecao"] = ultimo_indice / df["IPCA_Competência"]

    for col in COLUNAS_SERIES:
        df[col] = df[col] * df["FatorCorrecao"]

    df = df.drop(columns=["PeriodoIPCA", "IPCA_Competência", "FatorCorrecao"])
    return df

def montar_tabela_comparativa_exercicios(df_base: pd.DataFrame, serie: str) -> pd.DataFrame:
    if df_base.empty:
        return pd.DataFrame()

    df = df_base.copy()
    df["Exercício"] = df["Competência"].dt.year
    df["Mês"] = df["Competência"].dt.month
    df["NomeMês"] = df["Mês"].map(MESES_PT)

    ordem_meses = list(MESES_PT.values())

    tabela = df.pivot_table(
        index=["Mês", "NomeMês"],
        columns="Exercício",
        values=serie,
        aggfunc="sum",
        fill_value=0.0
    ).reset_index()

    tabela = tabela.sort_values("Mês").drop(columns="Mês")
    tabela = tabela.rename(columns={"NomeMês": "Mês"})
    tabela["Mês"] = pd.Categorical(tabela["Mês"], categories=ordem_meses, ordered=True)
    tabela = tabela.sort_values("Mês").reset_index(drop=True)
    tabela["Mês"] = tabela["Mês"].astype(str)

    cols = ["Mês"] + [c for c in tabela.columns if c != "Mês"]
    return tabela[cols]

def montar_base_grafico_comparativo(df_base: pd.DataFrame, serie: str) -> pd.DataFrame:
    if df_base.empty:
        return pd.DataFrame()

    df = df_base.copy()
    df["Exercício"] = df["Competência"].dt.year.astype(str)
    df["Mês"] = df["Competência"].dt.month
    df["NomeMês"] = df["Mês"].map(MESES_PT)

    ordem_meses = list(MESES_PT.values())
    df["NomeMês"] = pd.Categorical(df["NomeMês"], categories=ordem_meses, ordered=True)

    return df[["Competência", "Exercício", "Mês", "NomeMês", serie]].sort_values(["Mês", "Exercício"])

def montar_tabela_acumulada(df_base: pd.DataFrame) -> pd.DataFrame:
    if df_base.empty:
        return pd.DataFrame()

    df = df_base.copy().sort_values("Competência").reset_index(drop=True)

    for ano in sorted(df["Competência"].dt.year.unique()):
        mask = df["Competência"].dt.year == ano
        df_ano = df.loc[mask, COLUNAS_SERIES].cumsum()
        df.loc[mask, COLUNAS_SERIES] = df_ano.values

    return df

def formatar_moeda(df: pd.DataFrame, colunas_excluir=None) -> pd.DataFrame:
    if df.empty:
        return df

    colunas_excluir = colunas_excluir or []
    out = df.copy()

    for col in out.columns:
        if col not in colunas_excluir and pd.api.types.is_numeric_dtype(out[col]):
            out[col] = out[col].map(
                lambda x: f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            )
    return out

# ---------------------------
# Estado
# ---------------------------
if "dados_carregados" not in st.session_state:
    st.session_state["dados_carregados"] = False

for chave in [
    "df_nominal",
    "df_corrigido",
    "df_indices",
    "df_acumulado_nominal",
    "df_acumulado_corrigido",
]:
    if chave not in st.session_state:
        st.session_state[chave] = pd.DataFrame()

if "ipca_ultimo_periodo" not in st.session_state:
    st.session_state["ipca_ultimo_periodo"] = None

# ---------------------------
# UI
# ---------------------------
st.set_page_config(page_title="Painel Comparativo de Receitas", layout="wide")
st.title("Painel Comparativo de Receitas")
st.caption("Receitas nominais, receitas corrigidas, índices de correção, comparação entre exercícios, acumulados e análises mensais.")

with st.sidebar:
    st.header("Parâmetros")
    data_inicio = st.date_input("Data inicial", value=datetime(2024, 1, 1))
    data_fim = st.date_input("Data final", value=datetime.today())
    carregar = st.button("Carregar dados", width="stretch")

if carregar:
    if data_inicio > data_fim:
        st.error("A data inicial não pode ser maior que a data final.")
        st.stop()

    with st.spinner("Carregando receitas da API..."):
        df_raw = load_balancete_api(
            data_inicio.strftime("%Y-%m-%d"),
            data_fim.strftime("%Y-%m-%d")
        )

    if df_raw.empty:
        st.warning("Nenhum dado encontrado para o período informado.")
        st.session_state["dados_carregados"] = False
        st.stop()

    with st.spinner("Buscando série histórica do IPCA..."):
        ipca = fetch_ipca_series()

    if ipca.empty:
        st.error("Não foi possível obter a série do IPCA.")
        st.session_state["dados_carregados"] = False
        st.stop()

    df_consolidado = consolidar_liquido_periodo(df_raw)
    df_nominal = montar_tabela_nominal(df_consolidado)
    df_corrigido = corrigir_tabela_por_ipca(df_nominal, ipca)
    df_indices = montar_indices_correcao(ipca)
    df_acumulado_nominal = montar_tabela_acumulada(df_nominal)
    df_acumulado_corrigido = montar_tabela_acumulada(df_corrigido)

    st.session_state["df_nominal"] = df_nominal
    st.session_state["df_corrigido"] = df_corrigido
    st.session_state["df_indices"] = df_indices
    st.session_state["df_acumulado_nominal"] = df_acumulado_nominal
    st.session_state["df_acumulado_corrigido"] = df_acumulado_corrigido
    st.session_state["ipca_ultimo_periodo"] = str(ipca.index[-1])
    st.session_state["dados_carregados"] = True

if st.session_state["dados_carregados"]:
    df_nominal = st.session_state["df_nominal"]
    df_corrigido = st.session_state["df_corrigido"]
    df_indices = st.session_state["df_indices"]
    df_acumulado_nominal = st.session_state["df_acumulado_nominal"]
    df_acumulado_corrigido = st.session_state["df_acumulado_corrigido"]
    ipca_ultimo_periodo = st.session_state["ipca_ultimo_periodo"]

    # ---------------------------
    # Navegação principal persistente
    # ---------------------------
    ABAS = [
        "ABA 1 - Receitas Nominais",
        "ABA 2 - Receitas Corrigidas",
        "ABA 3 - Índices de Correção",
        "ABA 4 - Comparação entre Exercícios",
        "ABA 5 - Acumulado",
        "ABA 6 - Análise Mensal"
    ]

    if "aba_ativa" not in st.session_state:
        st.session_state["aba_ativa"] = "ABA 1 - Receitas Nominais"

    st.session_state["aba_ativa"] = st.segmented_control(
        "Navegação",
        options=ABAS,
        default=st.session_state["aba_ativa"],
        key="aba_ativa_selector",
        width="stretch",
    )

    aba_ativa = st.session_state["aba_ativa"]

    # ---------------------------
    # Renderização das abas
    # ---------------------------
    if aba_ativa == "ABA 1 - Receitas Nominais":
        st.subheader("Receitas Nominais")

        st.dataframe(
            formatar_moeda(df_nominal, colunas_excluir=["Competência"]),
            width="stretch",
            hide_index=True
        )

        serie_grafico = st.selectbox(
            "Selecione a série para visualizar",
            COLUNAS_SERIES,
            key="graf_nominal"
        )

        fig1 = px.line(
            df_nominal,
            x="Competência",
            y=serie_grafico,
            markers=True,
            title=f"Evolução mensal - {serie_grafico}"
        )
        st.plotly_chart(fig1, width="stretch")


    elif aba_ativa == "ABA 2 - Receitas Corrigidas":
        st.subheader("Receitas Corrigidas a valor presente pelo IPCA")
        st.caption(f"Atualização realizada até o último IPCA disponível: {ipca_ultimo_periodo}")

        st.dataframe(
            formatar_moeda(df_corrigido, colunas_excluir=["Competência"]),
            width="stretch",
            hide_index=True
        )

        serie_grafico_corr = st.selectbox(
            "Selecione a série para visualizar",
            COLUNAS_SERIES,
            key="graf_corr"
        )

        fig2 = px.line(
            df_corrigido,
            x="Competência",
            y=serie_grafico_corr,
            markers=True,
            title=f"Evolução mensal corrigida - {serie_grafico_corr}"
        )
        st.plotly_chart(fig2, width="stretch")


    elif aba_ativa == "ABA 3 - Índices de Correção":
        st.subheader("Índices de Correção")
        st.caption("Base: IPCA número-índice utilizado para atualizar os valores a preço presente.")

        df_indices_fmt = df_indices.copy()

        if "IPCA Número-Índice" in df_indices_fmt.columns:
            df_indices_fmt["IPCA Número-Índice"] = df_indices_fmt["IPCA Número-Índice"].map(
                lambda x: f"{x:.10f}".replace(".", ",")
            )

        if "Fator p/ valor presente" in df_indices_fmt.columns:
            df_indices_fmt["Fator p/ valor presente"] = df_indices_fmt["Fator p/ valor presente"].map(
                lambda x: f"{x:.10f}".replace(".", ",")
            )

        st.dataframe(
            df_indices_fmt,
            width="stretch",
            hide_index=True
        )

        fig3 = px.line(
            df_indices,
            x="Competência",
            y="IPCA Número-Índice",
            markers=True,
            title="Série histórica do IPCA número-índice"
        )
        st.plotly_chart(fig3, width="stretch")


    elif aba_ativa == "ABA 4 - Comparação entre Exercícios":
        st.subheader("Comparação entre exercícios lado a lado")

        tipo_comparacao = st.radio(
            "Base da comparação",
            ["Nominal", "Corrigida"],
            horizontal=True,
            key="tipo_comparacao"
        )

        df_base_comp = df_nominal if tipo_comparacao == "Nominal" else df_corrigido

        serie_comp = st.selectbox(
            "Selecione a série para comparar entre exercícios",
            COLUNAS_SERIES,
            key="serie_comp_exercicio"
        )

        tabela_comp = montar_tabela_comparativa_exercicios(df_base_comp, serie_comp)

        st.markdown(f"**Tabela comparativa — {serie_comp}**")
        st.dataframe(
            formatar_moeda(tabela_comp, colunas_excluir=["Mês"]),
            width="stretch",
            hide_index=True
        )

        base_grafico_comp = montar_base_grafico_comparativo(df_base_comp, serie_comp)

        fig4 = px.line(
            base_grafico_comp,
            x="NomeMês",
            y=serie_comp,
            color="Exercício",
            markers=True,
            title=f"Comparação entre exercícios — {serie_comp}",
            category_orders={"NomeMês": list(MESES_PT.values())}
        )
        fig4.update_layout(xaxis_title="Mês", yaxis_title="Valor")
        st.plotly_chart(fig4, width="stretch")


    elif aba_ativa == "ABA 5 - Acumulado":
        st.subheader("Acumulado")

        tipo_acumulado = st.radio(
            "Base do acumulado",
            ["Nominal", "Corrigida"],
            horizontal=True,
            key="tipo_acumulado"
        )

        df_base_acum = df_acumulado_nominal if tipo_acumulado == "Nominal" else df_acumulado_corrigido

        st.markdown("**Tabela acumulada**")
        st.dataframe(
            formatar_moeda(df_base_acum, colunas_excluir=["Competência"]),
            width="stretch",
            hide_index=True
        )

        serie_acum = st.selectbox(
            "Selecione a série acumulada para visualizar",
            COLUNAS_SERIES,
            key="serie_acumulada"
        )

        df_plot_acum = df_base_acum.copy()
        df_plot_acum["Exercício"] = df_plot_acum["Competência"].dt.year.astype(str)
        df_plot_acum["Mês"] = df_plot_acum["Competência"].dt.month
        df_plot_acum["NomeMês"] = df_plot_acum["Mês"].map(MESES_PT)

        ordem_meses = list(MESES_PT.values())
        df_plot_acum["NomeMês"] = pd.Categorical(
            df_plot_acum["NomeMês"],
            categories=ordem_meses,
            ordered=True
        )

        df_plot_acum = df_plot_acum.sort_values(["Exercício", "Mês"])

        fig5 = px.line(
            df_plot_acum,
            x="NomeMês",
            y=serie_acum,
            markers=True,
            color="Exercício",
            title=f"Acumulado por exercício — {serie_acum}",
            category_orders={"NomeMês": ordem_meses}
        )

        fig5.update_layout(
            xaxis_title="Mês",
            yaxis_title="Valor acumulado",
            showlegend=True
        )
        st.plotly_chart(fig5, width="stretch")


    elif aba_ativa == "ABA 6 - Análise Mensal":
        st.subheader("Análise mensal comparativa")

        competencias_disponiveis = (
            df_nominal["Competência"]
            .drop_duplicates()
            .sort_values(ascending=False)
            .tolist()
        )

        competencia_analise = st.selectbox(
            "Mês de análise",
            competencias_disponiveis,
            format_func=lambda x: rotulo_competencia(pd.Timestamp(x)),
            key="competencia_analise"
        )

        df_analise, contexto_analise = montar_tabela_analise_mensal(
            df_nominal=df_nominal,
            df_corrigido=df_corrigido,
            competencia_ref=pd.Timestamp(competencia_analise)
        )

        grupos_disponiveis = [
            "Receitas",
            "Receitas Próprias",
            "Receitas Próprias Dívida Ativa",
            "Receitas de Transferências",
        ]

        grupos_escolhidos = st.multiselect(
            "Grupos para exibir na tabela",
            options=grupos_disponiveis,
            default=grupos_disponiveis,
            key="grupos_analise_tab6"
        )

        if grupos_escolhidos:
            df_analise_filtrado = df_analise[df_analise["Grupo"].isin(grupos_escolhidos)].copy()
        else:
            df_analise_filtrado = df_analise.iloc[0:0].copy()

        st.caption(
            "Exibindo: " + ", ".join(grupos_escolhidos)
            if grupos_escolhidos else
            "Nenhum grupo selecionado."
        )

        st.markdown("**Tabela de análise**")
        st.dataframe(
            formatar_tabela_analise(df_analise_filtrado),
            width="stretch",
            hide_index=True
        )

        st.markdown("**Proporção entre Receita Própria e Receita de Transferências (valores reais)**")

        CORES_RECEITA = {
            "Receita Própria": "#1f77b4",
            "Receita de Transferências": "#ff7f0e"
        }

        bases_pizza = montar_base_pizzas(df_corrigido, contexto_analise)

        col1, col2, col3 = st.columns(3)

        for coluna, rotulo in zip([col1, col2, col3], bases_pizza.keys()):
            with coluna:
                fig_pizza = px.pie(
                    bases_pizza[rotulo],
                    names="Grupo",
                    values="Valor",
                    hole=0,
                    title=rotulo,
                    color="Grupo",
                    color_discrete_map=CORES_RECEITA
                )
                fig_pizza.update_traces(
                    textinfo="percent",
                    textposition="inside"
                )
                st.plotly_chart(fig_pizza, width="stretch")

        st.markdown("### Relatório automático de insights")

        insights, df_rank = gerar_insights_analise(
            df_analise=df_analise,
            df_corrigido=df_corrigido,
            contexto=contexto_analise
        )

        for texto in insights:
            st.markdown(f"- {texto}")

        st.markdown("### Ranking das rubricas no período analisado")
        st.dataframe(
            pd.DataFrame({
                "Item": df_rank["Item"],
                "Valor": df_rank["Valor"].map(formatar_num),
                "Participação": df_rank["Participação"].map(formatar_pct),
            }),
            width="stretch",
            hide_index=True
        )

else:
    st.info("Defina o período na barra lateral e clique em 'Carregar dados'.")
