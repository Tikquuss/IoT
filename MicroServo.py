# coding: utf-8

try:
    from machine import Pin, PWM
except ImportError:
    raise ImportError("python-machine.Pin or python-machine.PWM not found")
    
class Servo(object):
    _angle = 0
    _pin = 13
    _frequence = 50

    def __init__(self, angle, pin=13, frequence=50):
        self._angle=angle
        self._pin=pin
        self._frequence=frequence
    
    def _get_angle(self):
        return self._angle

    def _set_angle(self, angle):
        self._angle = angle

    angle=property(_get_angle, _set_angle)
    
    def _get_pin(self):
        return self._pin

    def _set_pin(self, pin):
        self._pin = pin

    pin=property(_get_pin, _set_pin)
    
    def _get_frequence(self):
        return self._frequence

    def _set_frequence(self, frequence):
        self._frequence = frequence

    frequence=property(_get_frequence, _set_frequence)
    
    def turn(self) :
        """Fonction qui place le servo connect茅 au pin 脿 une position de angle degr茅e"""
        servo = PWM(Pin(self._pin), self._frequence)
        servo.duty(self._angle)

  






