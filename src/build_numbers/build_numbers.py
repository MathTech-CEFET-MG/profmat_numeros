from pathlib import Path

from dados import csv_dissertacao, csv_instituicoes, caminho_saida_graficos

numbers_path = caminho_saida_graficos.parent / "numbers.md"
diretorio_atual = Path(__file__).parent

# Título e descrição de cada gráfico exibido na página. Para adicionar um
# gráfico novo, basta acrescentar uma entrada aqui
GRAFICOS = [
    {
        "arquivo": "grafico_vagas_vs_dissertacoes.html",
        "titulo": "Vagas Ofertadas vs Dissertações Defendidas por Instituição",
        "descricao": "Compara, ano a ano, as vagas ofertadas e as dissertações defendidas de cada instituição. Use os menus para escolher a instituição e o polo.",
    },
    {
        "arquivo": "grafico_evolucao_vagas_dissertacoes.html",
        "titulo": "Evolução Nacional: Vagas vs Dissertações",
        "descricao": "Total nacional de vagas ofertadas e dissertações defendidas em cada ano, somando todas as instituições do PROFMAT.",
    },
    {
        "arquivo": "grafico_crescimento_rede.html",
        "titulo": "Crescimento da Rede PROFMAT",
        "descricao": "Número de instituições com pelo menos uma dissertação defendida em cada ano.",
    },
    {
        "arquivo": "grafico_ranking_instituicoes.html",
        "titulo": "Top 20 Instituições com Mais Dissertações",
        "descricao": "As 20 instituições com o maior número de dissertações defendidas no total.",
    },
    {
        "arquivo": "grafico_dissertacao_instituicao.html",
        "titulo": "Dissertações por Instituição",
        "descricao": "Número total de dissertações defendidas em cada instituição do PROFMAT.",
    },
    {
        "arquivo": "grafico_dissertacao_regiao.html",
        "titulo": "Dissertações por Região",
        "descricao": "Número total de dissertações defendidas, agrupado por região do país.",
    },
    {
        "arquivo": "grafico_dissertacao_estado.html",
        "titulo": "Dissertações por Estado",
        "descricao": "Número total de dissertações defendidas, agrupado por estado.",
    },
    {
        "arquivo": "grafico_instituicao_regiao.html",
        "titulo": "Instituições por Região",
        "descricao": "Número de instituições associadas ao PROFMAT em cada região do país.",
    },
    {
        "arquivo": "grafico_dissertacoes_categoria.html",
        "titulo": "Dissertações por Categoria Administrativa",
        "descricao": "Número de dissertações defendidas, agrupado por categoria administrativa da instituição (federal, estadual, etc).",
    },
    {
        "arquivo": "grafico_vagas_por_regiao_pizza.html",
        "titulo": "Distribuição de Vagas Ofertadas por Região",
        "descricao": "Participação de cada região no total de vagas ofertadas. Use o menu para filtrar por ano.",
    },
]

SCRIPTS_DE_GRAFICO = [
    "build_graficos.py",
    "grafico_dissertacoes_vagas.py",
    "grafico_distribuicao_vagas_regiao.py",
]

# ------------------------------------------------------------------------------#
def gerar_graficos():
    caminho_saida_graficos.mkdir(parents=True, exist_ok=True)


    """Executa cada script de gráfico, um de cada vez"""

    for script in SCRIPTS_DE_GRAFICO:
        print(f"Gerando gráficos de {script}...")
        caminho_script = diretorio_atual / script
        codigo = caminho_script.read_text(encoding="utf-8")
        exec(compile(codigo, str(caminho_script), "exec"), {"__name__": "__main__"})

# ------------------------------------------------------------------------------#
def create_numbers(file_path, n_dis, n_inst):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("# Dissertações em Números\n\n")
        f.write(f"- **Número de dissertações:** {n_dis}\n")
        f.write(f"- **Número de instituições:** {n_inst}\n")

        for grafico in GRAFICOS:
            f.write(f"## {grafico['titulo']}\n\n")
            f.write(f"{grafico['descricao']}\n\n")
            f.write(f"[Abrir gráfico](graficos/{grafico['arquivo']})\n\n")


# ------------------------------------------------------------------------------#
def main():
    gerar_graficos()

    # Numero de dissertações e de instituições
    n_dis = len(csv_dissertacao)
    n_inst = len(csv_instituicoes)


    create_numbers(numbers_path, n_dis, n_inst)


# ------------------------------------------------------------------------------#
if __name__ == "__main__":
    main()

# ------------------------------------------------------------------------------#
