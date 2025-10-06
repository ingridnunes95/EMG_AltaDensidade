"""
Código para leitura de sinais fisiológicos, extração de atributos e criação
de um arquivo .arff

"""

# importando as bibliotecas
import extracao_atributos as ext
import geraARFF
import pandas as pd
import numpy as np
import os

"""
VARIÁVEIS:

* Y - sinal
Para Y(i,j), i deve ser o sinal no tempo e j os canais do EEG

* Xf - sinal após o janelamento
* Fs - frequencia de amostragem do sinal 
* janela - tamanho da janela em s
* superposição - superposição da janela em s
* n_canais - numero de canais do sinal 
* n_sinal - numero de sinais que precisam ser carregados
* Classe - classe do sinal que se encontra em carregamento 

"""

# Arquivos que serão lidos

file_names = []

all_files = os.listdir(r"C:\Users\Ingrid Nunes\Downloads\estudos_EMG\CodigosPython\arq")
csv_files = list(filter(lambda f: f.endswith('.csv'), all_files)) #chama os arquivos no diretório

file_names = csv_files
file_names.sort(key=lambda x: os.path.getmtime(x)) #ordena os arquivos de acordo com a data de modificação no diretório

print(file_names)

""" parâmetros iniciais """
NumFiles = len(file_names)  # número de arquivos
Fs = 2048  # frequência de amostragem
janela = 0.25  # tempo em segundos
superposicao = 0.125
n_canais = 256
classes = [7,7,8,8,9,9,10,10,7,7,8,8,9,9,10,10,7,7,8,8,9,9,10,10,7,7,8,8,9,9,10,10,7,7,8,8,9,9,10,10,7,7,8,8,9,9,10,10,7,7,8,8,9,9,10,10,7,7,8,8,9,9,10,10,7,7,8,8,9,9,10,10,7,7,8,8,9,9,10,10,7,7,8,8,9,9,10,10,7,7,8,8,9,9,10,10,7,7,8,8,9,9,10,10,7,7,8,8,9,9,10,10,7,7,8,8,9,9,10,10,7,7,8,8,9,9,10,10,7,7,8,8,9,9,10,10,7,7,8,8,9,9,10,10,7,7,8,8,9,9,10,10,7,7,8,8,9,9,10,10,7,7,8,8,9,9,10,10,7,7,8,8,9,9,10,10,7,7,8,8,9,9,10,10,7,7,8,8,9,9,10,10,7,7,8,8,9,9,10,10,7,7,8,8,9,9,10,10,7,7,8,8,9,9,10,10,7,7,8,8,9,9,10,10,7,7,8,8,9,9,10,10,7,7,8,8,9,9,10,10,8,8,9,9,10,10,7,7,8,8,9,9,10,10,7,7,8,8,9,9,10,10,7,7,8,8,9,9,10,10,7,7,8,8,9,9,10,10,7,7,8,8,9,9,10,10,7,7,8,8,9,9,10,10,7,7,8,8,9,9,10,10,7,7,8,8,9,9,10,10]  # quantidade de arquivos de cada classe!!!
arquivo_final = os.path.join(os.getcwd(), "atributosExplicitosEMG_4classes.arff")

""" vetores inicializados """
atributos_total = np.array([])  # inicializando vetor com os atributos + classes

for sinal in range(0, NumFiles):

    # carrega o sinal
    Y = pd.read_csv(file_names[sinal], delimiter=",").values  # lê o sinal em txt e armazena na matriz Y
    # caso o arquivo do sinal não esteja no formato .txt ou .csv, essa parte do código deve ser modificada

    # selecionando os canais de interesse
    # ATENÇÃO: lembrar que, em Python, a contagem começa do zero!!!!!!!!!!!
   # Y = np.concatenate((Y[:, 0:32], Y[:, 32:35], Y[:, 40:41], Y[:, 44:46]), axis=1)

    # Extração de atributos
    atributos = ext.ExtrairAtributos(Y, Fs, janela, superposicao, n_canais)
    [l, c] = atributos.shape

    classe = classes[sinal]  # capturando a classe referente ao sinal
    vetor_classe = np.full((l, 1), classe)  # criando uma lista para armazenar a classe do sinal
    atributos = np.concatenate((atributos, vetor_classe), axis=1)

    if sinal == 0:
        atributos_total = atributos
    else:
        atributos_total = np.concatenate((atributos_total, atributos), axis=0)


# gerando o arquivo .arff para os experimentos
geraARFF.base_arff(atributos_total, arquivo_final)