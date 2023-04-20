import numpy as np
import matplotlib.pyplot as plt
import psutil
from datetime import datetime
import time
import os
import paramiko
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
       query = f"INSERT INTO TabelaDeVibracoes (tempo, amplitude) VALUES ('{a}', {vibracao});"
       print(query)
       cursor.execute(query)
       dados_atuais()
    cnxn.commit()
    dados_atuais()


    # Plotando os dados simulados de vibração
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(eixo_tempo, vibracoes)
    dados_atuais()

    for intervalo in intervalos_vibracoes_altas:
        ax.axvspan(intervalo[0], intervalo[1], alpha=0.5, color='red')

    ax.axhline(y=valor_maximo, linestyle='--', color='red', label='Pode causar dano')
    ax.axhline(y=150, linestyle='--', color='orange', label='Limite de vibração')
    ax.set_xlabel('Tempo (s)')
    ax.set_ylabel('Amplitude (mm/s)')
    ax.set_title('Vibrações do caminhão de entregas')
    ax.legend()
    dados_atuais()
    
    #grafico tempo de execução em relação a memoria utilizada  
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(tempos, memorias)
    ax.set_xlabel('Tempo (s)')
    ax.set_ylabel('Memória utilizada (MB)')
    ax.set_title('Uso de memória durante a execução do algoritmo')

    fim = time.time()
    tempo_execucao = fim - inicio
    memoria_utilizada = psutil.Process().memory_info().rss / 1024 / 1024
    print(f'Tempo de execução: {tempo_execucao:.2f} segundos')
    print(f'Memoria utilizada: {memoria_utilizada} MB')

    tempo_x = [inicio, fim]
    tempo_y = [0, tempo_execucao]
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.plot(tempo_x, tempo_y, color='b')
    ax.set_xlim(inicio, fim)
    ax.set_xlabel('Tempo (s)')
    ax.set_ylabel('Tempo de execução (s)')
    ax.set_title('Desempenho do algoritmo')
    dados_atuais()

    plt.show()
    
    

    return intervalos_vibracoes_altas

import paramiko

def start_python_script_on_ec2(host, username, script_path, local_key_path):
    # Inicializa o cliente SSH
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Adiciona a chave privada do usuário para autenticação
    key = paramiko.RSAKey.from_private_key_file(local_key_path)
    
    # Conecta-se ao servidor remoto
    ssh.connect(hostname=host, username=username, pkey=key)

    # Executa o comando para inicializar o script Python
    stdin, stdout, stderr = ssh.exec_command(f'python3 {script_path}')

    # Lê a saída do comando
    output = stdout.read().decode()
    errors = stderr.read().decode()

    # Imprime a saída do comando
    print(output)
    print(errors)

    # Fecha a conexão SSH
    ssh.close()




simular_vibracoes_caminhao(valor_maximo=200, valor_minimo=0, variacao=20, duracao_tempo=60, frequencia_amostragem=10)

#maquina 1

# start_python_script_on_ec2(host='54.82.242.94', 
#                            username='ubuntu',
#                            script_path='./Desktop/GRUPO-5/Grupo_05/AA/algas_petterson_vibracao.py', 
#                            local_key_path='C:/Users/Aluno/Documents/CHAVE/CH-06042023.pem')


