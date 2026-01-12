import streamlit as st
import pandas as pd

st.markdown("""
    <style>
    .stApp { background-color: #633BBC; }
    .stApp p, .stApp h1, .stApp h2, .stApp h3, .stApp span, .stApp label { color: white !important; }
    </style>
""", unsafe_allow_html=True)
col_espaco, col_logo = st.columns([4, 1])
    
with col_logo:
        # Substitua 'logo.png' pelo caminho do seu arquivo ou URL
    st.image("logo_Papoon-13 (1).png", width=530)

# ===============================
# 1. VERIFICAÇÃO DE LOGIN
# ===============================
if not st.session_state.get("authentication_status"):
    st.error("🚫 Acesso negado. Por favor, faça login na página principal.")
    st.stop()

# ===============================
# 2. CONFIGURAÇÃO DA PÁGINA
# ===============================
st.set_page_config(
    page_title="Visão Geral das Campanhas",
    layout="wide"
)

st.title("📊 Visão Geral – Controle de Campanhas")

# ===============================
# 3. CONSTANTES E ARQUIVOS
# ===============================
ARQUIVOS = {
    "Park Shopping": "Mania - Project Control - CLIENTE  - Park Shopping.csv",
    "Anália Franco": "Mania - Project Control - CLIENTE  - Anália Franco.csv"
}

USUARIO_DONO = "lais.rosa"
USUARIO_DONO2="andre.potengy"

# ===============================
# 4. FUNÇÕES DE DADOS
# ===============================
@st.cache_data
def load_data_raw(caminho_arquivo):
    try:
        return pd.read_csv(caminho_arquivo)
    except FileNotFoundError:
        st.error(f"Arquivo não encontrado: {caminho_arquivo}")
        return pd.DataFrame()

def save_data(caminho_arquivo, df_editado):
    try:
        df_editado.to_csv(caminho_arquivo, index=False)
        st.cache_data.clear()
        st.toast("✅ Dados salvos com sucesso!", icon="💾")
        st.rerun()
    except Exception as e:
        st.error(f"Erro ao salvar: {e}")

def process_data_view(df_raw):
    df = df_raw.copy()
    df = df.dropna(how="all")

    if df.shape[1] >= 3:
        df = df.iloc[:, 1:]

    colunas_novas = ["campo", "talento_1", "talento_2"]
    if df.shape[1] >= 3:
        df.columns = colunas_novas + list(df.columns[3:])
        df = df[colunas_novas]

    return df[df["campo"].notna()]

# ===============================
# 5. ÁREA ADMINISTRATIVA (MELHORADA)
# ===============================
username_logado = st.session_state.get("username")

if username_logado == USUARIO_DONO or username_logado== USUARIO_DONO2:
    with st.expander("🔐 Painel Administrativo", expanded=False):

        st.markdown(
            f"""
            <div style="
                background: linear-gradient(145deg, #1f1f1f, #2b2b2b);
                padding:20px;
                border-radius:16px;
                box-shadow: 0 6px 16px rgba(0,0,0,0.6);
                margin-bottom:20px;
            ">
                <h3 style="margin-bottom:4px;">👤 Usuário Logado</h3>
                <p style="margin:0;"><strong>Username:</strong> {username_logado}</p>
                <p style="margin:0; color:#4cd137;"><strong>Permissão:</strong> Administrador</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        col_sel, col_info = st.columns([1, 2])

        with col_sel:
            opcao_arquivo = st.selectbox(
                "📄 Selecionar planilha para edição",
                list(ARQUIVOS.keys())
            )
            caminho_selecionado = ARQUIVOS[opcao_arquivo]

        with col_info:
         st.markdown(
        """
        <div style="
            background-color: #CBC3E3;
            padding:16px;
            border-radius:12px;
            border-left:6px solid #4cd137;
            box-shadow: 0 4px 10px rgba(0,0,0,0.15);
            color: #000000;
        ">
            <h4 style="margin-top:0; color:#000000;">✏️ Modo edição ativado</h4>
            <ul style="margin:0; padding-left:20px;">
                <li>Clique nas células para editar</li>
                <li>É possível adicionar ou remover linhas</li>
                <li>Clique em <strong>Salvar</strong> para aplicar no CSV</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )
            

        df_bruto = load_data_raw(caminho_selecionado)

        if not df_bruto.empty:
            st.markdown("### 📝 Editor de Dados")

            df_editado = st.data_editor(
                df_bruto,
                num_rows="dynamic",
                use_container_width=True,
                key=f"editor_{opcao_arquivo}"
            )

            col_btn, col_space = st.columns([1, 5])
            with col_btn:
                if st.button("💾 Salvar Alterações", type="primary"):
                    save_data(caminho_selecionado, df_editado)

    st.markdown("---")

