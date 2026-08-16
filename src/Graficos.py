from dis import print_instructions
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from pathlib import Path

from plotly import figure_factory

diretorio_atual = Path(__file__).parent

caminho_csv_dissertacao = diretorio_atual.parent / 'csv' / 'teste_atualizado.csv'
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

