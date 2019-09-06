# PWM : pulse width modulation/ modulation de largeur d'impulsion) 
"""
La PWM peut 锚tre activ茅e sur toutes les broches 脿 sortie activ茅e. La fr茅quence de base peut aller
de 1Hz 脿 40 MHz mais il y a un compromis; 脿 mesure que la fr茅quence de base augmente, la r茅solution
en service diminue . Voir LED Control pour plus de d茅tails.
"""

from machine import Pin, PWM

pwm0 = PWM(Pin(0))      # create PWM object from a pin
pwm0.freq()             # get current frequency
pwm0.freq(1000)         # set frequency
pwm0.duty()             # get current duty cycle / obtenir le cycle de service actue
pwm0.duty(200)          # set duty cycle / cycle de service d茅fini
pwm0.deinit()           # turn off PWM on the pin / d茅sactive PWM sur la broche

pwm2 = PWM(Pin(2), freq=20000, duty=512) # create and configure in one go
