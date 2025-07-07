import textwrap


def menu():
    """Exibe o menu de opções e retorna a escolha do usuário."""
    menu_str = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu_str)).strip().lower() # Adicionado .strip().lower() para robustez


def depositar(saldo, valor, extrato, /):
    """
    Realiza a operação de depósito.
    Aceita saldo, valor e extrato como argumentos posicionais.
    """
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    """
    Realiza a operação de saque.
    Aceita todos os argumentos como nomeados.
    """
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
    elif excedeu_limite:
        print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
    elif excedeu_saques:
        print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print("\n=== Saque realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    return saldo, extrato, numero_saques # Retorna numero_saques também


def exibir_extrato(saldo, /, *, extrato):
    """
    Exibe o extrato da conta.
    Aceita saldo como argumento posicional e extrato como nomeado.
    """
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("==========================================")


def criar_usuario(usuarios):
    """
    Cria um novo usuário, verificando se o CPF já existe.
    Armazena o usuário em uma lista de dicionários.
    """
    cpf = input("Informe o CPF (somente número): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print("=== Usuário criado com sucesso! ===")


def filtrar_usuario(cpf, usuarios):
    """
    Filtra a lista de usuários para encontrar um usuário pelo CPF.
    Retorna o usuário encontrado ou None.
    """
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_conta(agencia, numero_conta, usuarios):
    """
    Cria uma nova conta para um usuário existente (validado por CPF).
    Retorna o dicionário da nova conta ou None.
    """
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")
    return None # Adicionado retorno None explícito


def listar_contas(contas):
    """
    Lista todas as contas existentes no sistema com seus detalhes.
    """
    if not contas: # Adicionado para exibir mensagem se não houver contas
        print("\n@@@ Nenhuma conta cadastrada. @@@")
        return

    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 40) # Ajustado o tamanho da linha para 40 para melhor visualização
        print(textwrap.dedent(linha))
    print("=" * 40) # Adicionada linha final para consistência


def main():
    """
    Função principal que gerencia o fluxo do sistema bancário.
    """
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []  # Lista para armazenar dicionários de usuários
    contas = []    # Lista para armazenar dicionários de contas

    while True:
        opcao = menu()

        if opcao == "d":
            try:
                valor = float(input("Informe o valor do depósito: "))
            except ValueError:
                print("\n@@@ Valor inválido. Por favor, digite um número para o depósito. @@@")
                continue # Continua para a próxima iteração do loop

            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            try:
                valor = float(input("Informe o valor do saque: "))
            except ValueError:
                print("\n@@@ Valor inválido. Por favor, digite um número para o saque. @@@")
                continue # Continua para a próxima iteração do loop

            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            # Gera o número da conta sequencialmente
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta: # Só adiciona a conta se ela foi criada com sucesso (usuário encontrado)
                contas.append(conta)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            print("Saindo do sistema. Obrigado por usar nossos serviços!")
            break

        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")


if __name__ == "__main__":
    main()