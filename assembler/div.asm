input_dividendo:
    data r0 0x00
    out addr r0
    in data r2          ; lê caractere ASCII em r2

    data r1 0x2f          ; caractere '/'
    cmp r2 r1
    je init_divisor ; computa o divisor
    jmp mult_10 ; desloca o dividendo e continua "pegando" o dividendo

trata_digito:
    data r1 0xd0        ; -48 para o ASCII
    clf
    add r1 r2           ; r2 = r2 - 48 → valor do dígito (0–9)
    clf
    add r2 r3           ; r3 = r3 + dígito
    jmp input_dividendo

mult_10:
    move r3 r0 ; r0 = r3
    clr r3
    clf
    clr r1
    add r0 r1 ; r1 = r3
    clf
    shl r1 r1 ; r1 = 2*r3 
    shl r0 r0 ; r0 = 2*r3
    shl r0 r0 ; r0 = 4*r3
    shl r0 r0 ; r0 = 8*r3
    add r0 r3
    clf
    add r1 r3 ; contem o resultado * 10
    clf
    jmp trata_digito

init_divisor:
    data r0 0xff
    st r0 r3
    clr r3
    
    jmp input_divisor

input_divisor:
    data r0 0x00
    out addr r0
    in data r2          ; lê caractere ASCII em r2
    data r1 0x0a        ; caractere 'Enter'
    cmp r2 r1
    je divide ; output da entrada, computa o divisor
    jmp mult_10_divisor ; desloca o dividendo e continua "pegando" o dividendo


mult_10_divisor:
    move r3 r0 ; r0 = r3
    clr r3
    clf
    clr r1
    add r0 r1 ; r1 = r3
    clf
    shl r1 r1 ; r1 = 2*r3 
    shl r0 r0 ; r0 = 2*r3
    shl r0 r0 ; r0 = 4*r3
    shl r0 r0 ; r0 = 8*r3
    add r0 r3
    clf
    add r1 r3 ; contem o resultado * 10
    clf
    jmp trata_digito_divisor

trata_digito_divisor:
    data r1 0xd0        ; -48 para o ASCII
    clf
    add r1 r2           ; r2 = r2 - 48 → valor do dígito (0–9)
    clf
    add r2 r3           ; r3 = r3 + dígito
    jmp input_divisor 

divide:
    move r3 r1     ; r1 está com o divisor
    data r3 0x00
    cmp r1 r3
    je erro
    clr r3         ; zera r3

loop_div:
    data r0 0xFF
    ld r0 r0       ; r0 = dividendo atual
    data r2 0x00
    cmp r0 r2
    je output         ; se dividendo é zero, acabou

    cmp r1 r0
    ja output         ; se dividendo < divisor, acabou

    jmp subtrai


subtrai:
    clr r2     
    clf
    add r1 r2      ; r2 = divisor (nao altera r1)
    clf
    not r2 r2      ; r2 = not divisor
    data r0 0x01
    add r0 r2      ; r2 = -divisor
    clf
    data r0 0xFF
    ld r0 r0       ; r0 = dividendo atual
    add r2 r0      ; r0 = dividendo - divisor
    clf

    data r2 0xFF
    st r2 r0       ; atualiza dividendo

    data r0 0x01
    add r0 r3      ; quociente++
    clf

    jmp loop_div

output:
    ; r3 = quociente (0–99)
    ; r1 = contador de dezenas
    clr r1           ; r1 = 0
    DATA R0 09
    data r1 0x01
    CLF
    CMP R3 R0
    JA dezenas

    DATA R0 0x30

    CLF
    ADD R0 R3
    OUT addr R1
    OUT addr R3
    halt
dezenas:
    DATA R0 0xf6

    ADD R0 R3
    CLF

    ADD R1 R2
    CLF
    DATA R0 09

    CMP R3 R0
    JA dezenas

    DATA R0 0x30

    CLF
    ADD R0 R3
    CLF
    ADD R0 R2
    OUT addr R1
    OUT addr R2
    OUT addr r1
    OUT addr R3
    halt

erro:
data r1 0x01
data r0 0x58
out addr r1
out addr r0
halt