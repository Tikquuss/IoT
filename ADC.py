#ADC : analog to digital conversion /conversion analogique-numérique 
"""
La fonctionnalité ESP32 ADC est disponible sur les broches 32-39. 
Notez que, lors de l'utilisation de la configuration par défaut, 
les tensions d'entrée sur la broche ADC doivent être comprises entre 0,0v et 1,0v 
(tout ce qui est supérieur à 1,0 v sera simplement 4095). 
Une atténuation doit être appliquée pour augmenter cette plage de tension utilisable.
"""
from machine import ADC

adc = ADC(Pin(32))          # create ADC object on ADC pin
adc.read()                  # read value, 0-4095 across voltage range 0.0v - 1.0v
							# valeur lue, 0-4095 sur la plage de tension 0,0v - 1,0v
adc.atten(ADC.ATTN_11DB)    # set 11dB input attentuation (voltage range roughly 0.0v - 3.6v)
							# régler l'atténuation d'entrée 11dB (plage de tension d'environ 0,0v à 3,6v)
adc.width(ADC.WIDTH_9BIT)   # set 9 bit return values (returned range 0-511)
adc.read()                  # read value using the newly configured attenuation and width

"""
Référence de méthode de classe ADC spécifique à ESP32:

- ADC.atten ( atténuation ) : Cette méthode permet de régler l’amortissement sur l’entrée 
  du CAN. Cela permet une plage de tension d'entrée possible plus large, au détriment de
  la précision (le même nombre de bits représente désormais une plage plus large). 
  Les options d'atténuation possibles sont les suivantes:

  ADC.ATTN_0DB : atténuation de 0 dB, donne une tension d'entrée maximale de 1,00 V - il s'agit de la configuration par défaut
  ADC.ATTN_2_5DB : atténuation de ADC.ATTN_2_5DB, donne une tension d'entrée maximale d'environ 1,34 V
  ADC.ATTN_6DB : atténuation de 6 dB, donne une tension d'entrée maximale d'environ 2,00 v
  ADC.ATTN_11DB : atténuation de 11 dB, donne une tension d'entrée maximale d'environ 3,6 V
 
 Attention : Malgré une atténuation de 11 dB permettant une plage allant jusqu’à 3,6 v, notez que la 
 tension nominale maximale absolue pour les broches d’entrée est de 3,6 v et que, par conséquent, 
 le fait de s’approcher de cette limite peut endommager le circuit intégré!

- ADC.width(largeur) : Cette méthode permet de définir le nombre de bits à utiliser et à renvoyer 
  lors des lectures ADC. Les options de largeur possibles sont:

 ADC.WIDTH_9BIT : données 9 bits
 ADC.WIDTH_10BIT : données 10 bits
 ADC.WIDTH_11BIT : données 11 bits
 ADC.WIDTH_12BIT : données 12 bits - il s'agit de la configuration par défaut
"""