; guarda dados no vetor
data r0 1

data r1 1 

data r2 0x30 ; controla a memoria (posicao do vetor), marca o fim do vetor

; guarda ate acabar as instrucoes abaixo
add r2 r3 ; R3 marca o inicio do vetor
st r2 r0 ; guarda 1
add r1 r0
add r1 r2
st r2 r0 ; guarda 2
add r1 r0
add r1 r2
st r2 r0 ; guarda 3

clf
cmp r2 r3
ja 0x14 ; aqui tem que comecar a trocar

jmp 0x12 ; loop de fim do programa

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
jmp 0x0f; repete