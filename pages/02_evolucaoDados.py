import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Verificar Login
if not st.session_state.get("authentication_status"):
    st.error("Acesso negado. Por favor, faça login na página principal.") #se não tiver feito login, dá erro
    st.stop()

# 2. Configuração da Página e Estilo
st.set_page_config(page_title="Evolução - Papoon", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    .stApp p, .stApp h1, .stApp h2, .stApp h3, .stApp span, .stApp label { color: white !important; }
    </style>
""", unsafe_allow_html=True)
col_espaco, col_logo = st.columns([4, 1])
    
with col_logo:
        # Substitua 'logo.png' pelo caminho do seu arquivo ou URL
    st.image("logo_Papoon-13 (1).png", width=530)




with col_espaco:
    st.title("📈 Evolução de Performance") #título da página

try:
    # --- CARREGAMENTO DE DADOS ---
    df_qual_raw = pd.read_csv('evolucao_qualidade_publico.csv')
    df_seg = pd.read_csv('evolucao_seguidores.csv')
    
    date_cols = [c for c in df_qual_raw.columns if c != 'Perfil']
    
    # Criar uma cópia numérica para os cálculos e gráficos
    df_qual_num = df_qual_raw.copy()
    for col in date_cols:
        df_qual_num[col] = df_qual_num[col].astype(str).str.replace('%', '').astype(float)
    
    # Calcular Evolução para Ordenação
    df_qual_num['Evol_Total'] = df_qual_num[date_cols[-1]] - df_qual_num[date_cols[0]]
    df_sorted = df_qual_num.sort_values(by='Evol_Total', ascending=False)
    
    # --- INTERAÇÃO ---
    n_perfis = st.slider("Selecione a quantidade de perfis (Top Evolução de Qualidade):", 1, len(df_sorted), 5)
    top_perfis_names = df_sorted.head(n_perfis)['Perfil'].tolist()

    # --- SEÇÃO 1: QUALIDADE ---
    st.header("💎 Qualidade do Público")
    
    # Gráfico de público de qualidade
    top_df_qual_num = df_qual_num[df_qual_num['Perfil'].isin(top_perfis_names)]
    top_df_qual_num['Perfil'] = pd.Categorical(top_df_qual_num['Perfil'], categories=top_perfis_names, ordered=True)
    df_plot_qual = top_df_qual_num.sort_values('Perfil').melt(id_vars=['Perfil'], value_vars=date_cols, var_name='Mês', value_name='Qualidade')
    
    fig1 = px.line(df_plot_qual, x='Mês', y='Qualidade', color='Perfil', markers=True, template="none")
    fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="white"))
    st.plotly_chart(fig1, use_container_width=True, theme=None)

    # Tabela de Qualidade (Com porcentagens igual ao original)
    st.subheader("Tabela: Evolução Mensal da Qualidade (%)")
    top_df_qual_raw = df_qual_raw[df_qual_raw['Perfil'].isin(top_perfis_names)].copy()
    top_df_qual_raw['Perfil'] = pd.Categorical(top_df_qual_raw['Perfil'], categories=top_perfis_names, ordered=True)
    st.dataframe(top_df_qual_raw.sort_values('Perfil'), use_container_width=True)

    st.markdown("---")

    # --- SEÇÃO 2: SEGUIDORES ---
    st.header("👥 Número de Seguidores")
    
    # Gráfico de Seguidores
    top_df_seg = df_seg[df_seg['Perfil'].isin(top_perfis_names)].copy()
    top_df_seg['Perfil'] = pd.Categorical(top_df_seg['Perfil'], categories=top_perfis_names, ordered=True)
    df_plot_seg = top_df_seg.sort_values('Perfil').melt(id_vars=['Perfil'], value_vars=date_cols, var_name='Mês', value_name='Seguidores')
    
    fig2 = px.line(df_plot_seg, x='Mês', y='Seguidores', color='Perfil', markers=True, template="none")
    fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="white"))
    st.plotly_chart(fig2, use_container_width=True, theme=None)

    # Tabela de Seguidores (Números absolutos)
    st.subheader("Tabela: Evolução Mensal de Seguidores")
    st.dataframe(top_df_seg.sort_values('Perfil'), use_container_width=True)

except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")