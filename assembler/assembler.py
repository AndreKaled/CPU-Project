"""
Aluno: [André Kaled]
"""

import sys
import os
# constantes
INIT_CODE = "v3.0 hex words plain\n"
BYTE_SIZE = 1
TOTAL_BITS = BYTE_SIZE * 8                # capacidade maxima de dado (considerando complemento de dois)
MAX_POSITIVO = (1 << (TOTAL_BITS - 1)) -1 # maior positivo com complemento de dois
MIN_NEGATIVO = -(1 << (TOTAL_BITS - 1))   # menor negativo com complemento de dois
MASCARA = (1 << TOTAL_BITS) - 1           # mascara para garantir que caiba na RAM
COMPLEMENTO_DOIS = (1 << TOTAL_BITS)      # desloca bits e subtrai 1

# classe de instrucao (era uma struct), para traduzir a gramatica regular do assembly
class Instrucao:
    def __init__(self, comando="", op1="", op2=""):
        self.comando = comando
        self.op1 = op1
        self.op2 = op2

# simulador da ram
RAM_SIZE = 256
ram = [0x00] * RAM_SIZE

flags_jcaez = {"C": 0x8, "A":0x4, "E": 0x2, "Z":0x1}

# dicionario para ter a instrucao hexadecimal como base, modificando com registradores ou addr
comandos = {"LD"  : 0x00, "ST"  : 0x10,
            "DATA": 0x20, "JMPR": 0x30,
            "JMP" : 0x40, "CLF" : 0x60,
            "IN"  : 0x70, "OUT" : 0x78,
            "ADD" : 0x80, "SHR" : 0x90, 
            "SHL" : 0xA0, "NOT" : 0xB0,
            "AND" : 0xC0, "OR"  : 0xD0, 
            "XOR" : 0xE0, "CMP" : 0xF0,
}
def init():
    """ Inicializa os acessos de arquivos passados nos argumentos
    Para o segundo argumento, quando nao existir o arquivo, será criado pelo programa com o mesmo nome dado no argumento
    Para tratar eventuais erros, o programa para e informa o possível problema previsto para ser corrigido
    """
    input = None
    output = None
    try:
        # checa se foi chamado corretamente
        if len(sys.argv) < 3:
            print("ERRO: Há argumentos faltando! Use: python3 montador.py <codigo.asm> <saida.txt>")
            exit(1)
        if len(sys.argv) > 3:
            print("ERRO: Há argumentos demais! Use: python3 montador.py <codigo.asm> <saida.txt>")
            exit(1)
        if os.path.splitext(sys.argv[1])[1][1:] != "asm" or os.path.splitext(sys.argv[2])[1][1:] != "txt":
            print("ERRO: Extensões inválidas dos argumentos. ")
            if ext1 != "asm":
                print(f"Você não queria dizer {os.path.splitext(sys.argv[1])[0]}.asm?")
            if ext2 != "txt":
                print(f"Você não queria dizer {os.path.splitext(sys.argv[2])[0]}.txt?")
            exit(1)
        # abre os arquivos e inicia a escrita padrão
        input = open(sys.argv[1], "r") 
        output = open(sys.argv[2], "w")
        output.write(INIT_CODE)
        return input, output
    except FileNotFoundError:
        print(f"ERRO: Arquivo {sys.argv[1]} não encontrado!")
        exit(1)


def lerComando(linha):
    """ # A função recebe uma linha do arquivo de input e transforma para o tipo Intrução [comando, operador1, operador2], usado """
    linha = linha.upper().split(";")[0].strip()
    linha = linha.replace(",", " ")
    partes = linha.split()
    if not partes:
        return None
    cmd = partes[0]
    op1 = partes[1] if len(partes) > 1 else None
    op2 = partes[2] if len(partes) > 2 else None
    return Instrucao(cmd, op1, op2)

# salva os dados do vetor "ram" para o arquivo de saída
def salva(dados, pos, tam, output_file):
    vet = dados.copy()
    for i in range(pos, tam):
        vet.append(0x00)

    for i in range(tam):
        output_file.write(f"{vet[i]:02x}")
        if (i+1) % 16 == 0:
            output_file.write("\n")
        else:
            output_file.write(f" ")

# converte o registrador em número
def regToNum(reg=""):
    if (len(reg) != 2) or (reg[0] != 'R') or not reg[1].isdigit() or (int(reg[1]) < 0) or(int(reg[1]) > 3):
        print("ERRO: registrador inválido: ", reg)
        exit(1)
    return int(reg[1])

