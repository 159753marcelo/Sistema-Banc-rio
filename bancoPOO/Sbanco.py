import textwrap
from datetime import datetime # Importar para usar no histórico de transações

# ==============================================================================
# CLASSES DO SISTEMA BANCÁRIO (POO)
# ==============================================================================

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        # Implementa o comportamento de uma transação (sacar ou depositar)
        # O método transacao.registrar é polimórfico e lida com o tipo de transação
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__, # Nome da classe (Saque/Deposito)
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico() # Cada conta tem seu próprio histórico

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
        elif valor <= 0:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
        else:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True
        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques
        self._saques_hoje = 0

    @property
    def limite(self):
        return self._limite

    @property
    def limite_saques(self):
        return self._limite_saques

    def sacar(self, valor):
        excedeu_limite = valor > self._limite
        excedeu_saques = self._saques_hoje >= self._limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
        else:
            # Chama o sacar da classe base (Conta) para verificar saldo e efetuar o saque
            if super().sacar(valor): # Se o saque base for bem-sucedido
                self._saques_hoje += 1
                return True
        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """


class Transacao:
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    # Método abstrato que será implementado pelas subclasses
    def registrar(self, conta):
        raise NotImplementedError


class Saque(Transacao):
    def __init__(self, valor):
        super().__init__(valor)

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        super().__init__(valor)

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


# ==============================================================================
# FUNÇÕES DE INTERFACE/UTILITY (fora das classes, para o fluxo principal)
# ==============================================================================

# A função menu() está definida aqui, ANTES de ser usada na função main()
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


def recuperar_conta_cliente(cliente):
    """Permite ao cliente selecionar uma de suas contas."""
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return None

    if len(cliente.contas) == 1:
        return cliente.contas[0]
    else:
        print("\nContas disponíveis:")
        for i, conta in enumerate(cliente.contas):
            print(f"{i+1}. Agência: {conta.agencia}, C/C: {conta.numero}")
        
        while True:
            try:
                escolha = int(input("Selecione o número da conta: ")) - 1
                if 0 <= escolha < len(cliente.contas):
                    return cliente.contas[escolha]
                else:
                    print("Escolha inválida. Tente novamente.")
            except ValueError:
                print("Entrada inválida. Digite um número.")


def depositar_operacao(clientes):
    """Função de alto nível para a operação de depósito."""
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    try:
        valor = float(input("Informe o valor do depósito: "))
    except ValueError:
        print("\n@@@ Valor inválido. Por favor, digite um número. @@@")
        return

    transacao = Deposito(valor)
    cliente.realizar_transacao(conta, transacao)


def sacar_operacao(clientes):
    """Função de alto nível para a operação de saque."""
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    try:
        valor = float(input("Informe o valor do saque: "))
    except ValueError:
        print("\n@@@ Valor inválido. Por favor, digite um número. @@@")
        return

    transacao = Saque(valor)
    cliente.realizar_transacao(conta, transacao)


def exibir_extrato_operacao(clientes):
    """Função de alto nível para a operação de extrato."""
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato_str = ""
    if not transacoes:
        extrato_str = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato_str += f"{transacao['data']} - {transacao['tipo']}:\tR$ {transacao['valor']:.2f}\n"

    print(extrato_str)
    print(f"\nSaldo:\t\tR$ {conta.saldo:.2f}")
    print("==========================================")


def criar_usuario_operacao(clientes):
    """Cria um novo usuário (PessoaFisica)."""
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(cliente)
    print("\n=== Usuário criado com sucesso! ===")


def criar_conta_operacao(numero_conta, clientes, contas):
    """Cria uma nova conta corrente para um cliente existente."""
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.adicionar_conta(conta) # Adiciona a conta à lista de contas do cliente
    print("\n=== Conta criada com sucesso! ===")


def listar_contas_operacao(contas):
    """Lista todas as contas cadastradas no sistema."""
    if not contas:
        print("\n@@@ Nenhuma conta cadastrada. @@@")
        return

    print("\n================ CONTAS CADASTRADAS ================")
    for conta in contas:
        print(textwrap.dedent(str(conta))) # Usa o método __str__ da ContaCorrente
        print("-" * 40)
    print("====================================================")


def filtrar_cliente(cpf, clientes):
    """Função auxiliar para encontrar um cliente pelo CPF."""
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


# ==============================================================================
# FUNÇÃO PRINCIPAL
# ==============================================================================

def main():
    """Função principal que executa o sistema bancário."""
    clientes = [] # Lista de objetos Cliente
    contas = []   # Lista de objetos Conta

    while True:
        opcao = menu()

        if opcao == "d":
            depositar_operacao(clientes)
        elif opcao == "s":
            sacar_operacao(clientes)
        elif opcao == "e":
            exibir_extrato_operacao(clientes)
        elif opcao == "nu":
            criar_usuario_operacao(clientes)
        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta_operacao(numero_conta, clientes, contas)
        elif opcao == "lc":
            listar_contas_operacao(contas)
        elif opcao == "q":
            print("\nSaindo do sistema. Obrigado por usar nossos serviços!")
            break
        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")


if __name__ == "__main__":
    main()