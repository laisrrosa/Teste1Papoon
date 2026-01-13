import streamlit as st 
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import os
import pandas as pd
import plotly.express as px 
st.set_page_config(page_title="Papoon - Dashboard", layout="wide") #configurando a página de dashboard


#função para mudar o fundo para roxo
def mudar_fundo():
    st.markdown(
        """
        <style>
        /* Muda o fundo de toda a página */
        .stApp {
            background-color:#633BBC;
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
col_espaco, col_logo = st.columns([4, 1])
    
with col_logo:
        # Substitua 'logo.png' pelo caminho do seu arquivo ou URL
        st.image("logo_Papoon-13 (1).png", width=530)
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
    # Criar 2 colunas: a primeira ocupa 80% do espaço, a segunda 20% para adicionar logo. atualizado em 27/12/2025 por laís Rodrigues
    
    
    
    with col_espaco:
        st.write(f"Bem-vindo, *{st.session_state['name']}*")
        st.title("🚀 Papoon ")

# Carregar dados para os cálculos rápidos
    df_qual = pd.read_csv('publico_qualidade.csv')
    df_seg = pd.read_csv('evolucao_seguidores4.csv')

# Cálculos Rápidos
    total_seguidores = df_seg['2026-01'].sum() #soma o total de seguidores do último mês
    media_qualidade = pd.to_numeric(df_qual['2026-01'].str.replace('%','')).mean() #média da porcentagem do público de qualidade
    st.header("Resumo de dados dos seguidores") #título
    # 1. Layout de Métricas (KPIs)
    col1, col2, col3 = st.columns(3)
    with col1: #coluna 1
        st.metric("Audiência Total", f"{total_seguidores:,.0f}".replace(',', '.'))
    with col2:  #coluna 2
        st.metric("Qualidade Média", f"{media_qualidade:.1f}%")
    with col3:  #coluna 3
        st.metric("Perfis Ativos", len(df_qual))

    st.markdown("---") #divisão da página

    # 2. Destaques do Mês (Pódio)
    st.subheader("🏆 Destaques em Qualidade (Janeiro)") #título da sessão
    top_3_seg = df_qual[['Perfil', '2026-01']].copy()
    top_3_seg['Val'] = pd.to_numeric(top_3_seg['2026-01'].str.replace('%',''))
    top_3_seg= top_3_seg.sort_values('Val', ascending=False).head(3) #pega os 3 maiores valores do público de qualidade

     #criando 3 colunas 
    c1, c2, c3 = st.columns(3)
    for idx, row in enumerate(top_3_seg.itertuples()): #faz os perfis aparecerem na ordem do maior para o menor público de qualidade
        with [c1, c2, c3][idx]:
            st.info(f"**{idx+1}º Lugar**\n\n{row.Perfil} ({row.Val}%)")
            
    st.subheader("🏆 Destaques em Seguidores (Janeiro)") #título da sessão
    top_3_seg = df_seg[['Perfil', '2026-01']].copy()
    top_3_seg['Val'] = pd.to_numeric(top_3_seg['2026-01'], errors= 'coerce')
    top_3_seg = top_3_seg.sort_values('Val', ascending=False).head(3) #pega os 3 maiores valores do número de seguidores


    c11, c22, c33 = st.columns(3)
    colunas = [c11, c22, c33]

    for idx, row in enumerate(top_3_seg.itertuples()): #faz os perfis aparecerem na ordem do maior para o menor número de seguidores
        with [c1, c2, c3][idx]:
         with colunas[idx]:
            # Formata o número com ponto separador de milhar (ex: 12.783)
            valor_formatado = f"{row.Val:,.0f}".replace(",", ".")
            st.success(f"**{idx+1}º Lugar**\n\n{row.Perfil}\n\n{valor_formatado} seguidores")

    st.markdown("---") #divisão da página

    # 3. Resumo Visual Rápido
    st.subheader("📊 Panorama Geral")

    # Criando o gráfico
    fig_home = px.bar(df_seg, x='Perfil', y='2026-01', title="Distribuição de Seguidores por Perfil", template="none")

    # Ajustando a ordem para decrescente e as cores do layout, atualizado 27/12/2025 por Laís Rosa
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
    

