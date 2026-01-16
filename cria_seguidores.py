import random
import csv
import string
from datetime import datetime

# ----------------------------
# Util: meses YYYY-MM
# ----------------------------
def gerar_meses(inicio: str, fim: str):
    ini = datetime.strptime(inicio, "%Y-%m")
    end = datetime.strptime(fim, "%Y-%m")

    meses = []
    y, m = ini.year, ini.month
    while (y < end.year) or (y == end.year and m <= end.month):
        meses.append(f"{y:04d}-{m:02d}")
        m += 1
        if m == 13:
            m = 1
            y += 1
    return meses

# ----------------------------
# Util: gerar username fictício
# ----------------------------
SILABAS = [
    "la", "lu", "li", "le", "lo",
    "ma", "me", "mi", "mo", "mu",
    "ra", "re", "ri", "ro", "ru",
    "ca", "ce", "ci", "co", "cu",
    "ta", "te", "ti", "to", "tu",
    "na", "ne", "ni", "no", "nu",
    "ga", "ge", "gi", "go", "gu",
    "fa", "fe", "fi", "fo", "fu"
]

def gerar_username():
    # Base com 2 a 4 sílabas
    n = random.randint(2, 4)
    base = "".join(random.choice(SILABAS) for _ in range(n))

    # Chance de adicionar "ponto" ou "underscore"
    sep = ""
    r = random.random()
    if r < 0.33:
        sep = "."
    elif r < 0.66:
        sep = "_"

    # Sufixo (opcional): 0 a 2 dígitos, ou pequeno token
    sufixo = ""
    if random.random() < 0.65:
        sufixo = str(random.randint(0, 99))
    elif random.random() < 0.25:
        sufixo = random.choice(["oficial", "store", "beauty", "cos", "make"])

    # Monta username e remove duplicações de separador
    if sep:
        user = f"{base}{sep}{sufixo}" if sufixo else f"{base}{sep}{random.choice(SILABAS)}"
    else:
        user = f"{base}{sufixo}"

    # Regras simples (estilo IG): minúsculo e sem espaços
    user = user.lower().replace("__", "_").replace("..", ".").strip("._")
    return user

def gerar_lista_usernames(qtd: int):
    vistos = set()
    nomes = []
    while len(nomes) < qtd:
        u = gerar_username()
        if u not in vistos:
            vistos.add(u)
            nomes.append(u)
    return nomes

# ----------------------------
# Util: gerar série de seguidores
# ----------------------------
def gerar_serie_seguidores(
    n_meses: int,
    inicio_min=2000,
    inicio_max=50000,
    pct_var_min=-0.04,    # -4% ao mês
    pct_var_max=0.07,     # +7% ao mês
    prob_estavel=0.12,    # chance de manter igual no mês
    prob_pulo=0.10        # chance de "pulo" (viral/campanha)
):
    valor = random.randint(inicio_min, inicio_max)
    serie = [valor]

    for _ in range(n_meses - 1):
        if random.random() < prob_estavel:
            novo = valor
        else:
            pct = random.uniform(pct_var_min, pct_var_max)
            novo = int(round(valor * (1 + pct)))

            # pulo por campanha/viral
            if random.random() < prob_pulo:
                boost = random.uniform(0.03, 0.20)  # +3% a +20% extra
                novo = int(round(novo * (1 + boost)))

        novo = max(0, novo)
        # Limita queda muito brusca (opcional)
        novo = max(novo, int(valor * 0.90))

        valor = novo
        serie.append(valor)

    return serie

# ----------------------------
# Geração do CSV
# ----------------------------
def gerar_csv_ficticio(
    qtd_perfis=80,
    inicio_mes="2025-05",
    fim_mes="2026-01",
    arquivo_saida="seguidores_ficticios.csv",
    seed=123
):
    random.seed(seed)

    meses = gerar_meses(inicio_mes, fim_mes)
    header = ["Perfil"] + meses

    perfis = gerar_lista_usernames(qtd_perfis)

    with open(arquivo_saida, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)

        for perfil in perfis:
            serie = gerar_serie_seguidores(len(meses))
            writer.writerow([perfil] + serie)

    print(f"Arquivo gerado: {arquivo_saida}")
    print(f"Perfis gerados: {qtd_perfis}")
    print("Colunas:", header)

if __name__ == "__main__":
    gerar_csv_ficticio(
        qtd_perfis=80,
        inicio_mes="2025-05",
        fim_mes="2026-01",
        arquivo_saida="seguidores_ficticios.csv",
        seed=2026
    )
