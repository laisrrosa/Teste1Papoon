import streamlit as st 
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import os
import pandas as pd
import plotly.express as px 
st.set_page_config(page_title="Papoon - Dashboard", layout="wide")


#função para mudar o fundo para roxo
def mudar_fundo():
    st.markdown(
        """
        <style>
        /* Muda o fundo de toda a página */
        .stApp {
            background-color: #6A0DAD;
        }
        
        /* Ajusta a cor do texto para branco para dar contraste */
        .stApp p, .stApp h1, .stApp h2, .stApp h3, .stApp span, .stApp label {
            color: white !important;
        }
        </style>
        """,
        unsafe_allow_html=True  # O nome correto do parâmetro é este
    )

mudar_fundo() #chama a função de mudar fundo
with open('config.yaml') as file: 
    config= yaml.load(file, Loader=SafeLoader) #carrega o arquivo com login e senha dos usuários
    
authenticator= stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

authenticator.login()


if st.session_state.get("authentication_status"):  #se o usuário inserir usuário e senha corretos, abrir na página principal
    st.session_state["logged_in"] = True
    authenticator.logout(location="sidebar")
    st.write(f"Bem-vindo, *{st.session_state['name']}*")
    st.title("🚀 Papoon ")

# Carregar dados para os cálculos rápidos
    df_qual = pd.read_csv('evolucao_qualidade_publico.csv')
    df_seg = pd.read_csv('evolucao_seguidores.csv')

# Cálculos Rápidos
    total_seguidores = df_seg['2025-12'].sum()
    media_qualidade = pd.to_numeric(df_qual['2025-12'].str.replace('%','')).mean()
    st.header("Resumo de dados dos seguidores")
    # 1. Layout de Métricas (KPIs)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Audiência Total", f"{total_seguidores:,.0f}".replace(',', '.'))
    with col2:
        st.metric("Qualidade Média", f"{media_qualidade:.1f}%")
    with col3:
        st.metric("Perfis Ativos", len(df_qual))

    st.markdown("---")

    # 2. Destaques do Mês (Pódio)
    st.subheader("🏆 Destaques em Qualidade (Dezembro)")
    top_3_seg = df_qual[['Perfil', '2025-12']].copy()
    top_3_seg['Val'] = pd.to_numeric(top_3_seg['2025-12'].str.replace('%',''))
    top_3_seg= top_3_seg.sort_values('Val', ascending=False).head(3)


    c1, c2, c3 = st.columns(3)
    for idx, row in enumerate(top_3_seg.itertuples()):
        with [c1, c2, c3][idx]:
            st.info(f"**{idx+1}º Lugar**\n\n{row.Perfil} ({row.Val}%)")
            
    st.subheader("🏆 Destaques em Seguidores (Dezembro)")
    top_3_seg = df_seg[['Perfil', '2025-12']].copy()
    top_3_seg['Val'] = pd.to_numeric(top_3_seg['2025-12'], errors= 'coerce')
    top_3_seg = top_3_seg.sort_values('Val', ascending=False).head(3)

    c11, c22, c33 = st.columns(3)
    colunas = [c11, c22, c33]

    for idx, row in enumerate(top_3_seg.itertuples()):
        with colunas[idx]:
            # Formata o número com ponto separador de milhar (ex: 12.783)
            valor_formatado = f"{row.Val:,.0f}".replace(",", ".")
            st.success(f"**{idx+1}º Lugar**\n\n{row.Perfil}\n\n{valor_formatado} seguidores")

    st.markdown("---")

    # 3. Resumo Visual Rápido
    st.subheader("📊 Panorama Geral")

    # Criando o gráfico
    fig_home = px.bar(df_seg, x='Perfil', y='2025-12', title="Distribuição de Seguidores por Perfil", template="none")

    # Ajustando a ordem para decrescente e as cores do layout
    fig_home.update_layout(
        xaxis={'categoryorder':'total descending'}, # Esta linha faz a ordenação
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)', 
        font=dict(color="white")
    )

    st.plotly_chart(fig_home, use_container_width=True, theme=None)
            
    

    
elif st.session_state.get("authentication_status") is False: #se o usuário inserir usuário e senha incorretos, mostrar mensagem de erro
    st.error('Usuário/Senha inválido(s)')
elif st.session_state.get("authentication_status") is None: #se o usuário não inserir usuário ou senha, mostrar mensagem de errp
    st.error('Digite um usuário e senha')
    

