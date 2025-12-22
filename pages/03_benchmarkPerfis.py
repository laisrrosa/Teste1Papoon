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
                              "Elite (>80%)": "#2ecc71", 
                              "Standard (60-80%)": "#f1c40f", 
                              "Em Atenção (<60%)": "#e74c3c"
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

