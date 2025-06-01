# Makefile para o algoritmo asm -> hex

# diretórios
SRC_DIR = assembler
BIN_DIR = bin

# arquivos (pega todos os .c na pasta assembler)
SRC = $(wildcard $(SRC_DIR)/*.c)
OUT = $(BIN_DIR)/assembler

# compilador e flags
CC = gcc
CFLAGS = -Wall -Wextra -O2

# targets
all: $(OUT)

$(OUT): $(SRC)
	@if not exist $(BIN_DIR) mkdir $(BIN_DIR)
	$(CC) $(CFLAGS) -o $(OUT) $(SRC)
	@echo "Build completo: $(OUT)"

clean:
	if exist $(BIN_DIR) rmdir /S /Q $(BIN_DIR)
	@echo "limpeza concluida."

run: all
	./$(OUT) programa.asm output.hex
