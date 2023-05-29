import pyodbc
import csv
import requests

query = 'SELECT TOP 100 * FROM TabelaDeVibracoes_ec2_2 order by id desc;'

csv_filename = 'resultado.csv'

# Colocar sua connection string 
conn = pyodbc.connect('Driver={ODBC Driver 18 for SQL Server};Server=tcp:simulador.database.windows.net,1433;Database=vibrations;Uid=petterson.viturino@bandtec.com.br@simulador;Pwd={#Gf46492782879};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')

# Executa a consulta SQL
cursor = conn.cursor()
cursor.execute(query)

# Recupera os resultados da consulta
results = cursor.fetchall()

# Obtém os nomes das colunas
column_names = [column[0] for column in cursor.description]

# Exporta os resultados para um arquivo CSV
with open(csv_filename, 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    
    # Escreve os nomes das colunas no arquivo CSV
    writer.writerow(column_names)
    
    # Escreve cada linha de resultado no arquivo CSV
    writer.writerows(results)

print(f"Os resultados foram exportados para o arquivo {csv_filename}.")

# Fecha a conexão com o banco de dados
conn.close()


import requests

url = 'https://qu20rsf5mc.execute-api.us-east-1.amazonaws.com/marise/vibration-raw-dev-pett/resultado.csv'  # URL do endpoint para onde o arquivo será enviado
arquivo = r'C:\Users\petiv\OneDrive\Documentos\Grupo_05\AA\algoritmo-complexo-simulador-vibracao\resultado.csv'  # Caminho do arquivo que será enviado

# Configurar os cabeçalhos da requisição (opcional)
headers = {'Content-Type': 'application/octet-stream'}

# Ler o conteúdo do arquivo
with open(arquivo, 'rb') as f:
    conteudo = f.read()

# Enviar a requisição PUT com o conteúdo do arquivo
response = requests.put(url, data=conteudo, headers=headers)

# Verificar a resposta do servidor
if response.status_code == 200:
    print('Arquivo enviado com sucesso!')
else:
    print('Erro ao enviar o arquivo:', response.status_code)