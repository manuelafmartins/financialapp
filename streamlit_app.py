import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Calculadora de Investimentos", page_icon="💰", layout="centered")

# Estilo personalizado com CSS
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 24px;
        font-size: 16px;
        border-radius: 8px;
        border: none;
    }
    .stButton > button:hover {
        background-color: #45a049;
    }
    </style>
""", unsafe_allow_html=True)

# Menu de Configurações
with st.sidebar.expander("⚙️ Configurações"):
    idioma = st.selectbox("🌐 Selecione o idioma / Select the language", ["Português", "English", "Français", "Español"])
    moeda = st.selectbox(
        "💱 Selecione a moeda / Select the currency",
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

# Título com destaque
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>💸 Calculadora de Juros Compostos 💸</h1>", unsafe_allow_html=True)

# Entradas do usuário organizadas em duas colunas
col1, col2 = st.columns(2)

with col1:
    investimento_inicial = st.number_input(f"{simbolo_moeda} Investimento Inicial", min_value=0.0, value=20000.0, step=100.0)
    contribuicao_anual = st.number_input(f"{simbolo_moeda} Contribuição Anual", min_value=0.0, value=5000.0, step=100.0)
    taxa_juros = st.slider("📈 Taxa de Juros Anual (%)", min_value=0.0, max_value=20.0, value=5.0, step=0.1)

with col2:
    contribuicao_mensal = st.number_input(f"{simbolo_moeda} Contribuição Mensal", min_value=0.0, value=0.0, step=50.0)
    duracao_anos = st.slider("⏳ Duração do Investimento (anos)", min_value=1, max_value=50, value=5)
    taxa_inflacao = st.slider("📉 Taxa de Inflação (%)", min_value=0.0, max_value=10.0, value=3.0, step=0.1)

# Botão de cálculo com ícone
if st.button("🚀 Calcular Crescimento"):
    saldo = investimento_inicial
    historico = []
    with st.spinner('Calculando...'):
        for ano in range(1, duracao_anos + 1):
            saldo += contribuicao_anual
            saldo *= (1 + (taxa_juros / 100))
            saldo_ajustado = saldo / ((1 + (taxa_inflacao / 100)) ** ano)
            historico.append({"Ano": ano, "Saldo": saldo, "Saldo Ajustado": saldo_ajustado})

    df_resultado = pd.DataFrame(historico)
    saldo_final = df_resultado['Saldo'].iloc[-1]
    saldo_ajustado_final = df_resultado['Saldo Ajustado'].iloc[-1]
    
    # Exibir resultados em cartões
    col1, col2 = st.columns(2)
    col1.metric("📊 Saldo Final", f"{simbolo_moeda} {saldo_final:,.2f}")
    col2.metric("💡 Saldo Ajustado pela Inflação", f"{simbolo_moeda} {saldo_ajustado_final:,.2f}")

    # Gráfico interativo com Plotly
    fig = px.line(df_resultado, x='Ano', y='Saldo', title='📈 Evolução do Saldo ao Longo dos Anos')
    fig.update_layout(template='plotly_white')
    st.plotly_chart(fig, use_container_width=True)
    
    st.success("✅ Cálculo concluído!")
