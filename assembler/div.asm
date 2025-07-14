input_dividendo:
    data r0 0x00
    out addr r0
    in data r2          ; Le caractere ASCII do dividendo (um digito ou '/')

    data r1 0x2f        ; ASCII de '/'
    cmp r2 r1
    je init_divisor     ; Se achou '/', começa leitura do divisor
    jmp mult_10         ; senao, multiplica acumulado por 10 e continua lendo

trata_digito:
    data r1 0xd0        ; -48 converte ASCII para numero
    clf
    add r1 r2           ; r2 = r2 - 48 (valor do digito)
    clf
    add r2 r3           ; Acumula valor em r3 (valor total do dividendo)
    jmp input_dividendo ; Continua lendo o proximo digito

mult_10:
    ; Multiplica r3 por 10 usando shifts (r3 *= 10)
    move r3 r0
    clr r3
    clf
    clr r1
    add r0 r1
    clf
    shl r1 r1           ; r1 = 2*r3
    shl r0 r0           ; r0 = 8*r3
    shl r0 r0
    shl r0 r0
    add r0 r3
    clf
    add r1 r3           ; r3 = 10*r3
    clf
    jmp trata_digito

init_divisor:
    data r0 0xff
    st r0 r3            ; Salva dividendo da memoria em r3
    clr r3              ; Zera r3 para acumular o divisor
    jmp input_divisor

input_divisor:
    data r0 0x00
    out addr r0
    in data r2          ; Le caractere do divisor
    data r1 0x0a        ; ASCII de 'Enter'
    cmp r2 r1
    je divide           ; Se 'Enter', inicia divisao
    jmp mult_10_divisor

mult_10_divisor:
    ; Multiplica r3 por 10, igual ao dividendo
    move r3 r0
    clr r3
    clf
    clr r1
    add r0 r1
    clf
    shl r1 r1
    shl r0 r0
    shl r0 r0
    shl r0 r0
    add r0 r3
    clf
    add r1 r3
    clf
    jmp trata_digito_divisor

trata_digito_divisor:
    data r1 0xd0
    clf
    add r1 r2           ; ASCII para numero
    clf
    add r2 r3           ; Acumula valor em r3 (divisor)
    jmp input_divisor

divide:
    move r3 r1          ; Guarda divisor em r1
    data r3 0x00
    cmp r1 r3
    je erro             ; Divisao por zero

    clr r3              ; Zera quociente (r3)

loop_div:
    data r0 0xFF
    ld r0 r0            ; Le dividendo da memoria
    data r2 0x00
    cmp r0 r2
    je output           ; Se dividendo == 0, fim

    cmp r1 r0
    ja output           ; Se divisor > dividendo, fim

    jmp subtrai         ; Realiza subtracao

subtrai:
    ; r0 = r0 - r1 usando complemento de dois
    clr r2
    clf
    add r1 r2
    clf
    not r2 r2
    data r0 0x01
    add r0 r2           ; r2 = -r1
    clf

    data r0 0xFF
    ld r0 r0
    add r2 r0           ; r0 = dividendo - divisor
    clf

    data r2 0xFF
    st r2 r0            ; Atualiza dividendo

    data r0 0x01
    add r0 r3           ; quociente++
    clf

    jmp loop_div

output:
    ; Exibe o quociente contido em r3
    clr r1              ; Usado para checar se r3 >= 10
    DATA R0 09
    data r1 0x01
    CLF
    CMP R3 R0
    JA dezenas          ; Se r3 > 9, converte para duas casas

    DATA R0 0x30        ; ASCII de '0'
    CLF
    ADD R0 R3           ; Converte para ASCII
    OUT addr R1
    OUT addr R3
    halt

dezenas:
    ; Converte r3 para dois digitos ASCII
    DATA R0 0xf6        ; r0 = -10
    ADD R0 R3           ; r3 -= 10
    CLF

    ADD R1 R2           ; r2 += 1 (dezenas)
    CLF
    DATA R0 09
    CMP R3 R0
    JA dezenas          ; Repete enquanto r3 > 9

    DATA R0 0x30
    CLF
    ADD R0 R3
    CLF
    ADD R0 R2           ; r2 = unidade em ASCII

    OUT addr R1         ; Dezena (r1 = '1')
    OUT addr R2         ; Unidade (r2)
    OUT addr r1
    OUT addr R3         
    halt

erro:
    data r1 0x01
    data r0 0x58        ; Letra 'X'
    out addr r1
    out addr r0         ; Mostra 'X' como erro de divisao por zero
    halt
