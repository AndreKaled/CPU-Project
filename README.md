# CPU-Project: Montador de CPU de 8 bits em Logisim Evolution
Este projeto consiste na construção de uma CPU de 8 bits e a implementação de um montador (assembler) em Python para uma CPU de 8 bits desenvolvida e simulada no [Logisim Evolution](https://github.com/reds-heig/logisim-evolution). O objetivo principal é facilitar a criação de programas em linguagem assembly para esta CPU, convertendo o código fonte (.asm) em um arquivo de memória (.txt) que pode ser carregado diretamente no Logisim.

## Visão Geral
O CPU-Project é uma ferramenta educacional que permite explorar os fundamentos da arquitetura de computadores e o funcionamento interno de uma Unidade Central de Processamento (CPU). Através deste montador, é possível escrever programas assembly e observar o comportamento em uma CPU simulada, proporcionando uma compreensão prática de como as instruções são traduzidas e executadas.

## Arquitetura da CPU (8 bits)
A CPU implementada no Logisim Evolution possui as seguintes características e componentes:

1. Tamanho da Palavra: 8 bits
2. Memória RAM: 256 posições de 8 bits
3. Registradores: Inclui IAR (Instruction Address Register), IR (Instruction Register), ACC (Accumulator), TMP (Temporary Register), e registradores de uso geral (R0, R1, R2, R3).
4. Periféricos Integrados: Teclado, monitor e porta de E/S (Entrada/Saída) para interação com o usuário.
5. Conjunto de Instruções: Suporta um conjunto básico de instruções programáveis que abrangem operações aritméticas, lógicas, de movimentação de dados e controle de fluxo.
## O Montador (assembler.py)

- Análise do Código Assembly: Lê e interpreta arquivos .asm, ignorando comentários e trata diferentes bases numéricas (hexadecimal, decimal, binário, inclusive valores negativos em complemento de dois).
- Geração de Bytecode: Converte cada instrução assembly em seu respectivo bytecode de 8 bits, conforme a arquitetura da CPU.
- Geração de Arquivo de Memória: Produz um arquivo .txt formatado pronto para ser carregado na RAM da CPU no Logisim Evolution.

### Instruções Suportadas
O montador suporta um conjunto variado de instruções, incluindo:

Manipulação de Dados: LD, ST, DATA
Controle de Fluxo: JMPR, JMP, JC, JA, JE, JZ, e todas as suas combinações condicionais.
Operações Aritméticas/Lógicas: ADD, SHR, SHL, NOT, AND, OR, XOR, CMP
Controle de Flags: CLF
Entrada/Saída (I/O): IN, OUT

## Como Usar
Para utilizar o montador e gerar o arquivo de memória para sua CPU, siga os passos abaixo:

1. Clone o Repositório:

```bash
git clone https://github.com/AndreKaled/CPU-Project.git
cd CPU-Project
```

2. Navegue até a Pasta do Montador:
O script assembler.py está localizado na pasta assembler.

```bash
cd assembler
```

3. Prepare seu Código Assembly:
Crie seu programa em linguagem assembly para a CPU de 8 bits e salve-o com a extensão .asm (ex: meu_programa.asm). Certifique-se de que o código esteja de acordo com as instruções suportadas.

Exemplo de Conteúdo de meu_programa.asm:
```assembly
DATA R0, 0x10   ; Carrega o valor 16 (hexadecimal) no R0
DATA R1, 05     ; Carrega o valor 5 (decimal) no R1
DATA R2, -06    ; Carrega o valor -6 (decimal) no R2 (em complemento de dois)
ADD R0, R1      ; Adiciona R1 a R0 (R0 = R0 + R1)
JMP 0x00        ; Loop infinito para o início do programa
```
4. Execute o Montador:
Execute o script Python, passando o arquivo de entrada (.asm) e o nome do arquivo de saída desejado (.txt):

```bash
python3 assembler.py meu_programa.asm saida.txt
```

Substitua meu_programa.asm pelo nome do seu arquivo de código assembly.
Substitua saida.txt pelo nome que você quer dar ao arquivo de memória gerado.
Carregue no Logisim Evolution:
O arquivo saida.txt estará pronto para ser carregado na memória RAM da sua CPU no Logisim Evolution. Geralmente, isso é feito clicando com o botão direito no componente de memória RAM e selecionando "load Image..." (carregar Imagem...).

## Tecnologias
- Python 3: Linguagem de programação utilizada para desenvolver o montador.
- Logisim Evolution: Ferramenta de simulação de circuitos digitais onde a CPU foi construída.
- Assembly: Linguagem de programação de baixo nível para a CPU de 8 bits.