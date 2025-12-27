import streamlit as st
import pandas as pd
import plotly.express as px

# Verificar Login
if not st.session_state.get("authentication_status"):
    st.error("Por favor, faça login na página principal.")
    st.stop()

# Configuração e Estilo
st.set_page_config(page_title="Benchmarking", layout="wide")

st.markdown("<style>.stApp { background-color: #6A0DAD; } .stApp p, .stApp h1, .stApp h2, .stApp h3, .stApp span, .stApp label { color: white !important; }</style>", unsafe_allow_html=True)

st.title("📊 Benchmarking de Grupos")
st.markdown("""
Esta página mostra as porcentagens atuais do público de qualidade por perfil.
""")

try:
    df = pd.read_csv('evolucao_qualidade_publico.csv')
    date_cols = [c for c in df.columns if c != 'Perfil']
    for col in date_cols:
        df[col] = df[col].astype(str).str.replace('%', '').astype(float)

    # Calcular a média de qualidade atual (último mês disponível)
    ultimo_mes = date_cols[-1]
    df['Qualidade_Atual'] = df[ultimo_mes]

    # Categorização
    def categorizar(valor):
        if valor >= 80: return "Elite (>80%)"
        if valor >= 60: return "Standard (60-80%)"
        return "Em Atenção (<60%)"

    df['Categoria'] = df['Qualidade_Atual'].apply(categorizar)
    contagem = df['Categoria'].value_counts().reset_index()
    contagem.columns = ['Categoria', 'Quantidade']

    # Gráfico de Distribuição
    col1, col2 = st.columns([1, 1])
    
    with col1:
        fig_pizza = px.pie(contagem, values='Quantidade', names='Categoria', 
                          title="Distribuição da Base de Perfis",
                          color='Categoria',
                          color_discrete_map={
                              "Elite (>80%)": "#8210b3",      # Roxo escuro, 
                              "Standard (60-80%)":"#9065a0", # Roxo médio, 
                              "Em Atenção (<60%)": "#ed4b4b"
                          })
        fig_pizza.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",  # fundo externo
        plot_bgcolor="rgba(0,0,0,0)"    # fundo interno
    )
        st.plotly_chart(fig_pizza, use_container_width=True)
                

        



    with col2:
        st.subheader("Resumo por Categoria")
        st.dataframe(contagem, use_container_width=True)
        
except Exception as e:
    st.error(f"Erro: {e}")
try:
    # Filtro para ver os perfis por categoria
    cat_selecionada = st.selectbox(
        "Selecione uma categoria para listar os perfis:",
        contagem['Categoria']
    )

    perfis_cat = df[df['Categoria'] == cat_selecionada][
        ['Perfil', 'Qualidade_Atual']
    ]

    df_tabela = perfis_cat.sort_values(
        by='Qualidade_Atual',
        ascending=False
    )

    st.dataframe(
        df_tabela.style
            .set_properties(**{
                "background-color": "black",
                "color": "white",
                "border-color": "#444"
            })
            .set_table_styles([
                {
                    "selector": "th",
                    "props": [
                        ("background-color", "#111"),
                        ("color", "white"),
                        ("font-weight", "bold")
                    ]
                }
            ]),
        use_container_width=True
    )

except Exception as e:
    st.error(f"Erro: {e}")

# --- SEÇÃO: BENCHMARK DE SEGUIDORES ---
st.markdown("---")
st.title("📈 Benchmarking de Seguidores")
st.markdown("Análise da distribuição de tamanho da base dos perfis.")

try:
    # 1. Carregar dados de seguidores
    # Ajuste o nome do arquivo se necessário
    df_seg = pd.read_csv('evolucao_seguidores.csv')
    
    # Identificar colunas de data (excluindo 'Perfil')
    cols_data_seg = [c for c in df_seg.columns if c != 'Perfil']
    ultimo_mes_seg = cols_data_seg[-1]
    
    # Garantir que os dados são numéricos
    df_seg[ultimo_mes_seg] = pd.to_numeric(df_seg[ultimo_mes_seg], errors='coerce')
    df_seg['Seguidores_Atuais'] = df_seg[ultimo_mes_seg]

    # 2. Categorização por Volume (Exemplo de faixas, ajuste se necessário)
    def categorizar_seguidores(valor):
        if valor >=500000: return "Ultra (500k+)"
        if valor >= 100000: return "Mega (100k-500k)"
        if valor >= 50000:  return "Macro (50k-100k)"
        if valor >= 10000:  return "Médio (10k-50k)"
        return "Micro (<10k)"

    df_seg['Categoria_Seg'] = df_seg['Seguidores_Atuais'].apply(categorizar_seguidores)
    
    # Agrupamento para o gráfico
    contagem_seg = df_seg['Categoria_Seg'].value_counts().reset_index()
    contagem_seg.columns = ['Categoria', 'Quantidade']
    
    # Ordenação manual para a legenda ficar lógica
    ordem_cat = ["Ultra (500k+)", "Mega (100k-500k)", "Macro (50k-100k)", "Médio (10k-50k)", "Micro (<10k)"]
    contagem_seg['Categoria'] = pd.Categorical(contagem_seg['Categoria'], categories=ordem_cat, ordered=True)
    contagem_seg = contagem_seg.sort_values('Categoria')

    # 3. Visualização lado a lado (Pizza e Tabela)
    c1, c2 = st.columns([1, 1])

    with c1:
        fig_pizza_seg = px.pie(
            contagem_seg, 
            values='Quantidade', 
            names='Categoria',
            title="Distribuição por Porte de Seguidores",
            color='Categoria',
            color_discrete_map={
                "Ultra (>500k)" : "#0068c9", #azul
                "Mega (100k-500k)": "#8e44ad",      # Roxo escuro
                "Macro (50k-100k)": "#8210b3", # Roxo médio
                "Médio (10k-50k)": "#9065a0",# Roxo claro
                "Micro (<10k)": "#ed4b4b"    # Cinza/Branco
            }
        )
        fig_pizza_seg.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white")
        )
        st.plotly_chart(fig_pizza_seg, use_container_width=True)

    with c2:
        st.subheader("Resumo de Porte")
        st.dataframe(contagem_seg, use_container_width=True)

    # 4. Filtro de Detalhamento
    cat_seg_sel = st.selectbox(
        "Selecione o porte para listar os perfis:",
        ordem_cat
    )

    df_detalhe_seg = df_seg[df_seg['Categoria_Seg'] == cat_seg_sel][['Perfil', 'Seguidores_Atuais']]
    df_detalhe_seg = df_detalhe_seg.sort_values(by='Seguidores_Atuais', ascending=False)

    # Tabela estilizada
    st.dataframe(
        df_detalhe_seg.style
            .format({"Seguidores_Atuais": "{:,.0f}"}) # Formata com separador de milhar
            .set_properties(**{"background-color": "black", "color": "white", "border-color": "#444"})
            .set_table_styles([{"selector": "th", "props": [("background-color", "#111"), ("color", "white")]}]),
        use_container_width=True
    )

except Exception as e:
    st.error(f"Erro ao processar benchmarking de seguidores: {e}")