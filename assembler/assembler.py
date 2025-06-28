"""
Aluno: [André Kaled Duarte Coutinho Andrade]
Matricula: [22450837]
"""
import sys
import os
# =============================
#     CONSTANTES GLOBAIS       
#==============================
INIT_CODE = "v3.0 hex words plain\n"
BYTE_SIZE = 1
TOTAL_BITS = BYTE_SIZE * 8                # capacidade maxima de dado (considerando complemento de dois)
MAX_POSITIVO = (1 << (TOTAL_BITS - 1)) -1 # maior positivo com complemento de dois
MIN_NEGATIVO = -(1 << (TOTAL_BITS - 1))   # menor negativo com complemento de dois
MASCARA = (1 << TOTAL_BITS) - 1           # mascara para garantir que caiba na RAM
COMPLEMENTO_DOIS = (1 << TOTAL_BITS)      # desloca bits e subtrai 1
MAX_MEMORIA = (1 << TOTAL_BITS)           # maior hexadecimal armazenavel na memoria

# classe de instrucao (era uma struct), para traduzir a gramatica regular do assembly
class Instrucao:
    def __init__(self, comando="", bytecode="", op1="", op2=""):
        self.comando = comando
        self.bytecode = bytecode
        self.op1 = op1
        self.op2 = op2

# simulador da ram
RAM_SIZE = 256
ram = []
flags_jcaez = {"C": 0x8, "A":0x4, "E": 0x2, "Z":0x1}

# dicionario para ter a instrucao hexadecimal como base, modificando com registradores ou addr
comandos_clear = {"CLF" : 0x60}
comandos_IO = {"IN"  : 0x70, "OUT" : 0x78,}
comandos_logico_aritmeticos = {
    "LD"  : 0x00, "ST"  : 0x10,
    "ADD" : 0x80, "SHR" : 0x90, 
    "SHL" : 0xA0, "NOT" : 0xB0,
    "AND" : 0xC0, "OR"  : 0xD0, 
    "XOR" : 0xE0, "CMP" : 0xF0,
}

comandos_facilitadores = {
    "MOVE": 0, "CLR": 1,
    "HALT": 2,
}

comandos_data = {"DATA": 0x20,}
comandos_jumpers = {"JMPR": 0x30, "JMP" : 0x40}

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
            print("ERRO: Há argumentos demais! Use: python3 montador.py <codigo.asm> <saida.m>")
            exit(1)
        if os.path.splitext(sys.argv[1])[1][1:] != "asm" or os.path.splitext(sys.argv[2])[1][1:] != "m":
            print("ERRO: Extensões inválidas dos argumentos. ")
            if os.path.splitext(sys.argv[1])[1][1:] != "asm":
                print(f"Você não queria dizer {os.path.splitext(sys.argv[1])[0]}.asm?")
            if os.path.splitext(sys.argv[2])[1][1:] != "m":
                print(f"Você não queria dizer {os.path.splitext(sys.argv[2])[0]}.m?")
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
    """ A função recebe uma linha do arquivo de input e transforma para o tipo Intrução [comando, operador1, operador2] usado"""
    linha = linha.upper().split(";")[0].strip()
    linha = linha.replace(",", " ")
    partes = linha.split()
    flag = None
    if not partes:
        return None
    if partes[0] in comandos_logico_aritmeticos:
        opcode = comandos_logico_aritmeticos[partes[0]]
    elif partes[0] in comandos_data:
        opcode = comandos_data[partes[0]]
    elif partes[0] in comandos_jumpers:
        opcode = comandos_jumpers[partes[0]]
    elif partes[0] in comandos_IO:
        opcode = comandos_IO[partes[0]]
    elif partes[0] in comandos_clear:
        opcode = comandos_clear[partes[0]]
    elif partes[0] in comandos_facilitadores:
        opcode = comandos_facilitadores[partes[0]]
        flag = 1
    elif (partes[0].startswith("JC") or partes[0].startswith("JA") or 
    partes[0].startswith("JE") or partes[0].startswith("JZ")):
        opcode = 0x50 | flags(partes[0])
    else:
        print(f"ERRO: Comando {linha} inválido!")
        exit(1)
    cmd = partes[0]
    op1 = partes[1] if len(partes) > 1 else None
    op2 = partes[2] if len(partes) > 2 else None
    return Instrucao(cmd, opcode, op1, op2), flag

def salva(dados, output_file):
    """ Passa todos os dados salvos na "RAM" recebida para o arquivo de saída. 
        Quando a "RAM" está incompleta, a função preenche o vazio com 0x00
    """
    vet = dados.copy()
    for dado in vet:
        output_file.write(f"{dado:02x}\n")

