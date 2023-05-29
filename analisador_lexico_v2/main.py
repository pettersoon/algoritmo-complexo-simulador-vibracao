'''
   NÃO MODIFIQUE ESTE ARQUIVO - autor MAC0122

   Este arquivo contem o programa principal do projeto.
'''
from wordcloud import WordCloud

import matplotlib.pyplot as plt

# tk.tokeniza(), 
import tokeniza as tk

# categorias e dicionario "categoria: decrição" 
import operadores as op

PROMPT = "expressão >>> "
QUIT   = ''

#------------------------------------------------------------
def adicionar_variavel_manualmente():
    '''None -> None

    Programa que lê do teclado uma expressão aritmética 
    e imprime cada item léxico na expressão.

    Exemplos:

    
    '''
    print("Entre como uma expressão ou tecle apenas ENTER para encerrar.") 
    expressao = input(PROMPT)
    while expressao != QUIT:
        lista_tokens = tk.tokeniza(expressao)
        for token in lista_tokens:
            # pegue item e tipo
            item, tipo = token

            # cri string com a descriçao
            if tipo in [tk.OPERADOR, tk.PARENTESES]:
                descricao = "'%s' : %s" %(item,op.DESCRICAO[item])
            elif tipo == tk.VARIAVEL:
                descricao = "'%s' : nome de variável" %item
            elif tipo == tk.NUMERO:
                descricao = "%f : constante float" %item
            elif tipo == tk.SEPARADOR:
                descricao = "'%s' : separação para coesão da frase" %item
            else:
                descricao = "'%s' : categoria desconhecida" %item

            # imprima a descriçao
            print(descricao)
        # leia próxima expressão    
        expressao = input(PROMPT)        


def ler_arquivos_txt_automatico(caminho):
    '''None -> None

    Programa que lê do teclado uma expressão aritmética 
    e imprime cada item léxico na expressão.

    Exemplos:

    
    '''
    palavras = []
    with open(str(caminho), "r", encoding="utf-8", newline="") as fp:
        line = fp.read()
        print(line)
        while line:
            lista_tokens = tk.tokeniza(line.lower())
            for token in lista_tokens:
                # pegue item e tipo
                item, tipo = token

                # cri string com a descriçao
                if tipo in [tk.OPERADOR, tk.PARENTESES]:
                    descricao = "'%s' : %s" %(item,op.DESCRICAO[item])
                elif tipo == tk.VARIAVEL:
                    if(len(item) >= 4):
                        palavras.append(item)
                    descricao = "'%s' : nome de variável" %item
                elif tipo == tk.NUMERO:
                    descricao = "%f : constante float" %item
                elif tipo == tk.SEPARADOR:
                    descricao = "'%s' : separação para coesão da frase" %item
                else:
                    descricao = "'%s' : categoria desconhecida" %item

                # imprima a descriçao
                print(descricao)
                line = fp.readline()
    return palavras

def removendo_conectores(list_string : list):
    # Palavras que são utilizadas como conectoresw nas frases 
    # list_conectores = ['de','o','da','ter','um','em','que','é','por','ser','vai','e','a','u','i','para','tem','até','lá','os']
    list_conectores = ['pode','mais','isso','pela','para','estão','quem','quer','pelo','onde','muito','essa']

    # Utilizei no web-scrapping #rodovia, #carros e #estradas então retirei esses valores para o word cloud ser mais preciso 
    list_conectores.append('carro')
    list_conectores.append('rodovia')
    list_conectores.append('rodovias')
    list_conectores.append('estrada')
    list_conectores.append('estradas')

    for word in list_conectores:
        for i in list_string:
            if word == i:
                list_string.remove(word)
    return list_string


def gerar_word_cloud(caminho):
    list_word = ler_arquivos_txt_automatico(caminho)
    list_word = removendo_conectores(list_word)

    unique_string=(" ").join(word for word in list_word)
    word_cloud = WordCloud(collocations = False, background_color = 'white').generate(unique_string)
    plt.figure(figsize=(15,8))
    plt.imshow(word_cloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()
    plt.close()

#-------------------------------------------
# início da execução do programa manualmente
# adicionar_variavel_manualmente()


#-------------------------------------------
# início da execução do programa manualmente
gerar_word_cloud("./tweets-tt.txt")
