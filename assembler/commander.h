#ifndef COMMANDER_H
#define COMMANDER_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include "instrucao.h"

#define INIT_CODE "v3.0 hex words plain\n"
#define FILE_INPUT "input.asm"
#define FILE_OUTPUT "output.txt"
#define FILE_MODE "a"

FILE *input;
FILE *output;

char init();

Instrucao lerComando(char linha[64]);

void salva(unsigned char dados[], int pos, int tam);
#endif