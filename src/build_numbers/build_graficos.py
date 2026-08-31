import plotly.graph_objects as go
import plotly.express as px

from dados import csv_dissertacao, csv_instituicoes, df_total, regioes_fixas, caminho_saida_graficos


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


def gerar_grafico_barras(csv, x, y, titulo, caminho_saida, coluna_agrupar, coluna_valor=None, funcao_agg=None,
                         ordem='decrescente', cor=None):
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

    fig.write_html(caminho_saida_graficos / caminho_saida)


gerar_grafico_barras(
    csv=csv_instituicoes,
    x='Categoria administrativa',
    y='Quantidade de dissertações na base',
    titulo='Dissertações por Categoria Adiministrativa',
    caminho_saida='grafico_dissertacoes_categoria.html',
    coluna_agrupar='Categoria administrativa',
    coluna_valor='Quantidade de dissertações na base',
    funcao_agg='sum',
    ordem='crescente'

)

""" grafico de dissertacoes por instituicao  """
instituicao_counts_df = csv_dissertacao.groupby('Instituição Corrigida').size().rename('Contagem').reset_index()
OrdemDecrescenteOuCrescente(instituicao_counts_df, 'Contagem', 'decrescente')

grafico_disertacao_instituicao = px.bar(instituicao_counts_df, x='Contagem', y='Instituição Corrigida',
                                        title='Frequência de Ocorrências por Instituição',
                                        color='Instituição Corrigida', width=1300)

grafico_disertacao_instituicao.write_html(caminho_saida_graficos / "grafico_dissertacao_instituicao.html")

""" grafico de instituicoes por regiao """

regioes_counts = csv_instituicoes.groupby('Região').size().rename('Contagem').reset_index()
OrdemDecrescenteOuCrescente(regioes_counts, 'Contagem', 'decrescente')

grafico_instituicao_regiao = px.bar(regioes_counts, x='Região', y='Contagem',
                                    title='Instituição por Região',
                                    color='Região', width=1300)
grafico_instituicao_regiao.write_html(caminho_saida_graficos / "grafico_instituicao_regiao.html")

""" grafico de dissertaçoes por regiao  """

regioes_dissertacoes = csv_instituicoes.groupby('Região').agg({'Quantidade de dissertações na base': sum}).reset_index()
OrdemDecrescenteOuCrescente(regioes_dissertacoes, 'Quantidade de dissertações na base', 'decrescente')

grafico_dissertacao_regiao = px.bar(regioes_dissertacoes, x='Região', y='Quantidade de dissertações na base',
                                    title='Frequência de Ocorrências por Região',
                                    color='Região', width=1300)
grafico_dissertacao_regiao.write_html(caminho_saida_graficos / "grafico_dissertacao_regiao.html")

""" grafico de dissertacoes por estado """

estados_dissertacoes = csv_instituicoes.groupby('Estado').agg({'Quantidade de dissertações na base': sum}).reset_index()
OrdemDecrescenteOuCrescente(estados_dissertacoes, 'Quantidade de dissertações na base', 'decrescente')

grafico_dissertacao_estado = px.bar(estados_dissertacoes, x='Quantidade de dissertações na base', y='Estado',
                                    title='Número de dissertações por Estado',
                                    color='Estado', width=1300)
grafico_dissertacao_estado.write_html(caminho_saida_graficos / "grafico_dissertacao_estado.html")

""" 1) Evolução anual nacional: Vagas Ofertadas vs Dissertações (barras agrupadas) """
df_evolucao = df_total[['Ano', 'Vagas', 'Dissertações']].sort_values('Ano')

fig_evolucao = go.Figure()
fig_evolucao.add_trace(go.Bar(
    x=df_evolucao['Ano'], y=df_evolucao['Vagas'],
    name='Vagas Ofertadas', marker=dict(color='#2196F3')
))
fig_evolucao.add_trace(go.Bar(
    x=df_evolucao['Ano'], y=df_evolucao['Dissertações'],
    name='Dissertações Defendidas', marker=dict(color='#FF5722')
))
fig_evolucao.update_layout(
    title='Evolução Nacional: Vagas Ofertadas vs Dissertações Defendidas por Ano',
    xaxis=dict(title='Ano', type='category'),
    yaxis_title='Quantidade',
    barmode='group',
    width=1300
)
fig_evolucao.write_html(caminho_saida_graficos / "grafico_evolucao_vagas_dissertacoes.html")

""" 2) Ranking das instituições com mais dissertações (top 20) """
top_instituicoes = (
    csv_dissertacao.groupby('Instituição Corrigida')
    .size()
    .rename('Dissertações')
    .reset_index()
    .sort_values('Dissertações', ascending=False)
    .head(20)
)

fig_ranking = px.bar(
    top_instituicoes.sort_values('Dissertações'),
    x='Dissertações', y='Instituição Corrigida',
    title='Top 20 Instituições com Mais Dissertações Defendidas',
    color='Dissertações',
    color_continuous_scale='Blues',
    width=1300
)
fig_ranking.update_layout(yaxis_title='Instituição', height=700)
fig_ranking.write_html(caminho_saida_graficos / "grafico_ranking_instituicoes.html")

""" 3) Crescimento da rede: nº de instituições com dissertações defendidas por ano """
instituicoes_por_ano = (
    csv_dissertacao.groupby('Ano Corrigido')['Instituição Corrigida']
    .nunique()
    .rename('Instituições Ativas')
    .reset_index()
    .sort_values('Ano Corrigido')
)

fig_crescimento = px.bar(
    instituicoes_por_ano, x='Ano Corrigido', y='Instituições Ativas',
    title='Crescimento da Rede PROFMAT: Instituições com Dissertações Defendidas por Ano',
    text='Instituições Ativas',
    width=1300
)
fig_crescimento.update_layout(xaxis=dict(type='category'), yaxis_title='Nº de Instituições')
fig_crescimento.update_traces(marker_color='#4CAF50', textposition='outside')
fig_crescimento.write_html(caminho_saida_graficos / "grafico_crescimento_rede.html")
