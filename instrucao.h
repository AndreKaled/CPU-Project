#ifndef INSTRUCAO_H
#define INSTRUCAO_H

typedef struct Instrucao {
    char comando[6];
    char op1[3];
    char op2[3];
} Instrucao;
#endif