def regToNum(reg=""):
    """ recebe como argumento um registrador e o converte em número """
    if (len(reg) != 2) or (reg[0] != 'R') or not reg[1].isdigit() or (int(reg[1]) < 0) or(int(reg[1]) > 3):
        print("ERRO: registrador inválido: ", reg)
        exit(1)
    return int(reg[1])

def trataDado(op, permite_negativo=True):
    """ converte um argumento (bin, hex, dec) em hexadecimal, isso quando não
        for data, addr (para in/out) e registrador"""
    if not op:
        print("ERRO: está faltando argumentos")
        exit(1)
    if op.startswith("R") or op in {"DATA", "ADDR"}:
        return op # nao trata registrador nem palavra chave
    try:
        if op.startswith("0X"):
            num = int(op, 16)
        elif op.startswith("0B"):
            num = int(op,2)
        else:
            num = int(op)
        if not permite_negativo and num < 0:
            print(f"ERRO: valor {op} fora do intervalo [0,{MASCARA}]")
            exit(1)
        if permite_negativo:
            if num < MIN_NEGATIVO or num > MASCARA:
                print(f"ERRO: valor {op} fora do intervalo [{MIN_NEGATIVO, {MASCARA}}]")
            if num < 0:
                num = COMPLEMENTO_DOIS + num
        else:
            if num < 0 or num > MASCARA:
                print(f"ERRO: valor {op} fora do intervalo [0,{MASCARA}]")
                exit(1)
        return num & MASCARA
    except ValueError:
        print(f"ERRO: valor {op} não é um número válido")
        exit(1)

def flags(jcaez):
    """ aciona as flags do jumper """
    jcaez = jcaez[1:]
    if len(jcaez) > 4:
        print("ERRO: Há um JCAEZ com flags a mais do que esperado!")
        exit(1)
    hex = 0x0
    for let in jcaez:
        hex += flags_jcaez[let]
    return hex

def expandir_pseudo_instrucao(instrucao_obj_original, flag_facilitador):
    if flag_facilitador: # flag indicadora de que é um comando facilitador (MOVE, CLR, HALT)
        if instrucao_obj_original.comando == "CLR":
            # CLR Ra -> XOR Ra Ra
            return [Instrucao("XOR", comandos_logico_aritmeticos["XOR"], instrucao_obj_original.op1, instrucao_obj_original.op1)]
        
        elif instrucao_obj_original.comando == "MOVE":
            # MOVE Ra Rb -> XOR Rb, Ra; XOR Ra, Rb
            # instrucao_obj_original.op1 é a fonte (Ra)
            # instrucao_obj_original.op2 é o destino (Rb)
            return [
                Instrucao("XOR", comandos_logico_aritmeticos["XOR"], instrucao_obj_original.op2, instrucao_obj_original.op1), 
                Instrucao("XOR", comandos_logico_aritmeticos["XOR"], instrucao_obj_original.op1, instrucao_obj_original.op2)]
        
        elif instrucao_obj_original.comando == "HALT":
            # HALT como JMP para si mesmo.
            return [Instrucao("HALT", 0xEE, None, None)]
            
    # todos os outros comandos (LD, ADD, JMP, etc.), retorna a instrução original em uma lista.
    return [instrucao_obj_original]

def geraByteCode(instrucao_obj, ram, pos):
    """ Converte uma instrucao (já expandida) em bytecode e a armazena na RAM. """
    byte1 = instrucao_obj.bytecode
    byte2 = 0x00
    if instrucao_obj.comando in comandos_logico_aritmeticos:
        reg1_num = regToNum(instrucao_obj.op1)
        reg2_num = regToNum(instrucao_obj.op2)
        byte1 |= (reg1_num << 2) | reg2_num
    elif instrucao_obj.comando in comandos_data:
        reg_num = regToNum(instrucao_obj.op1)
        data_value = trataDado(instrucao_obj.op2, permite_negativo=True)
        byte1 |= reg_num
        byte2 = data_value    
    elif instrucao_obj.comando in comandos_IO:
        tipo = instrucao_obj.op1
        reg = instrucao_obj.op2
        in_out_bit = 1 if instrucao_obj.comando == "OUT" else 0
        byte1 |= (in_out_bit << 3) | ((1 if tipo == "ADDR" else 0) << 2) | regToNum(reg)
    elif instrucao_obj.comando == "JMPR":
        reg_num = regToNum(instrucao_obj.op1)
        byte1 |= reg_num
    elif instrucao_obj.comando == "CLF":
        byte1 = instrucao_obj.bytecode
    elif instrucao_obj.comando == "HALT":
        byte1 = instrucao_obj.bytecode
    # Lógica para JMP e Jumps Condicionais (JCAEZ)
    elif instrucao_obj.comando.startswith("J") and instrucao_obj.comando != "JMPR":
        byte2 = trataDado(instrucao_obj.op1, permite_negativo=False) # instrucao_obj.op1 deve ser o endereço ou label (resolvido na 2a passagem)
    else:
        print(f"ERRO INTERNO: Comando '{instrucao_obj.comando}' não tratado na geração do bytecode final.")
        exit(1)

    # escreve o(s) byte(s) na RAM
    ram.append(byte1)
    pos += 1

    # verifica se um segundo byte é necessário (DATA, JMP, JCAEZ)
    if instrucao_obj.comando in comandos_data or (instrucao_obj.comando.startswith("J") and instrucao_obj.comando != "JMPR"):
        ram.append(byte2)
        pos += 1

