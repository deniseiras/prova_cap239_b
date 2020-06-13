# Matemática Computacional I - parte B - Prova
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# 1o período 2020
# Autores: Denis Eiras
# 28/04/2020 - V1.0
#
# O programa é um utilitário que implementa a função ler_serie_generica_de_arquivo_ou_url, que permite ler um arquivo
# de uma série genérica, com diferentes tamanho
#
# Métodos utilizados:
#
# Bibliotecas pandas, para ler arquivos csv
# Bibliotecas python-magic e mimetypes para descobrir o tipo de arquivo com extensão genérica
#
# Entradas:
# - caminho e nome do arquivo
#
# Saídas:
#
# Array contendo série gerérica, sendo uma dimensão para cada coluna, ou um Pandas DataFrame.
#
# TODO - Ler JSON, XML, EXCEL

import numpy as np
import mimetypes
import pandas as pd
import magic
import os
from urllib.parse import urlparse
import requests


def ler_serie_generica_de_arquivo_ou_url(nome_arquivo_ou_url, is_url=False, is_obter_csv_como_dataframe=False):
    if is_url:
        a = urlparse(nome_arquivo_ou_url)
        nome_arquivo = os.path.basename(a.path)
        r = requests.get(nome_arquivo_ou_url, allow_redirects=True)
        with open(nome_arquivo, 'wb') as f:
            f.write(r.content)
    else:
        nome_arquivo = nome_arquivo_ou_url

    arr_serie = np.array([])
    print("Analisando arquivo: {}".format(nome_arquivo))

    if not os.path.exists(nome_arquivo):
        print("Arquivo {} não encontrado".format(nome_arquivo))
        return

    mimetypes.init()
    tipo_mime = mimetypes.guess_type(nome_arquivo)[0]
    tipo_arq = magic.from_file(nome_arquivo)

    if tipo_arq is None:
        print('Tipo de arquivo não reconhecido')
    else:
        print('Tipo do arquivo: {}'.format(tipo_arq))
        print('Mimetype do arquivo: {}'.format(tipo_mime))

        if 'ASCII text' in tipo_arq:

            if tipo_mime == 'text/csv':
                df_series = pd.read_csv(nome_arquivo)
                if is_obter_csv_como_dataframe:
                    arr_serie = df_series
                else:
                    arr_serie = np.array(df_series.values)

            elif tipo_mime == 'text/plain' or tipo_mime is None:
                print('Tentando gerar série de arquivo texto genérico')

                with open(nome_arquivo) as f:
                    try:
                        arr_primeira_linha_str = f.readline().split()
                        arr_primeira_linha = [float(x) for x in arr_primeira_linha_str]
                        arr_serie = converter_array_para_valor(arr_primeira_linha, arr_serie)
                    except:
                        print('Primeira linha é cabeçalho: {}'.format(arr_primeira_linha_str))

                    for arr_linha in f.readlines():
                        arr_linha = [float(x) for x in arr_linha.split()]
                        arr_serie = converter_array_para_valor(arr_linha, arr_serie)

        else:
            print("Não é um arquivo texto. Ainda não é possível abrir esse tipo de arquivo")

    return arr_serie


def converter_array_para_valor(arr_linha, arr_serie):
    # apenas uma coluna
    if len(arr_linha) == 1:
        arr_linha = np.array(arr_linha).flatten()[0]
    arr_serie = np.append(arr_serie, arr_linha)
    return arr_serie