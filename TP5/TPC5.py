def listar(cinema):
    print("Filmes em exibição:")
    for i, sala in enumerate(cinema):
        filme = sala[2]
        print(f"Sala {i + 1}: {filme}")


def disponivel(cinema, filme, lugar):
    cond = False
    for sala in cinema:
        nlugares, Vendidos, Filme = sala
        if Filme == filme and lugar <= nlugares:
            if lugar not in Vendidos:
                cond = True
    return cond

def VendeBilhete(cinema, filme, lugar):
    if disponivel(cinema,filme,lugar):
        for sala in cinema:
            nlugares, Vendidos, Filme = sala
        if Filme == filme:
            if lugar not in Vendidos:
                Vendidos.append(lugar)
    return cinema

def listarDisponibilidades(cinema):
    for i, sala in enumerate(cinema):
        filme = sala[2]
        nlugares = sala[0]
        ocupados = len(sala[1])
        disponiveis = nlugares - ocupados
        print(f"Sala {i + 1}: Filme '{filme}', Lugares disponíveis: {disponiveis}")



def inserirSala(cinema, sala):
    for s in cinema:
        if s[2] == sala[2]:   #s é uma sala individual dentro do cinema, tem mm estrutura que sala.
            print(f"Erro: A sala com o filme '{sala[2]}' já esxiste.")
            return cinema
    cinema.append(sala)
    return cinema

def removerSala(cinema, filme):
    return[sala for sala in cinema if sala[2] != filme]

def listarSala(cinema, filme):
    for sala in cinema:
        if sala[2] == filme:
            print(f"Filme: {sala[2]},   Lugares ocupados: {len(sala[1])},   Lugares disponiveis: {sala[0] - len(sala[1])}")
            return
        print(f"Erro: O filme '{filme} não está em exibição.")

def menu():
    cinema = []
    
    while True:
        print("\n--- Gestão de Cinema ---")
        print("1. Inserir sala")
        print("2. Listar filmes em exibição")
        print("3. Verificar se um lugar está disponível")
        print("4. Vender bilhete")
        print("5. Listar disponibilidades por sala")
        print("6. Remover sala")
        print("0. Sair")
        
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            filme = input("Nome do filme: ")
            nlugares = int(input("Número de lugares: "))
            nova_sala = (nlugares, [], filme)
            cinema = inserirSala(cinema, nova_sala)

        elif opcao == "2":
            listar(cinema)

        elif opcao == "3":
            filme = input("Nome do filme: ")
            lugar = int(input("Número do lugar: "))
            if disponivel(cinema, filme, lugar):
                print(f"O lugar {lugar} está disponível para o filme '{filme}'.")
            else:
                print(f"O lugar {lugar} já está ocupado.")

        elif opcao == "4":
            filme = input("Nome do filme: ")
            lugar = int(input("Número do lugar: "))
            if disponivel(cinema, filme, lugar):
                cinema = VendeBilhete(cinema, filme, lugar)
                print(f"Bilhete vendido para o lugar {lugar} no filme '{filme}'.")
            else:
                print(f"Não foi possível vender o bilhete. O lugar {lugar} já está ocupado.")

        elif opcao == "5":
            listarDisponibilidades(cinema)

        elif opcao == "6":
            filme = input("Nome do filme a remover: ")
            cinema = removerSala(cinema, filme)
            print(f"Sala do filme '{filme}' removida.")

        elif opcao != "0":
            print("Opção inválida. Tente novamente.")
    
    print("Saindo...")

menu()









