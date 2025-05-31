#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include "instrucao.h"

#define INIT_CODE "v3.0 hex words plain\n"
#define FILE_INPUT "input.asm"
#define FILE_OUTPUT "output.txt"

FILE *input;
FILE *output;

char init() {
    input = fopen(FILE_INPUT, "r");
    output = fopen(FILE_OUTPUT, "w");
    if (!input || !output) {
        printf("ERRO AO INICIAR ARQUIVOS.\n");
        return 0;
    }
    fprintf(output, INIT_CODE);
    return 1;
}

Instrucao lerComando(char linha[64]) {
    Instrucao in;
    memset(&in, 0, sizeof(Instrucao));
    sscanf(linha, "%5[A-Z] %3s %3s", in.comando, in.op1, in.op2);
    return in;
}

void salva(unsigned char dados[], int pos, int tam){
    for(int i = pos; i < tam; i++){
        dados[i] = 0x00;
    }

    for(int i = 0; i < tam; i++){
        fprintf(output, "%02X", dados[i]);
        if((i+1) % 16 == 0)
            fprintf(output, "\n");
        else
            fprintf(output, " ");
    }
    fclose(input);
    fclose(output);
}