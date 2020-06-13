# Matemática Computacional I - parte A - Prova - Branch Esquerda - Fluxograma
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# 1o período 2020
# Autores: Denis Eiras
# 02/06/2020 - V1.0
#
#
# Descrição
#
# Utilizar os dados de casos diários do país Bolívia, entre 10/03 a 28/05 e executar as tarefas do fluxograma:
# - (plot 1) - Mostrar o histograma
# - (plot 2) - Identificar a classe estatística no espaço de Cullen-Frey
# - (plot 3) - Ajustar um PDF ao histograma
# - (plot 4) - Calcular o índice espectral Alfa via DFA
# - Estimar o Beta teórico via valor de Alfa
# - (plot 5) - Obter o espectro de singularidades  f(Alfa) x Alfa
# - Calcular Delta de Alfa e A de Alfa = (a0 - amin) / (amax - a0)
# - Plote uma tebela com os valores de Alfa, Beta, Delta de Alfa, a0 e A de Alfa
#
#
# Entradas:
#
# - instância da Classe DadosEntrada
#
# Saídas
#
# - (plot 1) - Figura contendo o histograma
# - (plot 2) - Plot para identificar a classe estatística no espaço de Cullen-Frey
# - (plot 3) - Figura contendo o ajuste de PDF ao histograma
# - (plot 4) - Figura com o cálculo do índice espectral Alfa via DFA
# - (plot 5) - Figura com o espectro de singularidades  f(Alfa) x Alfa
# - Saída no output: tabela com os valores de Alfa, Beta, Delta de Alfa, a0 e A de Alfa

import math

import matplotlib.pyplot as plt
import numpy as np

from Codigos.specplus import dfa1d
from Codigos.mfdfa_ss_m2 import getMSSByUpscaling
from Exercicio4.exercicio4_1 import graph
from Exercicio4.exercicio4_2_1 import plot_histograma_e_gev


def executa_branch_esquerda(d):

    # (plot 1) - Mostrar o histograma
    str_compl_titulo = '{} de COVID-19 de {}'.format(d.coluna_serie_covid.capitalize(), d.valor_coluna_agrupador)
    arr_valores = d.df_covid_pais_real[d.coluna_serie_covid].to_numpy()
    histogram, bins_edge = np.histogram(arr_valores, bins=20)
    width = 0.7 * (bins_edge[1] - bins_edge[0])
    center = (bins_edge[:-1] + bins_edge[1:]) / 2
    plt.bar(center, histogram, align='center', width=width)
    plt.title('Histograma da série {}'.format(str_compl_titulo))
    plt.xlabel("bin")
    plt.ylabel("Quantidade")
    plt.savefig("./plot_1_histograma.png")
    plt.show()

    # (plot 2) - Identificar a classe estatística no espaço de Cullen-Frey
    graph(arr_valores, boot=100)

    # (plot 3) - Ajustar um PDF ao histograma
    c = -1
    loc = 20
    scale = 20
    num_inicio = 0
    num_final = 850
    num_total = num_final - num_inicio
    plot_histograma_e_gev(
        str_compl_titulo,
        d.df_covid_pais_real, c, loc, scale, num_inicio, num_final, num_total,
        nome_coluna=d.coluna_serie_covid)

    # (plot 4) - Calcular o índice espectral Alfa via DFA
    alfa, vetoutput, x, y, reta, error = dfa1d(arr_valores, 1)
    fig = plt.figure()
    if not math.isnan(alfa):
        cor_dfa = 'darkmagenta'
        # DFA axes title:
        texto_dfax = '$log_{10}$ (s)'
        texto_dfay = '$log_{10}$ F(s)'
        texto_titulo_dfa = r'Detrended Fluctuation Analysis $\alpha$ = '

        # Plot DFA
        fig_dfa = fig.add_subplot()
        fig_dfa.plot(x, y, 's', color=cor_dfa, alpha=0.8)
        fig_dfa.plot(x, reta, '-', color=cor_dfa, linewidth=1.5)
        fig_dfa.set_title(texto_titulo_dfa + '%.4f' % alfa, loc='center')
        fig_dfa.set_xlabel(texto_dfax)
        fig_dfa.set_ylabel(texto_dfay)
        fig_dfa.grid()

    else:
        fig_dfa = fig.add_subplot()
        fig_dfa.set_title('Detrended Fluctuation Analysis $\alpha$ = ' + 'N.A.', loc='center')
        fig_dfa.grid()

    img_filename = './plot_4_alfa_dfa.png'
    fig.set_size_inches(10, 5)
    plt.savefig(img_filename, dpi=300, bbox_inches='tight', pad_inches=0.1)
    plt.show()

    # Estimar o Beta teórico via valor de Alfa
    beta_teorico = 2 * alfa - 1
    print('Beta teórico estimado = {}'.format(beta_teorico))

    # (plot 5) - Obter o espectro de singularidades  f(Alfa) x Alfa
    [_, _, _, stats, _] = getMSSByUpscaling(arr_valores.tolist(), isNormalised=1)
    # [_, _, _, stats, _] = getMSSByUpscaling(valores, isNormalised=0)
    plt.plot(stats['LH'], stats['f'], 'ko-')
    plt.title(
        'Espectro de singularidades.\n$\\alpha$0 = {:.2f} : $\\Delta$$\\alpha$ = {:.2f} : $\\psi$ = {:.2f}'
        ' : A$\\alpha$ = {:.2f}'.format(stats['alfa_0'], stats['delta_alfa'], stats['a_alfa'],
                                        stats['psi']))
    plt.xlabel(r'$\alpha$')
    plt.ylabel(r'$f(\alpha)$')
    plt.grid('on', which='major')
    plt.savefig('./plot_5_espectro_de_singularidades.png')
    plt.show()

    delta_alfa = stats['delta_alfa']
    alfa_0 = stats['alfa_0']
    a_alfa = stats['a_alfa']
    print('alfa_min = {}, alfa_max = {}'.format(stats['LH_min'], stats['LH_max']))

    # - Plote uma tebela com os valores de Alfa, Beta, Delta de Alfa, Alfa0 e A de Alfa
    print('Alfa\tBeta\tDelta_Alfa\tAlfa_0\tA_alfa')
    print('{}\t{}\t{}\t{}\t{}'.format(alfa, beta_teorico, delta_alfa, alfa_0, a_alfa))
