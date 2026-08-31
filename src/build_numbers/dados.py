from pathlib import Path

import pandas as pd

diretorio_atual = Path(__file__).parent

caminho_csv_dissertacao = diretorio_atual.parent.parent / 'csv' / 'todas_as_dissertacoes.csv'
csv_dissertacao = pd.read_csv(caminho_csv_dissertacao)

caminho_csv_instituicao = diretorio_atual.parent.parent / 'csv' / 'instituicoes_profmat_classificadas.csv'
csv_instituicoes = pd.read_csv(caminho_csv_instituicao)

caminho_vagas = diretorio_atual.parent.parent / 'csv' / 'vagas_ofertadas-PROFMAT.csv'
csv_vagas = pd.read_csv(caminho_vagas)

# A linha "TOTAL DE VAGAS" do csv de vagas tem Sigla IES nula e é um
# somatório pré-calculado; sem removê-la ela duplica as contagens (bug do
# "Total Geral" contado em dobro).
csv_vagas = csv_vagas[csv_vagas['Sigla IES'].notna()]

colunas_anos = [col for col in csv_vagas.columns if col.isnumeric()]

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

regioes_fixas = sorted(csv_instituicoes['Região'].dropna().unique())

caminho_saida_graficos = diretorio_atual.parent.parent / 'docs' / 'numbers' / 'Graficos'
