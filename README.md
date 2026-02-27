# 📊 Dashboard de Análise Preditiva: Licitações Públicas

Este projeto apresenta uma solução de inteligência de dados desenvolvida em **Streamlit** para analisar e prever tendências no mercado de licitações públicas no estado do Paraná, abrangendo o período de **janeiro de 2022 a dezembro de 2025**.

## 🎯 Objetivo Estratégico
O dashboard foi desenhado para apoiar a tomada de decisão comercial, permitindo diferenciar cenários de participação através de filtros interativos:
* **Capacidade Própria:** Editais com disputa por item/lote, onde a empresa possui autonomia técnica.
* **Necessidade de Parceria:** Editais de julgamento global, que exigem a formação de consórcios ou parcerias estratégicas para atendimento completo do objeto.

## 🛠️ Diferenciais Técnicos
* **Modelagem Estatística:** Utilização do modelo **ETS (Error, Trend, Seasonal)** via biblioteca *statsmodels* para captar padrões de tendência e sazonalidade.
* **Gestão de Risco:** Implementação de **Intervalos de Confiança de 95%**, permitindo uma avaliação visual da incerteza estatística nas previsões futuras.
* **Tratamento de Dados Dinâmico:** Pipeline que realiza limpeza, preenchimento de lacunas temporais (*resampling*) e pivotamento automático da base original.
* **Insights Sazonais:** Identificação automática dos meses de maior demanda histórica e recordes de frequência para planejamento antecipado de estoque.
