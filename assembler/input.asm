data r0,0x30 ; comentário: dado hexadecimal 

DATA r1, 06  ; dado em decimal

DATA r1, -06  ; dado em decimal



dAta r2,0b00001000 ; dado binário

  data r3,0xff



; comentário 2

shr R0,R1    

shl   r3,r2

not r3, r0

and r0,R1

or  r2,r1

xor  r2,r1

Add r2,r0



ld r0,r1

st r3,r1



;comentario 3

clf     



cmp r1,r2



jmpr r3

jmp  0xf0



jc 0xb0

ja 0xb0

 je 0b00001111

jz 0xb0

jca 0xb0

jce 0xb0

jcz 0xb0

jcae 0xb0

jcaz 0xb0

jcez 0xb0

jcaez 0xb0

jae 0x02

jaz 0x02

jaez 0x02

jez 0x33



; I/O instructions

in data,r0

IN addr,r1

out data,r2

out addr,r3 