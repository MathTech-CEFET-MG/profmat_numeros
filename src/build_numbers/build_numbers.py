#------------------------------------------------------------------------------#

from pathlib import Path
# import build_graphics

docs_path    = Path("docs")
numbers_path = docs_path / "numbers" / "numbers.md"

#------------------------------------------------------------------------------#
def create_numbers(file_path, n):

    with open(file_path, "w", encoding="utf-8") as f:

        f.write("# Dissertações em Números\n\n")
        f.write(f"Número de dissertações: {n}\n\n")

        # numero de:
        # intituições
        # vagas
        # ???

        f.write('- [Grafico de vaga e dissertações por instituição](Graficos/grafico_vagas_vs_dissertacoes.html)\n')
        f.write('- [Grafico de dissertações por estados](Graficos/grafico_dissertacao_estado.html)\n')
        f.write('- [Grafico de dissertações por regiões](Graficos/grafico_dissertacao_regiao.html)\n')
        f.write('- [Grafico de dissertações por instituições](Graficos/grafico_dissertacao_instituicao.html)\n')
        f.write('- [Grafico de instituição por região](Graficos/grafico_instituicao_regiao.html)\n')
        f.write('- [Grafico de dissertações por categoria administrativa](Graficos/grafico_dissertacoes_categoria.html)\n')

#------------------------------------------------------------------------------#
def main():

    # Criar os gráficos

    # Numero de dissertações
    n_dis = 8000

    create_numbers(numbers_path, n_dis)

#------------------------------------------------------------------------------#
if __name__ == "__main__":
    main()

#------------------------------------------------------------------------------#
