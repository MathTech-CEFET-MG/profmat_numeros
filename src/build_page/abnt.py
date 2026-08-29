#------------------------------------------------------------------------------#

import re
import unicodedata

#------------------------------------------------------------------------------#

def author_abnt(nome_completo: str) -> str:
    """
    Converte um nome completo (sem abreviações) para o formato ABNT:
    'SOBRENOME, Prenomes ...'

    Trata casos atípicos, incluindo:
        - Afixos brasileiros (Júnior, Filho, Neto, Sobrinho...)
        - Partículas brasileiras e estrangeiras (de, da, do, von, van, del, bin, al...)
        - Sobrenomes compostos, inclusive com hífen
        - Nomes estrangeiros com partículas múltiplas
        - Variações ortográficas (com/sem acento)
        - Casos com afixos múltiplos
        - Preservação de acentos e capitalização adequada
    """

    if not nome_completo or not nome_completo.strip():
        return ""

    # Normaliza espaços
    nome = nome_completo.strip().split()

    # Palavras consideradas "afixos" no sobrenome
    afixos = {
        "junior", "júnior", "juniora", "filho", "neto", "sobrinho",
        "senior", "sênior"
    }

    # Partículas que não devem ser capitalizadas
    particulas = {
        "de", "da", "do", "das", "dos",
        "del", "della", "dalla", "dei",
        "van", "von", "der", "den", "het",
        "bin", "al", "ibn", "la", "le"
    }

    # ---------- Etapa 1: detectar hífens ----------
    # Mantemos nomes hifenizados como unidades (ex.: Silva-Santos)
    nome_hifen = []
    for parte in nome:
        if "-" in parte:
            subtokens = parte.split("-")
            nome_hifen.append([sub for sub in subtokens])
        else:
            nome_hifen.append([parte])

    # Reconstituir lista plana preservando hífens internamente
    tokens = []
    for grupo in nome_hifen:
        if len(grupo) > 1:
            tokens.append("-".join(grupo))
        else:
            tokens.append(grupo[0])

    # ---------- Etapa 2: identificar sobrenome ----------
    ultimo = tokens[-1].lower()

    # Caso o último termo seja um afixo → sobrenome composto
    if ultimo in afixos and len(tokens) >= 3:
        # Sobrenome = penúltimo + último
        sobrenome = tokens[-2:]
        prenomes = tokens[:-2]
    else:
        sobrenome = [tokens[-1]]
        prenomes = tokens[:-1]

    # ---------- Etapa 3: incluir partículas que pertencem ao sobrenome ----------
    while prenomes and prenomes[-1].lower() in particulas:
        sobrenome.insert(0, prenomes.pop(-1))

    # ---------- Etapa 4: formatação de capitalização ----------
    sobrenome_formatado = []
    for palavra in sobrenome:
        base = palavra.lower()
        if base in particulas:
            sobrenome_formatado.append(base)
        else:
            sobrenome_formatado.append(palavra.upper())

    sobrenome_final = " ".join(sobrenome_formatado)

    # Prenomes com capitalização normal
    prenomes_final = " ".join(prenomes)

    return f"{sobrenome_final}, {prenomes_final}"


#------------------------------------------------------------------------------#
def abnt(data: dict) -> str:

    year   = data["year"]
    author = data["author"]
    title  = data["title"]
    school = data["school"]
    url    = data["url"]

    author = author_abnt(author)

    return f"{author}. _{title}_. Dissertação (Mestrado) — {school}, {year}. Disponível em: <{url}>."

#------------------------------------------------------------------------------#