import file_controller as fc

RAM_SIZE = 256
pos = 0
ram = [0x00] * RAM_SIZE
class MapaComando:
    def __init__(self, nome="", baseOpCode="", usaSegundobyte=""):
        self.nome = nome
        self.baseOpCode = baseOpCode
        self.usaSegundoByte = usaSegundobyte

comandos = [
    MapaComando("LD",   0x00, 0),
    MapaComando("ST",   0x10, 0),
    MapaComando("DATA", 0x20, 1),
    MapaComando("JMPR", 0x30, 0),
    MapaComando("JMP",  0x40, 1),
    MapaComando("JC",   0x50, 1),MapaComando("JA",  0x54, 1),MapaComando("JE",    0x52, 1),MapaComando("JC",   0x51, 1),
    MapaComando("JCA",  0x5C, 1),MapaComando("JCE", 0x5A, 1),MapaComando("JCZ",   0x59, 1),MapaComando("JAE",  0x56, 1),
    MapaComando("JAZ",  0x55, 1),MapaComando("JEZ", 0x53, 1),MapaComando("JCAE",  0x5E, 1),MapaComando("JCAZ", 0x5D, 1),
    MapaComando("JCEZ", 0x5B, 1),MapaComando("JAEZ",0x57, 1),MapaComando("JCAEZ", 0x5F, 1),
    MapaComando("CLF",  0x60, 0),
    MapaComando("IN",   0x70, 0),
    MapaComando("OUT",  0x78, 0),
    MapaComando("ADD",  0x80, 0), 
    MapaComando("SHR",  0x90, 0), 
    MapaComando("SHL",  0xA0, 0), 
    MapaComando("NOT",  0xB0, 0),
    MapaComando("AND",  0xC0, 0), 
    MapaComando("OR",   0xD0, 0), 
    MapaComando("XOR",  0xE0, 0), 
    MapaComando("CMP",  0xF0, 0)
]

def regToNum(reg=""):
    if (len(reg) != 2) or (reg[0] != 'R') or not reg[1].isdigit() or (int(reg[1]) < 0) or(int(reg[1]) > 3):
        print("Registrador inválido: ", reg)
        exit(1)
    return int(reg[1])

def buscaComando(nome=""):
    for comando in comandos:
        if(comando.nome == nome):
            return comando
    return None

def geraByteCode(instrucao, ram, pos):
    cmd = buscaComando(instrucao.comando)
    if cmd == None:
        print("Comando inválido: ", instrucao.comando)
        exit(1)
        
    byte1 = cmd.baseOpCode
    byte2 = 0x00
    if (instrucao.comando == "LD" or instrucao.comando == "ST" or 
        instrucao.comando == "ADD" or instrucao.comando == "SHR" or 
        instrucao.comando == "SHL" or instrucao.comando == "NOT" or 
        instrucao.comando == "AND" or instrucao.comando == "OR" or 
        instrucao.comando == "XOR" or instrucao.comando == "CMP"):
        byte1 |= (regToNum(instrucao.op1) << 2) | regToNum(instrucao.op2)
    elif instrucao.comando == "DATA": # data usa 2 bytes
        byte1 |= regToNum(instrucao.op1)
        byte2 = int(instrucao.op2, 16)
    elif instrucao.comando == "IN" or instrucao.comando == "OUT":
        tipo = int(instrucao.op1, 16)
        reg = regToNum(instrucao.op2)
        # caso de ativacao
        if tipo == 0x11:
            byte1 |= 0x0c | reg # 0111 11RB
        else:
            byte1 |= (tipo << 2) | reg #0111 TTRB
    elif cmd.usaSegundoByte == 1: # para jumps 
        byte2 = int(instrucao.op1, 16)
        
    #modifica a "RAM"
    ram[pos] = byte1
    pos = pos + 1
    if(cmd.usaSegundoByte == 1):
        ram[pos] = byte2
        pos = pos + 1
    return pos

def main():
    input_file, output_file = fc.init()
    if input_file == None or output_file == None:
        exit(1)
    
    pos = 0
    for linha in input_file:
        linha = linha.strip()
        instrucao = fc.lerComando(linha)
        if len(instrucao.comando) == 0:
            continue
        pos = geraByteCode(instrucao, ram, pos)
    
    fc.salva(ram, pos, RAM_SIZE, output_file)
    exit(0)
    
main()