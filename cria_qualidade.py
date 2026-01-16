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
# Usernames fictícios
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
        user = f"{base}{sep}{sufixo}" if sufixo else f"{base}{sep}{''.join(random.choice(SILABAS) for _ in range(1))}"
    else:
        user = f"{base}{sufixo}"

    user = user.lower().strip("._")
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
# Série de "qualidade do público" (percentual)
# ----------------------------
def gerar_serie_qualidade(
    n_meses: int,
    inicio_min=45.0,
    inicio_max=85.0,
    delta_min=-2.2,   # variação mensal (pontos percentuais)
    delta_max=+2.2,
    prob_estavel=0.20,
    prob_evento=0.08  # evento (queda/subida maior)
):
    valor = round(random.uniform(inicio_min, inicio_max), 1)
    serie = [valor]

    for _ in range(n_meses - 1):
        if random.random() < prob_estavel:
            novo = valor
        else:
            delta = random.uniform(delta_min, delta_max)
            novo = round(valor + delta, 1)

            # evento: mudança mais forte (ex: campanha atrai público melhor/pior)
            if random.random() < prob_evento:
                evento = random.uniform(-4.0, 4.0)
                novo = round(novo + evento, 1)

        # limites realistas
        novo = max(0.0, min(100.0, novo))

        valor = novo
        serie.append(valor)

    return serie

# ----------------------------
# Gerar CSV no formato pedido
# ----------------------------
def gerar_csv_qualidade_publico(
    qtd_perfis=80,
    inicio_mes="2025-05",
    fim_mes="2026-01",
    arquivo_saida="qualidade_publico_ficticia.csv",
    seed=2026
):
    random.seed(seed)

    meses = gerar_meses(inicio_mes, fim_mes)
    header = ["Perfil"] + meses

    perfis = gerar_lista_usernames(qtd_perfis)

    with open(arquivo_saida, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)

        for perfil in perfis:
            serie = gerar_serie_qualidade(len(meses))
            # formata como "67.8%"
            serie_fmt = [f"{v:.1f}%" for v in serie]
            writer.writerow([perfil] + serie_fmt)

    print(f"Arquivo gerado: {arquivo_saida}")
    print(f"Perfis gerados: {qtd_perfis}")
    print("Colunas:", header)

if __name__ == "__main__":
    gerar_csv_qualidade_publico(
        qtd_perfis=80,
        inicio_mes="2025-05",
        fim_mes="2026-01",
        arquivo_saida="qualidade_publico_ficticia.csv",
        seed=2026
    )
