import streamlit as st
import pandas as pd
import numpy as np

# Configuração da página
st.set_page_config(page_title="Calculadora de Investimentos", page_icon=":money_with_wings:", layout="centered")

# Menu lateral para seleção de calculadoras
menu = st.sidebar.selectbox(
    "Selecione a Calculadora",
    [
        "Juros Compostos",
        # Outras calculadoras serão adicionadas futuramente
    ]
)

if menu == "Juros Compostos":
    st.title("Calculadora de Juros Compostos")
    
    # Entradas do usuário
    investimento_inicial = st.number_input("Investimento inicial (R$)", min_value=0.0, value=20000.0, step=100.0)
    contribuicao_anual = st.number_input("Contribuição anual (R$)", min_value=0.0, value=5000.0, step=100.0)
    contribuicao_mensal = st.number_input("Contribuição mensal (R$)", min_value=0.0, value=0.0, step=50.0)
    taxa_juros = st.number_input("Taxa de juros anual (%)", min_value=0.0, value=5.0, step=0.1) / 100
    duracao_anos = st.number_input("Duração do investimento (anos)", min_value=1, value=5)
    taxa_imposto = st.number_input("Taxa de imposto (%)", min_value=0.0, value=0.0, step=0.1) / 100
    taxa_inflacao = st.number_input("Taxa de inflação anual (%)", min_value=0.0, value=3.0, step=0.1) / 100
    
    if st.button("Calcular"):
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
        st.subheader("Resultado do Investimento")
        st.write(f"Saldo final: R$ {saldo:,.2f}")
        st.write(f"Saldo ajustado pela inflação: R$ {saldo_ajustado:,.2f}")
        
        st.subheader("Evolução Anual")
        st.dataframe(df_resultado)
        
        st.line_chart(df_resultado.set_index("Ano")["Saldo"])
