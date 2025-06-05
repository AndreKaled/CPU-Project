import sys
INIT_CODE = "v3.0 hex words plain\n"

class Instrucao:
    def __init__(self, comando="", op1="", op2=""):
        self.comando = comando
        self.op1 = op1
        self.op2 = op2

def init():
    FILE_INPUT = sys.argv[1]
    FILE_OUTPUT = sys.argv[2]
    try:
        input = open(FILE_INPUT, "r") 
        output = open(FILE_OUTPUT, "w")
        output.write(INIT_CODE)
        return input, output
    except IOError:
        print("ERRO AO INICIAR ARQUIVOS.")
        return None, None

def lerComando(linha):
    linha = linha.upper()
    linha = linha.strip().split(";")
    trecho = linha[0].split()
    comando = trecho[0]
    if len(trecho) > 1:
        op1 = trecho[1]
    else:
        op1 = None
    if len(trecho) > 2:
        op2 = trecho[2] 
    else: 
        op2 = None 
    return Instrucao(comando, op1, op2)

def salva(dados, pos, tam, output_file):
    vet = dados.copy()
    for i in range(pos, tam):
        vet.append(0x00)

    for i in range(tam):
        output_file.write(f"{vet[i]:02x}")
        if (i+1) % 16 == 0:
            output_file.write("\n")
        else:
            output_file.write(" ")
    
    output_file.close()