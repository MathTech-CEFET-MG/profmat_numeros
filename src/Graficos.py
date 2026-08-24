from dis import print_instructions
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from pathlib import Path

from plotly import figure_factory

diretorio_atual = Path(__file__).parent

caminho_csv_dissertacao = diretorio_atual.parent / 'csv' / 'todas_as_dissertacoes.csv'
csv_dissertacao = pd.read_csv(caminho_csv_dissertacao)

caminho_csv_instituicao = diretorio_atual.parent / 'csv' / 'instituicoes_profmat_classificadas.csv'
csv_instituicoes = pd.read_csv(caminho_csv_instituicao)

caminho_vagas = diretorio_atual.parent / 'csv' / 'vagas_ofertadas-PROFMAT.csv'
csv_vagas = pd.read_csv(caminho_vagas)


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



contagem_por_ano_inst = csv_dissertacao.groupby(['Ano Corrigido', 'Instituição']).size().reset_index(name='Quantidade')

colunas_anos = [col for col in csv_vagas.columns if col.isnumeric()]

# O CSV de vagas traz uma linha extra no final ("TOTAL DE VAGAS", com
# Sigla IES e Cidade em branco) que já é a soma de todas as instituições.
# Se essa linha não for removida, o "Total Geral" do gráfico soma tudo
# duas vezes: uma vez linha a linha, e outra vez com essa linha pronta.
csv_vagas = csv_vagas[csv_vagas['Sigla IES'].notna()]

df_vagas_melt = csv_vagas.melt(
    id_vars=['Sigla IES', 'Cidade'],
    value_vars=colunas_anos,
    var_name='Ano',
    value_name='Vagas'
)
df_vagas_melt['Vagas'] = (
    pd.to_numeric(df_vagas_melt['Vagas'], errors='coerce')
    .replace(-1, float('nan'))
    .fillna(0)
)
df_vagas_melt['Ano'] = df_vagas_melt['Ano'].astype(int)
df_vagas_melt['Cidade'] = df_vagas_melt['Cidade'].replace(0, 'Total Geral')

df_dissertacoes_agrupado = csv_dissertacao.groupby(['Instituição', 'Ano Corrigido']).size().reset_index(
    name='Dissertações')
df_dissertacoes_agrupado = df_dissertacoes_agrupado.rename(columns={'Instituição': 'Sigla IES', 'Ano Corrigido': 'Ano'})

print(df_vagas_melt[df_vagas_melt['Ano'] == 2013].groupby('Cidade')['Vagas'].sum())
print('---')
print('Total:', df_vagas_melt[df_vagas_melt['Ano'] == 2013]['Vagas'].sum())
df_final = pd.merge(df_vagas_melt, df_dissertacoes_agrupado, on=['Sigla IES', 'Ano'], how='outer')

df_total_vagas = (
    df_vagas_melt[df_vagas_melt['Cidade'] != 'Total Geral']
    .groupby('Ano')['Vagas']
    .sum()
    .reset_index()
)
df_total_diss = (
    df_dissertacoes_agrupado.groupby('Ano')['Dissertações']
    .sum()
    .reset_index()
)

df_total = pd.merge(df_total_vagas, df_total_diss, on='Ano', how='outer')
df_total['Vagas'] = df_total['Vagas'].fillna(0)
df_total['Dissertações'] = df_total['Dissertações'].fillna(0)
df_total['Sigla IES'] = 'Total Geral'
df_total['Cidade'] = 'Geral'

df_final = pd.concat([df_final, df_total], ignore_index=True)

df_final = df_final[df_final['Sigla IES'].notna()]
df_final['Sigla IES'] = df_final['Sigla IES'].astype(str)
df_final = df_final[df_final['Sigla IES'] != 'nan']

# Total Geral primeiro, resto em ordem alfabética
instituicoes_raw = sorted(df_final['Sigla IES'].unique())
instituicoes = ['Total Geral'] + [i for i in instituicoes_raw if i != 'Total Geral']  # agora só strings

fig = go.Figure()

