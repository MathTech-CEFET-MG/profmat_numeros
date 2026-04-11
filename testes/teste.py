import plotly.express as px
import pandas as pd
import numpy as np

df = pd.read_csv('https://raw.githubusercontent.com/MathTech-CEFET-MG/profmat_numeros/refs/heads/main/csv/teste_atualizado.csv')

instituicao_counts_df = df.groupby('Instituição Corrigida').size().rename('Contagem').reset_index()

px.bar(instituicao_counts_df, x='Instituição Corrigida', y='Contagem',
       title='Frequência de Ocorrências por Instituição',
       color = 'Instituição Corrigida', width= 1300)