# recebe o nome da instrucao e busca se existe um comando com o mesmo nome
def buscaComando(nome=""):
    if (nome.startswith("JC") or nome.startswith("JA") or 
    nome.startswith("JE") or nome.startswith("JZ")):
        return 0x50
    if nome in comandos:
        return comandos[nome]
    else:
        print(f"ERRO: Comando {nome} inválido!")
        exit(1)

def trataDado(op):
    if op != None and not op.startswith("R") and op not in {"DATA", "ADDR"}:
        numeroInicial = None
        if op.startswith("0X"):
            numeroInicial = int(op, 16)
            if numeroInicial > MASCARA:
                print(f"ERRO: o hexadecimal {op} não cabe "
                      f"em {TOTAL_BITS} bits (max:{hex(MASCARA)})")
                exit(1)
        elif op.startswith("0B"):
            numeroInicial = int(op, 2)  
            if numeroInicial > MASCARA:
                print(f"ERRO: o binário {op} não cabe "
                      f"em {TOTAL_BITS} bits (max:{bin(MASCARA)})")
                exit(1)
        else:
            try:
                numeroInicial = int(op)
                if numeroInicial < MIN_NEGATIVO or numeroInicial > MAX_POSITIVO:
                    print(f"ERRO: o número {op} está fora do "
                          f"intervalo [{MIN_NEGATIVO},{MAX_POSITIVO}]")
                    exit(1)
                if numeroInicial < 0:
                    numeroInicial = COMPLEMENTO_DOIS + numeroInicial
            except ValueError:
                print(f"ERRO: valor {op} não é um número válido")
                exit(1)
        valorMascarado = numeroInicial & MASCARA
        # ve se o bit de sinal está ligado e retorna em complemento de dois
        if valorMascarado & (1 << (TOTAL_BITS -1)) != 0:
            return (valorMascarado - COMPLEMENTO_DOIS) & MASCARA
        # valor positivo
        else:
            return valorMascarado
    return op

def flags(jcaez):
    jcaez = jcaez[1:]
    if len(jcaez) > 4:
        print("ERRO: Há um JCAEZ com flags a mais do que esperado!")
        exit(1)
    hex = 0x0
    for let in jcaez:
        hex += flags_jcaez[let]
    return hex

# converte a instrucao em byte, faz a manipulação bit a bit conforme os registradores ou addr
def geraByteCode(instrucao, ram, pos):
    byte1 = buscaComando(instrucao.comando)
    byte2 = 0x00
    instrucao.op1 = trataDado(instrucao.op1)
    instrucao.op2 = trataDado(instrucao.op2)
    print(instrucao.comando)
    if (instrucao.comando == "LD" or instrucao.comando == "ST" or instrucao.comando == "ADD" or instrucao.comando == "SHR" or instrucao.comando == "SHL" or 
        instrucao.comando == "NOT" or instrucao.comando == "AND" or instrucao.comando == "OR" or instrucao.comando == "XOR" or instrucao.comando == "CMP"):
        byte1 |= (regToNum(instrucao.op1) << 2) | regToNum(instrucao.op2)
    elif instrucao.comando == "DATA": # data usa 2 bytes
        byte1 |= regToNum(instrucao.op1)
        byte2 = instrucao.op2
    elif instrucao.comando == "IN" or instrucao.comando == "OUT":
        tipo = instrucao.op1
        reg = instrucao.op2
        in_out = 1 if instrucao.comando == "OUT" else 0
        if tipo == "ADDR":
            byte1 |= (in_out << 3) | (1 << 2) | regToNum(reg)
        elif tipo == "DATA":
            byte1 |= (in_out << 3) | (0 << 2) | regToNum(reg)
        else:
            print("Operando inválido para IN/OUT")
            exit(1)
    elif instrucao.comando == "JMPR":
        byte1 |= regToNum(instrucao.op1)
    elif instrucao.comando.startswith("J"): # para jumps 
        if instrucao.comando != "JMP" and instrucao.comando != "JMPR":
            byte1|= flags(instrucao.comando)
        byte2 = instrucao.op1
        
    # modifica a "RAM"
    ram[pos] = byte1
    pos = pos + 1
    if byte2:
        ram[pos] = byte2
        pos = pos + 1
    return pos

# funcao principal
def main():
    input_file, output_file = init()
    pos = 0
    for linha in input_file:
        linha = linha.strip()
        instrucao = lerComando(linha)
        if instrucao:
            pos = geraByteCode(instrucao, ram, pos)
    
    salva(ram, pos, RAM_SIZE, output_file)
    print(f"Processado com sucesso, arquivo em {sys.argv[2]}")
    output_file.close()
    input_file.close()
    exit(0)
    
main()