cores_polo = ['#2196F3', '#4CAF50', '#FF5722', '#9C27B0', '#FF9800', '#00BCD4']
traces_por_inst = {}  # inst -> {'diss_index': int, 'polos': {label_polo: trace_index}}

for inst in instituicoes:
    df_inst = df_final[df_final['Sigla IES'] == inst]
    cidades_disponiveis = sorted(df_inst['Cidade'].dropna().astype(str).unique())

    # Se não tiver cidade (ex: Total Geral), tem só uma linha "Geral"
    if len(cidades_disponiveis) == 0:
        df_inst = df_inst.copy()
        df_inst['Cidade'] = 'Geral'
        polos = ['Geral']
    else:
        # Opções do dropdown de polo: soma geral, comparativo entre polos, e cada polo individual
        polos = ['Total (todos os polos)', 'Comparar todos os polos'] + cidades_disponiveis

    polos_indices = {}  # label -> índice de trace (só para opções de UMA linha)
    cidades_traces = []  # índices das linhas de cada polo individual, p/ opção "Comparar"

    for j, polo in enumerate(polos):
        if polo == 'Comparar todos os polos':
            # Não gera uma trace própria: essa opção reaproveita as linhas de cada polo
            continue
        elif polo == 'Total (todos os polos)':
            df_polo = df_inst.groupby('Ano', as_index=False)['Vagas'].sum().sort_values('Ano')
        else:
            df_polo = df_inst[df_inst['Cidade'] == polo].sort_values('Ano')

        fig.add_trace(go.Bar(
            x=df_polo['Ano'],
            y=df_polo['Vagas'],
            name=f'Vagas — {polo}',
            marker=dict(color=cores_polo[j % len(cores_polo)]),
            visible=False
        ))
        polos_indices[polo] = len(fig.data) - 1
        if polo not in ('Total (todos os polos)',):
            cidades_traces.append(len(fig.data) - 1)

    # Uma linha de dissertações totais da instituição (sem polo), sempre junto com o polo escolhido
    df_diss_inst = (
        df_dissertacoes_agrupado[df_dissertacoes_agrupado['Sigla IES'] == inst]
        .sort_values('Ano')
    )

    fig.add_trace(go.Bar(
        x=df_diss_inst['Ano'],
        y=df_diss_inst['Dissertações'],
        name='Dissertações (total)',
        marker=dict(color='black'),
        visible=False
    ))
    diss_index = len(fig.data) - 1

    traces_por_inst[inst] = {
        'diss_index': diss_index,
        'polos': polos,  # ordem das opções do dropdown (inclui "Comparar todos os polos")
        'polos_indices': polos_indices,
        'cidades_traces': cidades_traces
    }

total_traces = len(fig.data)


def visibilidade_para(inst, polo):
    """Vetor de visibilidade para uma opção do dropdown de polo.

    - 'Comparar todos os polos': mostra a linha de cada polo individual junto.
    - Qualquer outra opção: mostra só aquela linha (+ dissertações da instituição).
    """
    info = traces_por_inst[inst]
    visibilidade = [False] * total_traces

    if polo == 'Comparar todos os polos':
        for idx in info['cidades_traces']:
            visibilidade[idx] = True
    else:
        visibilidade[info['polos_indices'][polo]] = True

    visibilidade[info['diss_index']] = True
    return visibilidade


def botoes_menu_polo(inst):
    """Gera os botões do 2º dropdown (polo) para uma instituição específica."""
    info = traces_por_inst[inst]
    return [
        dict(
            label=polo,
            method='update',
            args=[
                {'visible': visibilidade_para(inst, polo)},
                {'title.text': f'Vagas ({polo}) vs Dissertações: {inst}'}
            ]
        )
        for polo in info['polos']
    ]


# Botões do 1º dropdown (instituição). Ao trocar de instituição, também
# reconstrói as opções do 2º dropdown (polo) para essa instituição.
botoes_instituicao = []
for inst in instituicoes:
    primeiro_polo = traces_por_inst[inst]['polos'][0]

    botoes_instituicao.append(dict(
        label=inst,
        method='update',
        args=[
            {'visible': visibilidade_para(inst, primeiro_polo)},
            {
                'title.text': f'Vagas ({primeiro_polo}) vs Dissertações: {inst}',
                'updatemenus[1].buttons': botoes_menu_polo(inst),
                'updatemenus[1].active': 0
            }
        ]
    ))