def tamanho_instrucao(instrucao):
    """Retorna o tamanho de bytes de uma instrucao (expandida ou nao)
    Usado na primeira passagem pra calcular os endereços dos labels"""
    if (instrucao.comando in comandos_data or
        instrucao.comando == "HALT" or
        (instrucao.comando.startswith("J") and instrucao.comando != "JMPR")):
        return 2
    return 1

def primeiraPassagem(input_file_content):
    labels = {}
    rastreio_pos = 0

    # --- PRIMEIRA PASSAGEM ---
    for linha_str_original in input_file_content:
        linha_str = linha_str_original.strip()
        if not linha_str or linha_str.startswith(';'): # Ignora linhas vazias ou comentários
            continue
        
        # ve se tem label
        if ":" in linha_str:
            partes_label = linha_str_original.split(":", 1)
            nome_label = partes_label[0].strip()
            # valida label
            if not nome_label:
                print(f"ERRO: label inválido em {linha_str_original}")
                exit(1)
            if nome_label in labels:
                print(f"ERRO: declaração de label {nome_label} duplicada!")
                exit(1)

            # guarda no dicionario
            nome_label = nome_label.upper()
            labels[nome_label] = rastreio_pos
            linha_str = partes_label[1].strip()
            if not linha_str:
                continue

        # se tiver instrucao
        if linha_str:
            resultado_ler_comando = lerComando(linha_str)
            if resultado_ler_comando:
                instrucao_obj_lida, flag_facilitador = resultado_ler_comando
                instrucoes_reais = expandir_pseudo_instrucao(instrucao_obj_lida, flag_facilitador)
                for instrucao in instrucoes_reais:
                    rastreio_pos += tamanho_instrucao(instrucao)
                if rastreio_pos > RAM_SIZE:
                    print(f"ERRO: Código excedeu o tamanho máximo da RAM ({RAM_SIZE} bytes)!")
                    exit(1)
            else:
                continue
    return labels

def segundaPassagem(input_file_content, labels):
    """ --- SEGUNDA PASSAGEM --- 
    gera bytecode para as instruções já expandidas)
    """
    pos = 0
    for linha_str in input_file_content:
        linha_str = linha_str.strip()
        if not linha_str or linha_str.startswith(";"):
            continue

        tmp_linha_str = linha_str
        if ":" in tmp_linha_str:
            tmp_linha_str = tmp_linha_str.split(":",1)[1].strip()
            if not tmp_linha_str:
                continue
        if tmp_linha_str:
            resultado_ler_comando = lerComando(tmp_linha_str)
            if resultado_ler_comando:
                instrucao_obj, flag_facilitador = resultado_ler_comando
                instrucoes_expandidas = expandir_pseudo_instrucao(instrucao_obj, flag_facilitador)

                for instrucao in instrucoes_expandidas:
                    if (instrucao.comando.startswith("J") and
                        instrucao.comando != "JMPR" and
                        instrucao.op1 and instrucao.op1 in labels):
                        instrucao.op1 = str(labels[instrucao.op1])
                    elif instrucao.comando == "HALT":
                        instrucao.comando = "JMP"
                        instrucao.bytecode = comandos_jumpers["JMP"]
                        instrucao.op1 = str(pos)
                    geraByteCode(instrucao,ram,pos)
                    pos+= tamanho_instrucao(instrucao)
                    if len(ram) > RAM_SIZE:
                        print(f"ERRO: Código excedeu o tamanho máximo da RAM ({RAM_SIZE} bytes)!")
                        exit(1)

# funcao principal
def main():
    """ função principal do programa, faz a montagem """
    input_file, output_file = init()
    input_file_content = input_file.readlines()
    input_file.close()

    labels = primeiraPassagem(input_file_content)
    segundaPassagem(input_file_content, labels)
    
    salva(ram, output_file)
    print(f"Processado com sucesso, arquivo salvo em {sys.argv[2]}")
    output_file.close()
    exit(0)
    
main()