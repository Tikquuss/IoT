#Simple library for MPU6050 on ESP8266 with micropython

"""
*Un accéléromètre mesure l'accélération correcte, c'est-à-dire le taux de changement de vitesse par rapport 
à sa propre base de repos. Cela contraste avec l'accélération de coordonnées, qui est relative à un système
de coordonnées fixe. Le résultat pratique en est qu’au repos sur la Terre, un accéléromètre mesurera 
l’accélération due à la gravité de la Terre, de g ≈ 9,81 m / s. Un accéléromètre en chute libre mesurera 
zéro. Ceci peut être ajusté avec avec calibration.
*Un gyroscope mesure en revanche l'orientation et la vitesse angulaire, ou rotation autour d'un axe. 
La vitesse angulaire sera toujours nulle au repos.

La disponibilité de packs accéléromètre-gyroscope à puce unique bon marché les rend pratiques pour 
tout projet.

Dans la suite : 

AcX : Accélération suivant l'axe X
AcY : Accélération selon l'axe Y
AcZ : Accélération selon l'axe Z
GyX : Rotation autour de l'axe X
GyY : Rotation autour de l'axe Y
GyZ : Rotation autour de l'axe Z
Tmp : Température °C
"""

import machine

class accel():
    def __init__(self, i2c, addr=0x68):
        self.iic = i2c
        self.addr = addr
        self.iic.start()
        self.iic.writeto(self.addr, bytearray([107, 0]))
        self.iic.stop()

    def get_raw_values(self):
        self.iic.start()
        a = self.iic.readfrom_mem(self.addr, 0x3B, 14)
        self.iic.stop()
        return a

    def get_ints(self):
        b = self.get_raw_values()
        c = []
        for i in b:
            c.append(i)
        return c

    def bytes_toint(self, firstbyte, secondbyte):
        if not firstbyte & 0x80:
            return firstbyte << 8 | secondbyte
        return - (((firstbyte ^ 255) << 8) | (secondbyte ^ 255) + 1)

    def get_values(self):
        raw_ints = self.get_raw_values()
        vals = {}
        vals["AcX"] = self.bytes_toint(raw_ints[0], raw_ints[1])
        vals["AcY"] = self.bytes_toint(raw_ints[2], raw_ints[3])
        vals["AcZ"] = self.bytes_toint(raw_ints[4], raw_ints[5])
        vals["Tmp"] = self.bytes_toint(raw_ints[6], raw_ints[7]) / 340.00 + 36.53
        vals["GyX"] = self.bytes_toint(raw_ints[8], raw_ints[9])
        vals["GyY"] = self.bytes_toint(raw_ints[10], raw_ints[11])
        vals["GyZ"] = self.bytes_toint(raw_ints[12], raw_ints[13])
        return vals  # returned in range of Int16
        # -32768 to 32767

    #lissage : lisser ces fluctuations al茅atoires pour nous laisser de vraies donn茅es repr茅sentatives.
    #Lire plusieurs valeurs et de prendre la moyenne/m茅diane de toutes les valeurs. 
    #Le capteur renvoie plusieurs valeurs. Nous devons donc les calculer toutes individuellement.
    def get_smoothed_values(n_samples=10):
        """Obtenir des valeurs liss茅es du capteur par 茅chantillonnage le capteur `n_samples` fois et retourne la moyenne"""
        result = {}
        for _ in range(samples):
            data = accel.get_values()

            for key in data.keys():
                # Add on value / samples (to generate an average)
                # with default of 0 for first loop.
                # Ajouter de la valeur / des échantillons (pour générer une moyenne)
                # avec la valeur 0 par défaut pour la première boucle.
                result[m] = result.get(m, 0) + (data[m] / samples)

        return result

    #脡talonnage : si nous prenons un certain nombre de mesures de capteurs r茅p茅t茅es dans le temps, 
    #nous pouvons d茅terminer l'茅cart type ou moyen par rapport 脿 z茅ro dans le temps. 
    #Ce d茅calage peut ensuite 锚tre soustrait des mesures futures pour les corriger. 
    #L'appareil doit 锚tre au repos et ne pas changer pour que cela fonctionne de mani猫re fiable.
    def calibrate(threshold=50, n_samples=100):
        """
        Obtenir la date d'茅talonnage du capteur, en mesurant 脿 plusieurs reprises tandis que le capteur est
        stable.  L'茅talonnage r茅sultant dictionnaire contient des d茅calages pour ce capteur dans sa
        position actuelle.
        """
        while True:
            v1 = get_accel(n_samples)
            v2 = get_accel(n_samples)
            # Check all consecutive measurements are within the threshold. We use abs() so all calculated 
            # differences are positive.
            # Vérifiez que toutes les mesures consécutives sont dans le seuil.  Nous utilisons abs() 
            #donc tous calculés Les différences sont positives.
            if all(abs(v1[key] - v2[key]) < threshold for key in v1.keys()):
                return v1  # Calibrated.

    def get_smoothed_values_calibrate(n_samples=10, calibration=None):
        """
        Obtenir des valeurs lissées du capteur par échantillonnage le capteur `n_samples` fois et 
        retourne la moyenne. Si passé un dictionnaire `calibration`, soustrayez ces les valeurs 
        de la valeur finale du capteur avant de revenir.
        """    
        result = {}
        for _ in range(n_samples):
            data = accel.get_values()

            for key in data.keys():
                # Add on value / n_samples to produce an average
                # over n_samples, with default of 0 for first loop.
                result[m] = result.get(m, 0) + (data[m] / samples)

        if calibration: 
            # Remove calibration adjustment.
            for key in calibration.keys():
                result[m] -= calibration[m]

        return result

    def val_test(self):  # ONLY FOR TESTING! Also, fast reading sometimes crashes IIC
        from time import sleep
        while 1:
            print(self.get_values())
            sleep(0.05)

def main():
    #1
    from machine import I2C, Pin
    i2c = I2C(scl=Pin(5), sda=Pin(4)) # VCC=3V3, GND=GND
    accelerometer = accel(i2c)
    accelerometer.get_values()
    #2
    calibration = calibrate()
    while True:
        data = get_smoothed_values(n_samples=100, calibration=calibration)
        print(
            '\t'.join('{0}:{1:>10.1f}'.format(k, data[k])
            for k in sorted(data.keys())),
        end='\r'

if __name__ == "__main__":
    main()
    

# {'GyZ': -235, 'GyY': 296, 'GyX': 16, 'Tmp': 26.64764, 'AcZ': -1552, 'AcY': -412, 'AcX': 16892}
# Accelerometer/Gyroscope values are in int16 range (-32768 to 32767) If the mpu6050 loses power, 
# you have to call init() again





