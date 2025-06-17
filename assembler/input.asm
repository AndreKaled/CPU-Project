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

ld r3 r0 ; carrega x em r0
ld r2 r1 ; carrega y em r1
st r2 r3 ; guarda ponteiro Pinicio no final (onde vai ter a troca)
data r3 0x00 ; limpa para tmp

; troca r0 com r1
add r0 r3 
data r0 0x00

add r1 r0
data r1 0x00

add r3 r1

ld r2 r3 ; carrega ponteiro Pinicio em r3 de volta
; salva a troca
st r3 r0
st r2 r1

; subtrai 1 do ponteiro Pfinal e soma 1 do ponteiro Pinicio
data r0 0x01

add r0 r3
data r1 0xff

add r1 r2

jmp 0x0f; repete