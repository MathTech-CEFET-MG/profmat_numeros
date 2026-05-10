import plotly.express as px
import pandas as pd
import numpy as np
from pathlib import Path

diretorio_atual = Path(__file__).parent

caminho_csv_dissertacao = diretorio_atual.parent / 'csv' / 'teste_atualizado.csv'
csv_dissertacao = pd.read_csv(caminho_csv_dissertacao)

caminho_csv_instituicao = diretorio_atual.parent / 'csv' / 'instituicoes_profmat_classificadas.csv'
csv_instituicoes = pd.read_csv(caminho_csv_instituicao)

def OrdemDecrescenteOuCrescente(df, x, organizacao):
    if organizacao == 'decrescente':
        verifica = False
    elif organizacao == 'crescente':
        verifica = True
    else:
        print("Erro: Use 'crescente' ou 'decrescente'")
        return df

    df = df.sort_values(by=x, ascending=verifica)
    return df
 
def gerar_grafico_barras(csv, x, y, titulo, caminho_saida, coluna_agrupar, coluna_valor=None, funcao_agg=None, ordem='decrescente', cor=None):

    if x == 'Contagem' or y == 'Contagem':
        df = csv.groupby(coluna_agrupar).size().rename('Contagem').reset_index()
    else:
        df = csv.groupby(coluna_agrupar).agg({coluna_valor: funcao_agg}).reset_index()


    coluna_para_ordenar = 'Contagem' if (x == 'Contagem' or y == 'Contagem') else coluna_valor
    bool_ordem = (ordem == 'crescente')
    df_ordenado = df.sort_values(by=coluna_para_ordenar, ascending=bool_ordem)


    cor_grafico = cor if cor else coluna_agrupar

    fig = px.bar(
        df_ordenado,
        x=x,
        y=y,
        title=titulo,
        color=cor_grafico,
        width=1300
    )

    fig.write_html("../docs/numbers/Graficos/" + caminho_saida)

    

gerar_grafico_barras(
    csv= csv_instituicoes,
    x= 'Categoria administrativa',
    y= 'Quantidade de dissertações na base',
    titulo= 'Dissertações por Categoria Adiministrativa',
    caminho_saida='grafico_dissertacoes_categoria.html',
    coluna_agrupar='Categoria administrativa',
    coluna_valor='Quantidade de dissertações na base',
    funcao_agg='sum',
    ordem = 'crescente'

)

""" grafico de dissertacoes por instituicao  """
instituicao_counts_df = csv_dissertacao.groupby('Instituição Corrigida').size().rename('Contagem').reset_index()
OrdemDecrescenteOuCrescente(instituicao_counts_df,'Contagem', 'decrescente')

grafico_disertacao_instituicao = px.bar(instituicao_counts_df, x='Contagem', y='Instituição Corrigida',
       title='Frequência de Ocorrências por Instituição',
       color = 'Instituição Corrigida', width= 1300)

grafico_disertacao_instituicao.write_html("../docs/numbers/Graficos/grafico_dissertacao_instituicao.html")

""" grafico de instituicoes por regiao """

regioes_counts = csv_instituicoes.groupby('Região').size().rename('Contagem').reset_index()
OrdemDecrescenteOuCrescente(regioes_counts,'Contagem', 'decrescente')

grafico_instituicao_regiao = px.bar(regioes_counts, x = 'Região', y = 'Contagem',
        title='Instituição por Região',
        color='Região', width=1300)
grafico_instituicao_regiao.write_html("../docs/numbers/Graficos/grafico_instituicao_regiao.html")

""" grafico de dissertaçoes por regiao  """

regioes_dissertacoes = csv_instituicoes.groupby('Região').agg({'Quantidade de dissertações na base': sum}).reset_index()
OrdemDecrescenteOuCrescente(regioes_dissertacoes,'Quantidade de dissertações na base','decrescente')

grafico_dissertacao_regiao = px.bar(regioes_dissertacoes, x='Região', y='Quantidade de dissertações na base',
       title='Frequência de Ocorrências por Região',
       color = 'Região', width= 1300)
grafico_dissertacao_regiao.write_html("../docs/numbers/Graficos/grafico_dissertacao_regiao.html")

""" grafico de dissertacoes por estado """

estados_dissertacoes = csv_instituicoes.groupby('Estado').agg({'Quantidade de dissertações na base': sum}).reset_index()
OrdemDecrescenteOuCrescente(estados_dissertacoes, 'Quantidade de dissertações na base', 'decrescente')

grafico_dissertacao_estado = px.bar(estados_dissertacoes, x  = 'Quantidade de dissertações na base', y = 'Estado',
                                    title = 'Número de dissertações por Estado',
                                    color = 'Estado', width= 1300)
grafico_dissertacao_estado.write_html("../docs/numbers/Graficos/grafico_dissertacao_estado.html")




