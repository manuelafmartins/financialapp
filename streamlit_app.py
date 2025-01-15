import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import datetime

# Configuração da página
st.set_page_config(page_title="Calculadora de Investimentos", page_icon="💶", layout="centered")

# Estilo personalizado com CSS
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton > button {
        background-color: #007BFF;
        color: white;
        padding: 10px 24px;
        font-size: 16px;
        border-radius: 8px;
        border: none;
    }
    .stButton > button:hover {
        background-color: #0056b3;
    }
    </style>
""", unsafe_allow_html=True)

# Menu lateral para seleção de calculadoras
menu = st.sidebar.selectbox(
    "1. Selecione a Análise",
    [
        "Juros Compostos",
        "Juros Simples",
        "ROI"
    ]
)

if menu == "Juros Compostos":
    st.markdown("<h1 style='text-align: center; color: #007BFF;'>Calculadora de Juros Compostos</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        investimento_inicial = st.number_input("💼 Investimento Inicial (€)", min_value=0.0, value=20000.0, step=100.0)
        contribuicao_anual = st.number_input("📅 Contribuição Anual (€)", min_value=0.0, value=5000.0, step=100.0)
        taxa_juros = st.slider("📈 Taxa de Juros Anual (%)", min_value=0.0, max_value=20.0, value=5.0, step=0.1)
        granularidade = st.radio("📊 Granularidade dos Resultados", ["Anual", "Mensal"])
    
    with col2:
        contribuicao_mensal = st.number_input("📆 Contribuição Mensal (€)", min_value=0.0, value=0.0, step=50.0)
        data_inicio = st.date_input("📅 Data de Início", datetime.date.today())
        data_fim = st.date_input("📅 Data de Fim", datetime.date.today() + datetime.timedelta(days=365*5))
        contribuicao_periodo = st.selectbox("💸 Contribuir no início ou fim do período?", ["Início", "Fim"])

    if st.button("🚀 Calcular Crescimento"):
        saldo = investimento_inicial
        historico = []
        periodo = 'M' if granularidade == "Mensal" else 'A'
        datas = pd.date_range(start=data_inicio, end=data_fim, freq=periodo)
        
        with st.spinner('🔄 Calculando...'):
            for i, data in enumerate(datas):
                if contribuicao_periodo == "Início":
                    saldo += contribuicao_mensal if periodo == 'M' else contribuicao_anual
                saldo *= (1 + (taxa_juros / (100 * (12 if periodo == 'M' else 1))))
                if contribuicao_periodo == "Fim":
                    saldo += contribuicao_mensal if periodo == 'M' else contribuicao_anual
                historico.append({"Data": data, "Saldo": saldo})
        
        df_resultado = pd.DataFrame(historico)
        saldo_final = df_resultado['Saldo'].iloc[-1]
        total_principal = investimento_inicial + (contribuicao_anual * (data_fim.year - data_inicio.year))
        total_contribuicoes = total_principal - investimento_inicial
        juros_totais = saldo_final - total_principal
        poder_compra_ajustado = saldo_final / ((1 + 0.03) ** (data_fim.year - data_inicio.year))
        
        # Resumo dos resultados
        st.subheader("📊 Resumo do Investimento")
        st.write(f"**Saldo Final:** € {saldo_final:,.2f}")
        st.write(f"**Total do Principal:** € {total_principal:,.2f}")
        st.write(f"**Total de Contribuições:** € {total_contribuicoes:,.2f}")
        st.write(f"**Juros Totais:** € {juros_totais:,.2f}")
        st.write(f"**Poder de Compra Ajustado pela Inflação:** € {poder_compra_ajustado:,.2f}")
        
        # Tabela de resultados
        st.subheader("📅 Tabela de Crescimento")
        st.dataframe(df_resultado)
        
        # Gráfico interativo
        fig = px.area(df_resultado, x='Data', y='Saldo', title='📈 Evolução do Saldo')
        fig.update_traces(line_color='#007BFF')
        fig.update_layout(template='plotly_white', xaxis_title='Data', yaxis_title='Saldo (€)')
        st.plotly_chart(fig, use_container_width=True)