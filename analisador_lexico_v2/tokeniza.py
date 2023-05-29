
# Constantes
TESTE   = False

# caracteres usados em operadores
OPERADORES = "%*/+-!^="

# caracteres usados em números inteiros
DIGITOS = "0123456789"

# ponto decimal
PONTO = "."
PONTO_E_VIRGULA = ";"

# todos os caracteres usados em um números float
FLOATS = DIGITOS + PONTO

# caracteres usados em nomes de variáveis
LETRAS  = "_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZáãàâçéèêóòôõíìîóòõôúùû"

# abre e fecha parenteses
ABRE_FECHA_PARENTESES = "()"

# categorias
OPERADOR   = 1 # para operadores aritméticos e atribuição
NUMERO     = 2 # para números: todos são considerados float
VARIAVEL   = 3 # para variáveis
PARENTESES = 4 # para '(' e ')
SEPARADOR = 5
NAO_ENCONTRADO = 6

# Whitespace characters: space, newline, horizontal tab,
# vertical tab, form feed, carriage return
BRANCOS    = [' ', '\n', '\t', '\v', '\f', '\r']

# caractere que indica comentário
COMENTARIO = "#"


#------------------------------------------------------------
def tokeniza(exp):
    """(str) -> list

    Recebe uma string exp representando uma expressão e cria 
    e retorna uma lista com os itens léxicos que formam a
    expressão.

    Cada item léxico (= token) é da forma
       
        [item, tipo]

    O componente item de um token é 

        - um float: no caso do item ser um número; ou 
        - um string no caso do item ser um operador ou 
             uma variável ou um abre/fecha parenteses.

    O componente tipo de um token indica a sua categoria
    (ver definição de constantes acima). 

        - OPERADOR;
        - NUMERO; 
        - VARIAVEL; ou 
        - PARENTESES

    A funçao ignora tuo que esta na exp apos o caractere
    COMENTARIO (= "#").
    """
    resultado = []
    variavel_sep = []
    numero_completo = []
    # exp = ''.join(exp.split(" "))
    for index, i in enumerate(exp):
        if i in COMENTARIO:
            break
        if i in LETRAS:
            variavel_sep.append(i)
            if index+1 == len(exp):
                variavel_com = ''.join(variavel_sep)
                resultado.append([variavel_com, VARIAVEL])
                variavel_sep = []
                continue
            if exp[index+1] in DIGITOS:
                variavel_sep.append(exp[index+1])
            if exp[index+1] not in LETRAS:
                variavel_com = ''.join(variavel_sep)
                resultado.append([variavel_com, VARIAVEL])
                variavel_sep = []
        elif i in OPERADORES:
            resultado.append([i, OPERADOR])
        elif i in ABRE_FECHA_PARENTESES:
            resultado.append([i, PARENTESES])
        elif i in PONTO_E_VIRGULA:
            resultado.append([i, SEPARADOR])
        elif i in BRANCOS:
            resultado.append([i,SEPARADOR])
        elif i in DIGITOS:
            if exp[index-1] not in LETRAS:
                if index == len(exp) - 1:
                    numero_completo.append(i)
                    resultado.append([float("".join(numero_completo)), NUMERO])
                    numero_completo = []
                elif exp[index+1] in DIGITOS:
                    numero_completo.append(i)
                else:
                    numero_completo.append(i)
                    resultado.append([float("".join(numero_completo)), NUMERO])
                    numero_completo = []
        else:
            resultado.append([i, NAO_ENCONTRADO])
            # if exp[index-1] not in LETRAS:
            #     resultado.append([float(i), NUMERO])
    return resultado
    
