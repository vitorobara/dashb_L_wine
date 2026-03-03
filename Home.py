import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.exponential_smoothing.ets import ETSModel
import plotly.graph_objects as go

# Configuração da página
st.set_page_config(page_title="Análise de Licitações", layout="wide")

# Barra Lateral - Filtros
st.sidebar.header("Configurações da Análise")
opcao = st.sidebar.selectbox(
    "Selecione o Cenário:",
    ["Capacidade Própria (Por Item/Lote)", "Necessidade de Parceria (Global)"]
)
# Mapeamento da seleção para a coluna do DataFrame
coluna_map = {
    "Capacidade Própria (Por Item/Lote)": "Sim, por item/lote",
    "Necessidade de Parceria (Global)": "Não, julgamento global"
}
col_selecionada = coluna_map[opcao]

# 1. Carregamento e Preparação dos Dados
@st.cache_data
def load_data():
    df = pd.read_excel('dataset/Base-PR.xlsx')
    df['Data'] = pd.to_datetime(df['Data'], format='%Y-%m-%d')
    
    df_pivot = df.pivot_table(index='Data', 
                              columns='Disputa_Parcial', 
                              values='Objeto', # Qualquer coluna serve para contar
                              aggfunc='count').fillna(0)
    df_pivot = df_pivot.resample('MS').sum().fillna(0)
    
    return df_pivot

df_completo = load_data()
modelo = df_completo[col_selecionada]

# 2. Introdução (Texto Estratégico)
st.title("📊 Análise de Tendências e Sazonalidade em Licitações")

st.markdown("""
### Contexto Estratégico
Este dashboard apresenta o comportamento das oportunidades de licitação entre **2022 e 2025**. 
O objetivo é transformar dados históricos em inteligência competitiva.

> **Nota sobre a Amostragem:** Embora o intervalo de 48 meses seja considerado um tamanho amostral jovem, 
estamos captando a dinâmica de mercado mais recente e relevante, permitindo identificar padrões 
emergentes e janelas de oportunidade.
""")


# 4. Processamento do Modelo ETS
model = ETSModel(modelo, error='add', trend='add', seasonal='add', seasonal_periods=12)
fit = model.fit()

# Previsão para 12 meses
pred = fit.get_prediction(start=len(modelo), end=len(modelo) + 11)
df_fc = pred.summary_frame(alpha=0.05)

# 5. Construção do Gráfico Plotly (com a Área Rosa)
fig = go.Figure()

# Área Rosa (Incerteza)
fig.add_trace(go.Scatter(
    x=df_fc.index, y=df_fc['pi_upper'],
    mode='lines', line=dict(width=0), showlegend=False
))
fig.add_trace(go.Scatter(
    x=df_fc.index, y=df_fc['pi_lower'],
    mode='lines', fill='tonexty',
    fillcolor='rgba(255, 192, 203, 0.4)', 
    line=dict(width=0), name='Intervalo de Confiança (95%)'
))

# Histórico
fig.add_trace(go.Scatter(
    x=modelo.index, y=modelo.values,
    mode='lines+markers', name='Histórico Real', line=dict(color='#1f77b4')
))

# Forecast
fig.add_trace(go.Scatter(
    x=df_fc.index, y=df_fc['mean'],
    mode='lines', name='Forecast Holt-Winters',
    line=dict(color='red', dash='dash')
))

fig.update_layout(
    title=f"Tendência para: {opcao}",
    xaxis_title="Período",
    yaxis_title="Frequência de Licitações",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    template="plotly_white",
    height=500
)


# Renderiza o gráfico
st.plotly_chart(fig, use_container_width=True)

st.info("💡 Dica: Use a área sombreada rosa para entender a margem de risco em suas decisões de estoque ou parcerias.")
# 6. Insights Adicionais
col1, col2 = st.columns(2)
#with col1:
#    st.metric("Média Histórica", f"{serie.mean():.2f}")
#with col2:
#    st.metric("Maior frequência", f"{df_fc['mean'].iloc[0]:.2f}")

# Cálculo das médias por mês (independente do ano)
meses_nomes = {
    1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 
    5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto', 
    9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
}

# Agrupamos pelo mês do índice e tiramos a média
medias_sazonais = modelo.groupby(modelo.index.month).mean()
medias_sazonais.index = medias_sazonais.index.map(meses_nomes)
top_3_meses = medias_sazonais.sort_values(ascending=False).head(3)

# Exibição nos Colunas
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏆 Meses de Maior Demanda")
    st.write("Média histórica por mês (2022-2025):")
    for mes, valor in top_3_meses.items():
        st.markdown(f"**{mes}**: {valor:.2f} licitações/mês")

with col2:
    st.subheader("🚀 Tendência")
    st.metric("Previsão p/ Próximo Mês", f"{df_fc['mean'].iloc[2]:.2f}")
    st.write(f"Conforme o modelo ETS, a tendência imediata é de {'alta' if df_fc['mean'].iloc[2] > modelo.iloc[1] else 'baixa'}.")

st.info("💡 A análise de médias por mês ajuda a identificar a sazonalidade, permitindo que você planeje recursos e parcerias antes dos meses de pico.")
