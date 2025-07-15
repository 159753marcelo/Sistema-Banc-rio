# 🏦 Sistema Bancário Orientado a Objetos (POO)

              **Sistema Bancário Avançado**! 🚀

Este projeto foi completamente refatorado para utilizar o paradigma de **Programação Orientada a Objetos (POO)** em Python. Agora, clientes, contas e transações são representados por objetos, o que torna o código mais organizado, modular e fácil de manter e expandir.

---

## ✨ Funcionalidades Principais:

### 👤 Gerenciamento de Clientes e Contas:
* **Novo Usuário** `[nu]`: Cadastre clientes como `PessoaFisica`, informando CPF, nome, data de nascimento e endereço.
* **Nova Conta** `[nc]`: Crie uma `ContaCorrente` para um cliente existente, vinculando a conta ao seu respectivo titular.
* **Listar Contas** `[lc]`: Visualize todas as `ContasCorrente` cadastradas no sistema, com seus detalhes de agência, número e titular.

### 💰 Operações Financeiras:
* **Depositar** `[d]`: Realize depósitos em uma conta selecionada. As transações são registradas no `Historico` da conta.
* **Sacar** `[s]`: Efetue saques em uma conta selecionada, respeitando os limites de R$500 por saque e um máximo de 3 saques diários para `ContaCorrente`. As transações também são registradas no `Historico`.
* **Extrato** `[e]`: Consulte o `Historico` completo de transações de uma conta, exibindo detalhes como tipo, valor e data/hora de cada operação, além do saldo atual.

### 🎯 Características da Implementação POO:
* **Classes Dedicadas**: `Cliente`, `PessoaFisica`, `Conta`, `ContaCorrente`, `Historico`, `Transacao`, `Saque`, `Deposito`.
* **Herança**: `PessoaFisica` herda de `Cliente`, e `ContaCorrente` herda de `Conta`, promovendo a reutilização de código.
* **Polimorfismo**: Métodos como `sacar` são especializados em `ContaCorrente`, e `registrar` em `Saque` e `Deposito` agem de formas diferentes.
* **Encapsulamento**: Uso de propriedades (`@property`) para controlar o acesso aos atributos internos das classes (ex: `saldo`, `historico`).
* **Composição**: Cada `Conta` "possui um" `Historico`, o que centraliza o registro das transações.

---

## 🚀 Como Executar o Projeto:

1.  **Requisito:** Certifique-se de ter o **Python 3** (ou superior) instalado em seu sistema.
2.  **Salve o Código:** Salve o código fornecido (aquele que você me enviou por último, o "corrigido") em um arquivo chamado `banco_poo.py` (ou o nome que preferir, mantendo a extensão `.py`).
3.  **Abra o Terminal:** Navegue até o diretório onde você salvou o arquivo.
4.  **Execute o Programa:** Digite o seguinte comando e pressione Enter:
    ```bash
    python banco_poo.py
    ```
5.  **Interaja:** O menu será exibido no terminal. Siga as instruções para criar usuários, contas e realizar operações bancárias.

