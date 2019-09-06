import esp32

print(esp32.hall_sensor())     # read the internal hall sensor, lit le capteur de hall interne
print(esp32.raw_temperature()) # read the internal temperature of the MCU, in Farenheit
print(esp32.ULP())            # access to the Ultra-Low-Power Co-processor
