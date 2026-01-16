import random
import csv
from datetime import datetime

# ----------------------------
# Meses YYYY-MM
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
# Gerador de perfis fictícios
# ----------------------------
SILABAS = [
    "la","lu","li","le","lo","ma","me","mi","mo","mu","ra","re","ri","ro","ru",
    "ca","ce","ci","co","cu","ta","te","ti","to","tu","na","ne","ni","no","nu",
    "ga","ge","gi","go","gu","fa","fe","fi","fo","fu","pa","pe","pi","po","pu"
]

def gerar_username():
    base = "".join(random.choice(SILABAS) for _ in range(random.randint(2, 4)))

    sep = random.choice(["", ".", "_"])
    sufixo = ""
    r = random.random()
    if r < 0.65:
        sufixo = str(random.randint(0, 99))
    elif r < 0.85:
        sufixo = random.choice(["beauty", "make", "skin", "cos", "store", "oficial"])

    if sep:
        user = f"{base}{sep}{sufixo}" if sufixo else f"{base}{sep}{random.choice(SILABAS)}"
    else:
        user = f"{base}{sufixo}"

    return user.lower().strip("._")

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
# Série de seguidores (inteiros)
# ----------------------------
def gerar_serie_seguidores(
    n_meses: int,
    inicio_min=2000,
    inicio_max=50000,
    pct_var_min=-0.04,   # -4% ao mês
    pct_var_max=0.07,    # +7% ao mês
    prob_estavel=0.12,
    prob_pulo=0.10
):
    valor = random.randint(inicio_min, inicio_max)
    serie = [valor]

    for _ in range(n_meses - 1):
        if random.random() < prob_estavel:
            novo = valor
        else:
            pct = random.uniform(pct_var_min, pct_var_max)
            novo = int(round(valor * (1 + pct)))

            # pulo (viral/campanha)
            if random.random() < prob_pulo:
                boost = random.uniform(0.03, 0.20)
                novo = int(round(novo * (1 + boost)))

        novo = max(0, novo)
        # limita queda brusca (opcional)
        novo = max(novo, int(valor * 0.90))

        valor = novo
        serie.append(valor)

    return serie

# ----------------------------
# Série de qualidade do público (%)
# ----------------------------
def gerar_serie_qualidade(
    n_meses: int,
    inicio_min=45.0,
    inicio_max=85.0,
    delta_min=-2.2,      # variação mensal em pontos percentuais
    delta_max=+2.2,
    prob_estavel=0.20,
    prob_evento=0.08
):
    valor = round(random.uniform(inicio_min, inicio_max), 1)
    serie = [valor]

    for _ in range(n_meses - 1):
        if random.random() < prob_estavel:
            novo = valor
        else:
            delta = random.uniform(delta_min, delta_max)
            novo = round(valor + delta, 1)

            # evento: mudança maior
            if random.random() < prob_evento:
                evento = random.uniform(-4.0, 4.0)
                novo = round(novo + evento, 1)

        novo = max(0.0, min(100.0, novo))
        valor = novo
        serie.append(valor)

    return serie

# ----------------------------
# Gerar 2 CSVs usando os MESMOS perfis
# ----------------------------
def gerar_dois_csvs(
    qtd_perfis=80,
    inicio_mes="2025-05",
    fim_mes="2026-01",
    out_seguidores="seguidores_ficticios.csv",
    out_qualidade="qualidade_publico_ficticia.csv",
    seed=2026
):
    random.seed(seed)

    meses = gerar_meses(inicio_mes, fim_mes)
    header = ["Perfil"] + meses

    # gera perfis UMA vez e reaproveita
    perfis = gerar_lista_usernames(qtd_perfis)

    # 1) CSV de seguidores
    with open(out_seguidores, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for perfil in perfis:
            serie = gerar_serie_seguidores(len(meses))
            writer.writerow([perfil] + serie)

    # 2) CSV de qualidade (%)
    with open(out_qualidade, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for perfil in perfis:
            serie = gerar_serie_qualidade(len(meses))
            serie_fmt = [f"{v:.1f}%" for v in serie]
            writer.writerow([perfil] + serie_fmt)

    print("Gerado com sucesso:")
    print(f"- {out_seguidores}")
    print(f"- {out_qualidade}")
    print(f"Perfis: {qtd_perfis} | Meses: {inicio_mes} a {fim_mes}")

if __name__ == "__main__":
    gerar_dois_csvs(
        qtd_perfis=80,
        inicio_mes="2025-05",
        fim_mes="2026-01",
        out_seguidores="seguidores_ficticios2.csv",
        out_qualidade="qualidade_publico_ficticia2.csv",
        seed=2026
    )
