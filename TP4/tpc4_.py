import random

def  menu():
    print("---------------------MENU---------------------")
    print("opçao 1 - Criar Lista") 
    print("opçao 2- Ler Lista")
    print("opçao 3 - Soma")
    print("opçao 4 - Média")
    print("opçao 5 - Maior")
    print("opçao 6 - Menor")
    print("opçao 7 - estar Ordenada por ordem crescente")
    print("opçao 8 - estar Ordenada por ordem decrescente")
    print("opçao 9 - Procura um elemento")
    print("opçao 0 - Sair")
    print("-----------------------------------------------")

def criar_lista_aleatoria():
    tamanho = int(input("Digite o tamanho da sua lista: "))
    lista = []
    i = 0
    while i < tamanho:
        x = random.randint(1,100)
        lista.append(x)
        i = i + 1
    return lista

def ler_lista():
    tamanho = int(input("Digite o tamanho da lista: "))
    i = 0 
    lista = []
    while i < tamanho:
        x = int(input("escreva um numero da sua lista:"))
        i = i + 1
        lista.append(x)
    return lista


def calcular_soma(lista):
    soma = 0
    i = 0
    while i < len(lista): 
        soma = soma + lista[i]
        i = i + 1
    return soma


def calcular_media(lista):
    if len(lista) == 0:
        return 0
    soma = 0
    i = 0
    while i < len(lista):
        soma = soma + lista[i]
        i = i + 1
    return soma / len(lista)



def encontrar_maior(lista):
    maior = lista[0]
    for elem in lista:
        if elem > maior:
            maior = elem
    return maior


def encontrar_menor(lista):
    menor = lista[0]
    for elem in lista:
        if elem < menor:
            menor = elem
    return menor


def esta_ordenada_crescente(lista):
    for i in range(len(lista) - 1):
        if lista[i] > lista[i + 1]:
            return "Não"
    return "Sim"


def esta_ordenada_decrescente(lista):
    for i in range(len(lista) - 1):
        if lista[i] < lista[i + 1]:
            return "Não"
    return "Sim"
   


def procurar_elemento(lista):
    x = int(input("introduza o numero que pretende procurar:"))
    posicao = lista.index(x)
    if x in lista:
        print (f"Está e encontra-se na posição {posicao}")
    else:
        print ("-1")

def Main():
    cond = True

    while(cond):
        menu()
        opcao = input("introduza a opçao pretendida:")

        if opcao == "1":
            lista = criar_lista_aleatoria()
            print(lista)
            
        elif opcao == "2":
            lista = ler_lista()
            print(lista)

        elif opcao == "3":
            res = calcular_soma(lista)
            print(res)

        elif opcao == "4":
            res = calcular_media(lista)
            print(res)

        elif opcao == "5":
            res = encontrar_maior(lista)
            print(res)

        elif opcao == "6":
            res = encontrar_menor(lista)
            print(res)

        elif opcao == "7":
            res = esta_ordenada_decrescente(lista)
            print(res)

        elif opcao == "8":
            res = esta_ordenada_crescente(lista)
            print(res)

        elif opcao == "9":
            res = procurar_elemento(lista)
            print(res)

        elif opcao == "0":
            cond = False
            print("Volte Sempre!")
Main()