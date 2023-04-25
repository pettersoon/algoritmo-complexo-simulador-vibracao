import numpy as np
import matplotlib.pyplot as plt
import psutil
from datetime import datetime
import time
import pyodbc

def simular_vibracoes_caminhao(valor_maximo, valor_minimo, variacao, duracao_tempo, frequencia_amostragem):
    def dados_atuais():
        tempo_atual = time.time() - inicio
        tempos.append(tempo_atual)
        memoria_atual = psutil.Process().memory_info().rss / 1024 / 1024
        memorias.append(memoria_atual)
        
    inicio = time.time()
    num_amostras = duracao_tempo * frequencia_amostragem
    eixo_tempo = np.linspace(0, duracao_tempo, num_amostras)
    tempos = []
    memorias = []
    dados_atuais()

    # Simulando os dados de vibração do caminhão
    frequencia = 10  # Hz (frequência constante)
    amplitude = (valor_maximo + valor_minimo) / 2
    x = amplitude * np.sin(2 * np.pi * frequencia * eixo_tempo)
    dados_atuais()

    probabilidade_alta = 0.01  # probabilidade de uma vibração alta ocorrer
    vibracoes_baixas = np.random.uniform(valor_minimo, valor_maximo, size=num_amostras)
    vibracoes_altas = np.random.uniform(valor_maximo, valor_maximo + variacao, size=num_amostras)
    prob_vibracoes_altas = np.random.uniform(size=num_amostras)
    dados_atuais()

    # Adicionando os dados de vibração alta onde a probabilidade é maior que o limiar
    vibracoes = np.where(prob_vibracoes_altas < probabilidade_alta, vibracoes_altas.astype(float), vibracoes_baixas.astype(float))
    dados_atuais()

    # Gerando os intervalos de tempo em que ocorrem as vibrações altas
    intervalos_vibracoes_altas = []
    inicio_intervalo = None
    for i in range(num_amostras):
        if vibracoes[i] > valor_maximo:
            if inicio_intervalo is None:
                inicio_intervalo = i
        else:
            if inicio_intervalo is not None:
                intervalos_vibracoes_altas.append((inicio_intervalo / frequencia_amostragem, i / frequencia_amostragem))
                inicio_intervalo = None
    if inicio_intervalo is not None:
        intervalos_vibracoes_altas.append((inicio_intervalo / frequencia_amostragem, num_amostras / frequencia_amostragem))
    dados_atuais()

    # Insere os dados no banco de dados na Azure
    cnxn = pyodbc.connect('Driver={ODBC Driver 18 for SQL Server};Server=tcp:simulador.database.windows.net,1433;Database=vibrations;Uid=petterson.viturino@bandtec.com.br@simulador;Pwd={#Gf46492782879};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    cursor = cnxn.cursor()
    for vibracao in vibracoes:
       a = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
       query = f"INSERT INTO TabelaDeVibracoes_ec2_1 (tempo, amplitude) VALUES ('{a}', '{vibracao}');"
       print(query)
       cursor.execute(query)
       dados_atuais()
    cnxn.commit()
    dados_atuais()

    fim = time.time()
    tempo_execucao = fim - inicio
    memoria_utilizada = psutil.Process().memory_info().rss / 1024 / 1024
    print(f'Tempo de execução: {tempo_execucao:.2f} segundos')
    print(f'Memoria utilizada: {memoria_utilizada} MB')
    
    cnxn = pyodbc.connect('Driver={ODBC Driver 18 for SQL Server};Server=tcp:simulador.database.windows.net,1433;Database=vibrations;Uid=petterson.viturino@bandtec.com.br@simulador;Pwd={#Gf46492782879};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    cursor = cnxn.cursor()
    query = f"INSERT INTO TabelaDeTempoExecucao_ec2_1 (tempo_execucao, memoria_utilizada) VALUES ({tempo_execucao:.2f},{memoria_utilizada});"
    print(query)
    cursor.execute(query)
    cnxn.commit()
    dados_atuais()

    return intervalos_vibracoes_altas

simular_vibracoes_caminhao(valor_maximo=200, valor_minimo=0, variacao=20, duracao_tempo=60, frequencia_amostragem=10)


