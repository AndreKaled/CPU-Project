data r0 7 ; guarda dados no vetor (este é n de vet[1..n])

data r1 0xff ; decremento

data r2 0xff ; controla a memoria (vai até o inicio do vetor)

data r3 0x00 ; para comparar qnd chegar no fim da insercao

st r2 r0 ; loop de insercao
add r1 r0
clf
add r1 r2
clf
cmp r0 r0
jz 0x12

jmp 0x08

data r3 0x00

add r2 r3 ; r3 é o ponteiro pro inicio
data r2 0xff ; r2 é o ponteiro pro final

data r1 0x01

add r1 r3 ; para estar na posicao certa
clf
cmp r2 r3
ja 0x20 ; aqui tem que comecar a trocar

jmp 0x1e ; loop de fim do programa

; trocas do vetor
ld r3 r0 ; carrega x em r0 (inicio)
ld r2 r1 ; carrega y em r1 (fim)
st r3 r1 ; salva y em r3 (inicio)
st r2 r0 ; salva x em r2 (fim)

data r0 0x01 ; 1 para somar no ponteiro inicio

data r1 0xff ; -1 para tirar do ponteiro fim

clf
add r0 r3
clf
add r1 r2
jmp 0x1a; repete