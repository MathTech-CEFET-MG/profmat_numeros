import plotly.graph_objects as go

from dados import df_vagas_melt, csv_instituicoes, regioes_fixas, caminho_saida_graficos

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
fig_vagas_regiao.write_html("../../docs/numbers/Graficos/grafico_vagas_por_regiao_pizza.html")
