
def Menu():
    print("--------------- MENU ---------------")
    print("1. Criar uma turma")
    print("2. Inserir um aluno na turma")
    print("3. Listar a turma")
    print("4. Consultar um aluno por ID")
    print("5. Guardar a turma em ficheiro")
    print("6. Carregar uma turma de um ficheiro")
    print("0. Sair da aplicação")
    print("-------------------------------------")




def Criar_Turma():
    turma = []
    return turma

def Inserir_Aluno(turma):

    nome_aluno = input("Nome do aluno: ")
    id_aluno = input("ID do aluno: ")
    notaTPC = float(input("Nota do TPC: "))
    notaProjeto = float(input("Nota do Projeto: "))
    notaTeste = float(input("Nota do Teste: "))

    aluno = (nome_aluno, id_aluno, [notaTPC, notaProjeto, notaTeste])
    turma.append(aluno)

    print(f" O aluno {nome_aluno} foi inserido na turma.")
    return turma


def Listar_Turma(turma):
    if turma == []:
        print("Ainda não existem alunos na turma.")
    else:
        print(" ---------------------------------------- LISTAGEM DA TURMA ---------------------------------------- ")
        for aluno in turma:
            print(f"Nome: {aluno[0]} | ID: {aluno[1]} | Nota TPC: {aluno[2][0]} | Nota Projeto: {aluno[2][1]} | Nota Teste: {aluno[2][2]}")
        print(" --------------------------------------------------------------------------------------------------- ")


def Consultar_Aluno(turma):
    id_consultar = input("Digite o ID do aluno que deseja consultar:")
    encontrado = False
    for aluno in turma:
        if id_consultar == aluno[1]:
            encontrado = True
            print("Aluno encontrado:")
            print(f"Nome: {aluno[0]} | ID: {aluno[1]} | Nota TPC: {aluno[2][0]} | Nota Projeto: {aluno[2][1]} | Nota Teste: {aluno[2][2]}")
    if not encontrado:
        print("Aluno não encontrado.")


def Guardar_Ficheiro(turma):
    nome_ficheiro = input("Nome do ficheiro para guardar a turma (nomedoficheiro.txt):")

    file = open(nome_ficheiro,"w", encoding="utf-8") # sempre que abrimos um ficheiro... # encoding="utf-8" para evitar erros em letras com acentos, cedilhas, etc
    for aluno in turma:
        linha = f"{aluno[0]} | {aluno[1]} | {aluno[2][0]}, {aluno[2][1]}, {aluno[2][2]}"
        file.write(f"{linha}\n")
    file.close() 

    print(f"Turma guardada no ficheiro {nome_ficheiro}.")


def Carregar_Ficheiro():
    nome_ficheiro = input("Nome do ficheiro que deseja carregar (nomedoficheiro.txt):")
    turma = []
    
    file = open(nome_ficheiro,"r", encoding="utf-8") 
    for line in file: # line = aluno (tem a informação toda do aluno)
        nome_aluno, id_aluno, notas = line.split(" | ")
        notaTPC, notaProjeto, notaTeste = notas.split(", ")
        notas_aluno = [float(notaTPC), float(notaProjeto), float(notaTeste)]
        turma.append((nome_aluno, id_aluno, notas_aluno))
    file.close() 

    print("Ficheiro carregado com sucesso:")
    print (turma)
    return turma


def Main():
    turma = []
    cond = True
    while cond:
        Menu()
        opcao = input("Introduza uma opção:")
        if opcao == "1":
            turma = Criar_Turma()
            print("Nova turma criada.")
        elif opcao == "2":
            turma = Inserir_Aluno(turma)
        elif opcao == "3":
            Listar_Turma(turma)
        elif opcao == "4":
            Consultar_Aluno(turma)
        elif opcao == "5":
            Guardar_Ficheiro(turma)
        elif opcao == "6":
            turma = Carregar_Ficheiro()
        elif opcao == "0":
            cond = False
            print("Até à próxima!")

Main()
