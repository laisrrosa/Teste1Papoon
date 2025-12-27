import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Verificar Login
if not st.session_state.get("authentication_status"):
    st.error("Por favor, faça login na página principal.")
    st.stop()

# 2. Configuração e Estilo (Fundo Roxo)
st.set_page_config(page_title="Tendências", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #6A0DAD; }
    .stApp p, .stApp h1, .stApp h2, .stApp h3, .stApp span, .stApp label { color: white !important; }
    </style>
""", unsafe_allow_html=True)

st.title("🔮 Análise de Tendência Individual")

try:
    # --- CARREGAMENTO E LIMPEZA ---
    df_qual = pd.read_csv('evolucao_qualidade_publico.csv')
    df_seg = pd.read_csv('evolucao_seguidores.csv')
    
    # Padronização agressiva para evitar erros de nomes
    df_qual['Perfil'] = df_qual['Perfil'].astype(str).str.strip()
    df_seg['Perfil'] = df_seg['Perfil'].astype(str).str.strip()

    date_cols = [c for c in df_qual.columns if c != 'Perfil']
    
    # --- LISTA DE SELEÇÃO (Focada nos 80 da Qualidade) ---
    perfis_para_selecao = sorted(df_qual['Perfil'].unique().tolist())
    
    # Debug na barra lateral para você ver os números reais
    st.sidebar.subheader("Status dos Dados")
    st.sidebar.write(f"Perfis na Qualidade: {len(df_qual)}")
    st.sidebar.write(f"Perfis em Seguidores: {len(df_seg)}")

    perfil_escolhido = st.selectbox("Selecione um perfil (Total: 80):", perfis_para_selecao)
    
    st.markdown("---")

    # ==========================================
    # SEÇÃO 1: QUALIDADE
    # ==========================================
    st.header("💎 Tendência de Qualidade")
    
    # Filtro de Qualidade
    df_q_p = df_qual[df_qual['Perfil'] == perfil_escolhido].copy()
    
    if not df_q_p.empty:
        # Converter % para número
        for col in date_cols:
            df_q_p[col] = df_q_p[col].astype(str).str.replace('%', '').astype(float)
        
        perfil_data_q = df_q_p.melt(id_vars=['Perfil'], value_vars=date_cols, var_name='Mes', value_name='Qualidade')
        perfil_data_q['Data_Real'] = pd.to_datetime(perfil_data_q['Mes'])

        fig_q = px.scatter(perfil_data_q, x='Data_Real', y='Qualidade', 
                           trendline="ols", trendline_color_override="white",
                           template="none", labels={'Qualidade': 'Qualidade (%)', 'Data_Real': 'Mês'})
        fig_q.add_traces(px.line(perfil_data_q, x='Data_Real', y='Qualidade').data)
        fig_q.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="white"),
                            xaxis=dict(gridcolor='rgba(255,255,255,0.1)', tickformat="%b %Y"),
                            yaxis=dict(gridcolor='rgba(255,255,255,0.1)'))
        st.plotly_chart(fig_q, use_container_width=True, theme=None)
        
        try:
            results = px.get_trendline_results(fig_q)
            slope = results.iloc[0]["px_fit_results"].params[1]
            
            if slope > 0:
                st.success(f"📈 **Ascensão:** O perfil de {perfil_escolhido} apresenta melhora na qualidade do público.")
            elif slope < 0:
                st.error(f"📉 **Queda:** O perfil de {perfil_escolhido} apresenta declínio na qualidade do público.")
            else:
                st.warning(f"➖ **Estável:** A qualidade do público de {perfil_escolhido} está constante.")
        except:
            st.info("ℹ️ Dados insuficientes para calcular tendência estatística de qualidade.")
    else:
        st.warning("⚠️ Perfil não encontrado no arquivo de Qualidade.")

    st.markdown("---")

    # ==========================================
    # SEÇÃO 2: SEGUIDORES
    # ==========================================
    st.header("👥 Tendência de Seguidores")
    
    # Filtro de Seguidores
    df_s_p = df_seg[df_seg['Perfil'] == perfil_escolhido].copy()

    if not df_s_p.empty:
        perfil_data_s = df_s_p.melt(id_vars=['Perfil'], value_vars=date_cols, var_name='Mes', value_name='Seguidores')
        perfil_data_s['Data_Real'] = pd.to_datetime(perfil_data_s['Mes'])

        fig_s = px.scatter(perfil_data_s, x='Data_Real', y='Seguidores', 
                           trendline="ols", trendline_color_override="#00FFCC",
                           template="none", labels={'Seguidores': 'Seguidores', 'Data_Real': 'Mês'})
        fig_s.add_traces(px.line(perfil_data_s, x='Data_Real', y='Seguidores').data)
        fig_s.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="white"),
                            xaxis=dict(gridcolor='rgba(255,255,255,0.1)', tickformat="%b %Y"),
                            yaxis=dict(gridcolor='rgba(255,255,255,0.1)'))
        st.plotly_chart(fig_s, use_container_width=True, theme=None)
        
        try:
            results_s = px.get_trendline_results(fig_s)
            slope_s = results_s.iloc[0]["px_fit_results"].params[1]
            
            if slope_s > 0:
                st.success(f"📈 **Ascensão:** A base de seguidores de {perfil_escolhido} está crescendo.")
            elif slope_s < 0:
                st.error(f"📉 **Queda:** A base de seguidores de {perfil_escolhido} está diminuindo.")
            else:
                st.warning(f"➖ **Estável:** O número de seguidores de {perfil_escolhido} está estagnado.")
        except:
            st.info("ℹ️ Dados insuficientes para calcular tendência estatística de seguidores.")
    else:
        # Se o perfil está na qualidade mas não nos seguidores, ele avisa aqui:
        st.error(f"❌ Não foram encontrados dados de seguidores para o perfil: {perfil_escolhido}")

except Exception as e:
    st.error(f"Ocorreu um erro técnico: {e}")