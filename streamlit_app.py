import streamlit as st
import pandas as pd
import numpy as np

# Configuração da página
st.set_page_config(page_title="Calculadora de Investimentos", page_icon=":money_with_wings:", layout="centered")

# Menu de Configurações
with st.sidebar.expander("⚙️ Configurações"):
    idioma = st.selectbox("Selecione o idioma / Select the language", ["Português", "English"])
    moeda = st.selectbox(
        "Selecione a moeda / Select the currency",
        ["Real (BRL)", "Dólar (USD)", "Euro (EUR)", "Libra (GBP)", "Iene (JPY)", "Franco Suíço (CHF)"]
    )
    simbolo_moeda = {
        "Real (BRL)": "R$",
        "Dólar (USD)": "$",
        "Euro (EUR)": "€",
        "Libra (GBP)": "£",
        "Iene (JPY)": "¥",
        "Franco Suíço (CHF)": "CHF"
    }[moeda]

# Textos dinâmicos para suporte a idiomas
textos = {
    "Português": {
        "menu_calculadora": "Selecione a Calculadora",
        "titulo": "Calculadora de Juros Compostos",
        "investimento_inicial": "Investimento inicial",
        "contribuicao_anual": "Contribuição anual",
        "contribuicao_mensal": "Contribuição mensal",
        "taxa_juros": "Taxa de juros anual (%)",
        "duracao_investimento": "Duração do investimento (anos)",
        "taxa_imposto": "Taxa de imposto (%)",
        "taxa_inflacao": "Taxa de inflação anual (%)",
        "calcular": "Calcular",
        "resultado": "Resultado do Investimento",
        "saldo_final": "Saldo final",
        "saldo_ajustado": "Saldo ajustado pela inflação",
        "evolucao_anual": "Evolução Anual"
    },
    "English": {
        "menu_calculadora": "Select Calculator",
        "titulo": "Compound Interest Calculator",
        "investimento_inicial": "Initial Investment",
        "contribuicao_anual": "Annual Contribution",
        "contribuicao_mensal": "Monthly Contribution",
        "taxa_juros": "Annual Interest Rate (%)",
        "duracao_investimento": "Investment Duration (years)",
        "taxa_imposto": "Tax Rate (%)",
        "taxa_inflacao": "Annual Inflation Rate (%)",
        "calcular": "Calculate",
        "resultado": "Investment Result",
        "saldo_final": "Final Balance",
        "saldo_ajustado": "Inflation-adjusted Balance",
        "evolucao_anual": "Annual Growth"
    }
}

# Menu lateral para seleção de calculadoras
menu = st.sidebar.selectbox(
    textos[idioma]["menu_calculadora"],
    [
        textos[idioma]["titulo"],
    ]
)

if menu == textos[idioma]["titulo"]:
    st.title(textos[idioma]["titulo"])
    
    # Entradas do usuário
    investimento_inicial = st.number_input(f"{textos[idioma]['investimento_inicial']} ({simbolo_moeda})", min_value=0.0, value=20000.0, step=100.0)
    contribuicao_anual = st.number_input(f"{textos[idioma]['contribuicao_anual']} ({simbolo_moeda})", min_value=0.0, value=5000.0, step=100.0)
    contribuicao_mensal = st.number_input(f"{textos[idioma]['contribuicao_mensal']} ({simbolo_moeda})", min_value=0.0, value=0.0, step=50.0)
    taxa_juros = st.number_input(textos[idioma]["taxa_juros"], min_value=0.0, value=5.0, step=0.1) / 100
    duracao_anos = st.number_input(textos[idioma]["duracao_investimento"], min_value=1, value=5)
    taxa_imposto = st.number_input(textos[idioma]["taxa_imposto"], min_value=0.0, value=0.0, step=0.1) / 100
    taxa_inflacao = st.number_input(textos[idioma]["taxa_inflacao"], min_value=0.0, value=3.0, step=0.1) / 100
    
    if st.button(textos[idioma]["calcular"]):
        saldo = investimento_inicial
        saldo_ajustado = investimento_inicial
        historico = []
        
        for ano in range(1, duracao_anos + 1):
            saldo += contribuicao_anual
            saldo *= (1 + taxa_juros)
            saldo -= saldo * taxa_imposto
            saldo_ajustado = saldo / ((1 + taxa_inflacao) ** ano)
            historico.append({
                "Ano": ano,
                "Saldo": saldo,
                "Saldo Ajustado": saldo_ajustado
            })
        
        df_resultado = pd.DataFrame(historico)
        st.subheader(textos[idioma]["resultado"])
        st.write(f"{textos[idioma]['saldo_final']}: {simbolo_moeda} {saldo:,.2f}")
        st.write(f"{textos[idioma]['saldo_ajustado']}: {simbolo_moeda} {saldo_ajustado:,.2f}")
        
        st.subheader(textos[idioma]["evolucao_anual"])
        st.dataframe(df_resultado)
        
        st.line_chart(df_resultado.set_index("Ano")["Saldo"])