# Ativar a primeira instituição / primeiro polo por padrão
inst_inicial = instituicoes[0]
polo_inicial = traces_por_inst[inst_inicial]['polos'][0]
for idx, visivel in enumerate(visibilidade_para(inst_inicial, polo_inicial)):
    fig.data[idx].visible = visivel

# Configurar o layout e posicionar os dois menus dropdown
fig.update_layout(
    updatemenus=[
        dict(
            active=0,
            buttons=botoes_instituicao,
            x=0.0,
            xanchor="left",
            y=1.08,
            yanchor="bottom",
            direction="down"
        ),
        dict(
            active=0,
            buttons=botoes_menu_polo(inst_inicial),
            x=0.25,
            xanchor="left",
            y=1.08,
            yanchor="bottom",
            direction="down"
        )
    ],
    title=dict(
        text=f'Vagas ({polo_inicial}) vs Dissertações: {inst_inicial}',
        x=0.5,
        xanchor='center',
        y=0.98,
        yanchor='top'
    ),
    margin=dict(t=160),
    barmode='group',
    xaxis=dict(title="Ano", type='category'),
    yaxis_title="Quantidade",
    width=1300
)
print(df_vagas_melt[df_vagas_melt['Sigla IES'] == 'CEFET'].to_string())
fig.write_html("../docs/numbers/Graficos/grafico_vagas_vs_dissertacoes.html")

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
fig_evolucao.write_html("../docs/numbers/Graficos/grafico_evolucao_vagas_dissertacoes.html")

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
fig_ranking.write_html("../docs/numbers/Graficos/grafico_ranking_instituicoes.html")

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
fig_crescimento.write_html("../docs/numbers/Graficos/grafico_crescimento_rede.html")

regioes_fixas = sorted(csv_instituicoes['Região'].dropna().unique())

""" 4) Distribuição de vagas ofertadas por Região, com dropdown de ano """
vagas_com_regiao = (
    df_vagas_melt[df_vagas_melt['Cidade'] != 'Total Geral']
    .merge(csv_instituicoes[['Sigla', 'Região']], left_on='Sigla IES', right_on='Sigla', how='left')
)
vagas_com_regiao = vagas_com_regiao[vagas_com_regiao['Região'].notna()]

anos_vagas_disponiveis = sorted(vagas_com_regiao['Ano'].unique())
opcoes_ano_pizza = ['Todos os Anos'] + anos_vagas_disponiveis


def valores_pizza_regiao(ano):
    dados = vagas_com_regiao if ano == 'Todos os Anos' else vagas_com_regiao[vagas_com_regiao['Ano'] == ano]
    soma = dados.groupby('Região')['Vagas'].sum()
    return [float(soma.get(r, 0)) for r in regioes_fixas]


fig_vagas_regiao = go.Figure(data=[go.Pie(
    labels=regioes_fixas,
    values=valores_pizza_regiao('Todos os Anos')
)])

botoes_pizza = []
for opcao in opcoes_ano_pizza:
    label_botao = 'Todos os Anos' if opcao == 'Todos os Anos' else str(opcao)
    botoes_pizza.append(dict(
        label=label_botao,
        method='update',
        args=[
            {'values': [valores_pizza_regiao(opcao)]},
            {'title.text': f'Distribuição de Vagas Ofertadas por Região ({label_botao})'}
        ]
    ))

fig_vagas_regiao.update_layout(
    updatemenus=[dict(
        active=0, buttons=botoes_pizza,
        x=0.5, xanchor='center', y=1.15, yanchor='top', direction='down'
    )],
    title=dict(
        text='Distribuição de Vagas Ofertadas por Região (Todos os Anos)',
        x=0.5, xanchor='center', y=0.98, yanchor='top'
    ),
    margin=dict(t=160),
    width=900, height=650
)
fig_vagas_regiao.write_html("../docs/numbers/Graficos/grafico_vagas_por_regiao_pizza.html")

