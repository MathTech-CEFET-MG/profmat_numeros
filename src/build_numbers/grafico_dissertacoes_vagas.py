import plotly.graph_objects as go
import pandas as pd

from dados import df_vagas_melt, df_dissertacoes_agrupado, df_total, caminho_saida_graficos

df_final = pd.merge(df_vagas_melt, df_dissertacoes_agrupado, on=['Sigla IES', 'Ano'], how='outer')

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
fig.write_html("../../docs/numbers/Graficos/grafico_vagas_vs_dissertacoes.html")