# ===============================
# 6. FUNÇÕES VISUAIS
# ===============================
def get_valor(df, campo):
    resultado = df.loc[df["campo"] == campo, "valor"]
    return None if resultado.empty else resultado.values[0]

def status_badge(valor):
    if valor is None or pd.isna(valor) or str(valor).strip() == "":
        return "🔴 <span style='color:#ff6b6b'>Pendente</span>"
    return "🟢 <span style='color:#4cd137'>Feito</span>"

def is_checklist_item(campo):
    return isinstance(campo, str) and campo.lower().startswith(("post", "stories"))

def card_talento(nome, username, stories, posts, valor):
    st.markdown(
        f"""
        <div style="
            padding:24px;
            border-radius:16px;
            background: linear-gradient(145deg, #1e1e1e, #2a2a2a);
            color:#ffffff;
            box-shadow: 0 6px 14px rgba(0,0,0,0.6);
            margin-bottom:20px;
        ">
            <h2>{nome}</h2>
            <p style="color:#bbbbbb;">{username}</p>
            <hr style="border:1px solid #333;">
            <p>📸 <strong>{stories}</strong> stories</p>
            <p>🖼️ <strong>{posts}</strong> posts</p>
            <p>💰 <strong>{valor}</strong></p>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_checklist(df):
    checklist = df[df["campo"].apply(is_checklist_item)]
    for _, row in checklist.iterrows():
        st.markdown(
            f"**{row['campo']}**: {status_badge(row['valor'])}",
            unsafe_allow_html=True
        )

def render_outros_dados(df):
    excluir = ["Talento", "Username", "Stories contratados", "Posts contratados", "Valor Total Talentos"]
    outros = df[~df["campo"].isin(excluir) & ~df["campo"].apply(is_checklist_item)]

    if not outros.empty:
        st.dataframe(
            outros.rename(columns={"campo": "Item", "valor": "Valor"}),
            use_container_width=True,
            hide_index=True
        )

# ===============================
# 7. CARREGAMENTO DE DADOS
# ===============================
df_park = process_data_view(load_data_raw(ARQUIVOS["Park Shopping"]))
df_analia = process_data_view(load_data_raw(ARQUIVOS["Anália Franco"]))

df_t1 = df_park[["campo", "talento_1"]].rename(columns={"talento_1": "valor"})
df_t2 = df_park[["campo", "talento_2"]].rename(columns={"talento_2": "valor"})
df_t3 = df_analia[["campo", "talento_1"]].rename(columns={"talento_1": "valor"})
df_t4 = df_analia[["campo", "talento_2"]].rename(columns={"talento_2": "valor"})

# ===============================
# 8. ABAS
# ===============================
tabs = st.tabs([
    "RJ", "Goiânia", "Brasília", "Sorocaba + Goiânia",
    "Anália Franco", "Park Shopping", "Riosul"
])

with tabs[5]:
    st.header("📍 Park Shopping")
    col1, col2 = st.columns(2)

    with col1:
        card_talento(
            get_valor(df_t1, "Talento"),
            get_valor(df_t1, "Username"),
            get_valor(df_t1, "Stories contratados"),
            get_valor(df_t1, "Posts contratados"),
            get_valor(df_t1, "Valor Total Talentos"),
        )
        render_checklist(df_t1)
        render_outros_dados(df_t1)

    with col2:
        card_talento(
            get_valor(df_t2, "Talento"),
            get_valor(df_t2, "Username"),
            get_valor(df_t2, "Stories contratados"),
            get_valor(df_t2, "Posts contratados"),
            get_valor(df_t2, "Valor Total Talentos"),
        )
        render_checklist(df_t2)
        render_outros_dados(df_t2)

with tabs[4]:
    st.header("📍 Anália Franco")
    col1, col2 = st.columns(2)

    with col1:
        card_talento(
            get_valor(df_t3, "Talento"),
            get_valor(df_t3, "Username"),
            get_valor(df_t3, "Stories contratados"),
            get_valor(df_t3, "Posts contratados"),
            get_valor(df_t3, "Valor Total Talentos"),
        )
        render_checklist(df_t3)
        render_outros_dados(df_t3)

    with col2:
        card_talento(
            get_valor(df_t4, "Talento"),
            get_valor(df_t4, "Username"),
            get_valor(df_t4, "Stories contratados"),
            get_valor(df_t4, "Posts contratados"),
            get_valor(df_t4, "Valor Total Talentos"),
        )
        render_checklist(df_t4)
        render_outros_dados(df_t4)

for i in [0, 1, 2, 3, 6]:
    with tabs[i]:
        st.info("📌 Dados dessa localidade ainda não foram cadastrados.")
