#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "instrucao.h"
#include "commander.h"

#define RAM_SIZE 256
unsigned char ram[RAM_SIZE];
int pos = 0;

typedef struct {
    const char *nome;
    unsigned char baseOpcode;
    char usaSegundoByte;  // 0 = não, 1 = sim
} MapaComando;

MapaComando comandos[] = {
    {"LD",    0x00, 0},
    {"ST",    0x10, 0},
    {"DATA",  0x20, 1},
    {"JMPR",  0x30, 0},
    {"JMP",   0x40, 1},
    {"JC",    0x50, 1}, {"JA",    0x54, 1}, {"JE",    0x52, 1}, {"JZ",    0x51, 1},
    {"JCA",   0x5C, 1}, {"JCE",   0x5A, 1}, {"JCZ",   0x59, 1}, {"JAE",   0x56, 1},
    {"JAZ",   0x55, 1}, {"JEZ",   0x53, 1}, {"JCAE",  0x5E, 1}, {"JCAZ",  0x5D, 1},
    {"JCEZ",  0x5B, 1}, {"JAEZ",  0x57, 1}, {"JCAEZ", 0x5F, 1},
    {"CLF",   0x60, 0},
    {"IN",    0x70, 0},
    {"OUT",   0x78, 0},
    {"ADD",   0x80, 0}, 
    {"SHR",   0x90, 0}, 
    {"SHL",   0xA0, 0}, 
    {"NOT",   0xB0, 0},
    {"AND",   0xC0, 0}, 
    {"OR",    0xD0, 0}, 
    {"XOR",   0xE0, 0}, 
    {"CMP",   0xF0, 0}
};

unsigned char regToNum(const char *reg) {
    if (strlen(reg) != 2 || reg[0] != 'R' || reg[1] < '0' || reg[1] > '3') {
        printf("Registrador inválido: %s\n", reg);
        exit(1);
    }
    return reg[1] - '0';
}

MapaComando *buscaComando(const char *nome) {
    int total = sizeof(comandos) / sizeof(comandos[0]);
    for (int i = 0; i < total; i++) {
        if (strcmp(comandos[i].nome, nome) == 0)
            return &comandos[i];
    }
    return NULL;
}

void geraBytecode(Instrucao in) {
    MapaComando *cmd = buscaComando(in.comando);
    if (!cmd) {
        printf("Comando desconhecido: %s\n", in.comando);
        exit(1);
    }

    unsigned char byte1 = cmd->baseOpcode;
    unsigned char byte2 = 0x00;

    if (strcmp(in.comando, "LD") == 0 || strcmp(in.comando, "ST") == 0 ||
        strcmp(in.comando, "ADD") == 0 || strcmp(in.comando, "SHR") == 0 ||
        strcmp(in.comando, "SHL") == 0 || strcmp(in.comando, "NOT") == 0 ||
        strcmp(in.comando, "AND") == 0 || strcmp(in.comando, "OR") == 0 ||
        strcmp(in.comando, "XOR") == 0 || strcmp(in.comando, "CMP") == 0) {
        
        byte1 |= (regToNum(in.op1) << 2) | regToNum(in.op2);

    } else if (strcmp(in.comando, "DATA") == 0) {
        byte1 |= regToNum(in.op1);
        byte2 = (unsigned char) strtol(in.op2, NULL, 16);

    } else if (strcmp(in.comando, "IN") == 0 || strcmp(in.comando, "OUT") == 0) {
        unsigned char tipo = (unsigned char) strtol(in.op1, NULL, 16);
        unsigned char reg = regToNum(in.op2);
        
        if (tipo == 0x11) {  // caso especial: ativação
            byte1 |= 0x0C | reg;  // 0111 11RB
        } else {
            byte1 |= (tipo << 2) | reg;  // 0111 TT RB
        }
    }
    else if (cmd->usaSegundoByte) {
        byte2 = (unsigned char) strtol(in.op1, NULL, 16);
    }

    ram[pos++] = byte1;
    if (cmd->usaSegundoByte)
        ram[pos++] = byte2;
}

int main() {
    if (!init()) return 1;

    char linha[64];
    while (fgets(linha, sizeof(linha), input)) {
        linha[strcspn(linha, "\n")] = 0;
        Instrucao in = lerComando(linha);

        if (strlen(in.comando) == 0) continue;

        geraBytecode(in);
    }
    salva(ram, pos, RAM_SIZE);
    return 0;
}
