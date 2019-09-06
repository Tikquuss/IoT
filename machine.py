import machine

# valeurs de frequences possibles : 20MHz, 40MHz, 80Mhz, 160MHz or=u 240MHz
print(machine.freq())          # get the current frequency of the CPU
print(machine.freq(240000000)) # set the CPU frequency to 240 MHz
print(machine.freq())
