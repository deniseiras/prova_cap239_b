# Matemática Computacional I - parte B - Prova parte A - Programa principal
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# 1o período 2020
# Autores: Denis Eiras
# 02/06/2020 - V1.0
#
#
# Descrição
#
# O código abaixo implementa a programa principal, que lê os dados de número de casos diários da COVID para a Bolívia
# e executa os branchs da esquerda e da direita
#
# Entradas:
#
# - N: (Inteiro) - Número de dias de previsão
# - prob_agent: (Dicionario: {String: Array de Floats}: Dicionário para configuração dos espectros de probabilidade.
# - coluna_agrupadora_covid: (String) = nome da coluna para agrupar a série. Ex. 'location'
# - coluna_serie_covid: (String) Nome da coluna da série, ex:  'new_cases'
# - valor_coluna_agrupador: (String) Valor da coluna agrupadora. Ex: 'Bolivia'
# - coluna_data: (String) Nome da coluna que contém a data. Ex: 'date'
# - data_inicial: (String) Data inicial da serie. Ex: '2020-05-09'
# - num_dias_para_media: (Inteiro) Número de dias de média a ser considerada para inicialização do modelo
# - data_inicial_previsao: (String) Data Inicial de previsão. Ex: '2020-05-16'
# - data_final: (String) Data final de dados Reais. Ex: '2020-06-05'
# - estrategia_g: (String) Estrategia a ser usada para cálculo de g na previsão:
#     - 'Media' - Estratégia padrão, conforme modelo da prova
#     - 'Fixo'  - Valor fixo para g. O valor é determinado no parâmetro 'g_fixo'
#     - 'Ajuste'- Estratégia desenvolvida que utiliza o valor médio entre os mínimos e máximos calculados para prever g.
# - g_fixo = 0.25
#   Ex = {'Espectro 1': [0.5, 0.45, 0.05], 'Espectro 2': [0.7, 0.25, 0.05]}
# - fator_n_min: (Array de Floats) Fatores "n" mínimos. Ex = [2.0, 4.0, 5.0]
# - fator_n_max: (Array de Floats) Fatores "n" máximos. Ex = [4.0, 7.0, 10.0]
# - is_atualizar_arquivo_covid: (Boolean) True para atualizar o arquivo da covid da url do parâmetro
#   'url_owid_covid_data'
# - url_owid_covid_data: : (String) Url para baixar arquivo da COVID.
#   Ex:'https://covid.ourworldindata.org/data/owid-covid-data.csv'
# - nome_arq_covid_completo: (String) Nome do arquivo da covid a salvar. Ex: './owid-covid-data.csv'
#
# Saídas
#
# Branch esquerda
#
#
# Branch direita
#
# - Uma figura contendo o fator de supressão e o fator g, dos espectros definidos
# - Uma figura para cada espectro de probabilidades, contendo as previsões, os dados observados e as médias
#


import pandas as pd
import datetime

# início do programa principal
from Exercicio4.exercicio4_2_2 import ler_serie_generica_de_arquivo_ou_url
from Prova.prova_fluxograma import executa_branch_esquerda
from Prova.prova_modelo_covid import executa_branch_direita


class DadosEntrada:
    coluna_agrupadora_covid = 'location'
    coluna_serie_covid = 'new_cases'
    coluna_data = 'date'
    valor_coluna_agrupador = 'Bolivia'
    num_dias_para_media = 7
    data_inicial = '2020-03-10'
    data_final = '2020-05-28'
    # dias de previsão
    N = 20
    data_inicial_previsao = '2020-03-10'
    # Estratégias => Media, Fixo, Ajuste
    estrategia_g = 'Media'
    # Estratégias => Media , Fixo, Ajuste. Média faz mais sentido com casos reais
    estrategia_g_inicializacao = 'Media'
    g_fixo = 0.25
    g0 = 0.2  # 0.2 0.5 0.8
    prob_agent = {'Espectro 1': [0.5, 0.45, 0.05], 'Espectro 2': [0.7, 0.25, 0.05]}
    fator_n_min = [2.0, 4.0, 5.0]
    fator_n_max = [4.0, 7.0, 10.0]
    is_atualizar_arquivo_covid = False
    url_owid_covid_data = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
    # nome arquivo covid a salvar
    nome_arq_covid_completo = './owid-covid-data.csv'
    df_covid_pais_real = None


def filtra_e_insere_datas_faltantes(dados_, df_covid_pais):
    df_covid_pais_date = pd.DataFrame()
    df_covid_pais_date[dados_.coluna_data] = pd.to_datetime(df_covid_pais[dados_.coluna_data])

    mascara_data = (df_covid_pais_date[dados_.coluna_data] >= dados_.data_inicial) & (
            df_covid_pais_date[dados_.coluna_data] <= dados_.data_final)
    dados_.df_covid_pais_real = df_covid_pais.loc[mascara_data]

    # insere datas faltantes
    dates_list = pd.date_range(start=dados_.data_inicial, end=dados_.data_final)
    df_dates = pd.DataFrame(dates_list, columns=["date"])
    df_dates[dados_.coluna_agrupadora_covid] = dados_.valor_coluna_agrupador
    df_dates[dados_.coluna_serie_covid] = 0
    for index_c, row_c in dados_.df_covid_pais_real.iterrows():
        for index, row in df_dates.iterrows():
            date_time_str = row_c[dados_.coluna_data]
            date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d')
            if row[dados_.coluna_data] < date_time_obj:
                continue
            elif date_time_obj == row[dados_.coluna_data]:
                df_dates.at[index, dados_.coluna_agrupadora_covid] = row_c[dados_.coluna_agrupadora_covid]
                df_dates.at[index, dados_.coluna_serie_covid] = row_c[dados_.coluna_serie_covid]
                break
    dados_.df_covid_pais_real = df_dates


def get_dados_covid_por_agrupador(dados_):
    # obtém dados da covid e atualiza se especificado
    if dados_.is_atualizar_arquivo_covid:
        df_covid_completo = ler_serie_generica_de_arquivo_ou_url(dados_.url_owid_covid_data,
                                                                 is_obter_csv_como_dataframe=True,
                                                                 is_url=True)
    else:
        df_covid_completo = ler_serie_generica_de_arquivo_ou_url(dados_.nome_arq_covid_completo,
                                                                 is_obter_csv_como_dataframe=True)
    # seleciona por agrupador (Ex. location)
    df_covid_completo = df_covid_completo[[dados_.coluna_agrupadora_covid, dados_.coluna_data, dados_.coluna_serie_covid]]
    is_pais = df_covid_completo[dados_.coluna_agrupadora_covid] == dados_.valor_coluna_agrupador
    df_covid_pais = df_covid_completo[is_pais]

    filtra_e_insere_datas_faltantes(dados_branch_esq, df_covid_pais)


if __name__ == '__main__':

    # Parâmetros de entrada padrão para a branch esquerda
    dados_branch_esq = DadosEntrada()

    # Parâmetros para a branch direita
    dados_branch_dir = DadosEntrada()
    dados_branch_dir.data_inicial = '2020-03-03'
    dados_branch_dir.data_inicial_previsao = '2020-03-10'
    dados_branch_dir.data_final = '2020-05-28'

    # branch esquerda
    get_dados_covid_por_agrupador(dados_branch_esq)
    executa_branch_esquerda(dados_branch_esq)

    # branch direita
    # get_dados_covid_por_agrupador(dados_branch_dir)
    # executa_branch_direita(dados_branch_dir)
