import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import datetime

# Configuração da página
st.set_page_config(page_title="Calculadora de Investimentos", page_icon="💶", layout="wide")

# Estilo personalizado com CSS
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton > button {
        background-color: #28a745;
        color: white;
        padding: 10px 24px;
        font-size: 16px;
        border-radius: 8px;
        border: none;
    }
    .stButton > button:hover {
        background-color: #218838;
    }
    .resumo-box {
        border: 2px solid #007BFF;
        padding: 20px;
        border-radius: 10px;
        background-color: #e9f5ff;
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
    st.markdown("<h1 style='text-align: center; color: #007BFF;'>Juros Compostos</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        investimento_inicial = st.number_input("💼 Investimento Inicial (€)", min_value=0.0, value=20000.0, step=100.0)
        taxa_juros = st.slider("📈 Taxa de Juros Anual (%)", min_value=0.0, max_value=20.0, value=5.0, step=0.1)
        contribuicao_mensal = st.number_input("📆 Contribuição Mensal (€)", min_value=0.0, value=200.0, step=50.0)
        periodo_anos = st.number_input("📅 Período de Investimento (anos)", min_value=1, value=5)
    
    with col2:
        contribuicao_anual = st.number_input("📅 Contribuição Anual (€)", min_value=0.0, value=5000.0, step=100.0)
        data_inicio = st.date_input("📅 Data de Início", datetime.date.today())
        granularidade = st.radio("📊 Granularidade dos Resultados", ["Anual", "Mensal"])
        contribuicao_periodo = st.selectbox("💸 Contribuir no início ou fim do período?", ["Início", "Fim"])

    if st.button("🚀 Calcular Crescimento"):
        data_fim = data_inicio + datetime.timedelta(days=365 * periodo_anos)
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
        total_contribuicoes = (contribuicao_anual * periodo_anos) + (contribuicao_mensal * 12 * periodo_anos)
        juros_totais = saldo_final - investimento_inicial - total_contribuicoes

        # Resumo dos resultados
        st.markdown("<div class='resumo-box'>", unsafe_allow_html=True)
        st.subheader("📊 Resumo do Investimento")
        st.write(f"**Saldo Final:** € {saldo_final:,.2f}")
        st.write(f"**Total de Contribuições:** € {total_contribuicoes:,.2f}")
        st.write(f"**Juros Totais:** € {juros_totais:,.2f}")
        st.markdown("</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)

        with col1:
            # Tabela de resultados
            st.subheader("📅 Tabela de Crescimento")
            st.dataframe(df_resultado.style.format({"Saldo": "€ {:,.2f}"}))
        with col2:
            # Gráfico interativo
            fig = px.line(df_resultado, x='Data', y='Saldo', title='📈 Evolução do Saldo')
            fig.update_traces(line_color='#007BFF')
            fig.update_layout(template='plotly_white', xaxis_title='Data', yaxis_title='Saldo (€)')
            st.plotly_chart(fig, use_container_width=True)
