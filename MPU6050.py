#Auteur : Pascal Tikeng
# Note : 
"""
* Un accéléromètre mesure l'accélération correcte, c'est-à-dire le taux de changement de vitesse par rapport 
à sa propre base de repos. Cela contraste avec l'accélération de coordonnées, qui est relative à un système
de coordonnées fixe. Le résultat pratique en est qu’au repos sur la Terre, un accéléromètre mesurera 
l’accélération due à la gravité de la Terre, de g ≈ 9,81 m / s. Un accéléromètre en chute libre mesurera 
zéro. Ceci peut être ajusté avec avec calibration.

* Un gyroscope mesure en revanche l'orientation et la vitesse angulaire, ou rotation autour d'un axe. 
La vitesse angulaire sera toujours nulle au repos.

La disponibilité de packs accéléromètre-gyroscope à puce unique bon marché les rend pratiques pour tout projet.
Dans ce projet j'utilise le MPU6050

Dans la suite : 

AcX : Accélération suivant l'axe X
AcY : Accélération selon l'axe Y
AcZ : Accélération selon l'axe Z
GyX : Rotation autour de l'axe X
GyY : Rotation autour de l'axe Y
GyZ : Rotation autour de l'axe Z
Tmp : Température °C

# Accelerometer/Gyroscope values are in int16 range (-32768 to 32767) If the mpu6050 loses power, 
# you have to call init() again
"""

import machine

class mpu6050(object):
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

    #lissage : lisser ces fluctuations aléatoires pour nous laisser de vraies données représentatives.
    #Il s'agit de lire plusieurs valeurs et de prendre la moyenne/médiane de toutes les valeurs. 
    #Le capteur renvoie plusieurs valeurs. Nous devons donc les calculer toutes individuellement.
    def get_smoothed_values(self, n_samples=10):
        """Obtenir des valeurs lissées du capteur par échantillonnage le capteur `n_samples` fois et retourne la moyenne"""
        result = {}
        for _ in range(n_samples):
            data =  self.get_values()

            for key in data.keys():
                # Ajouter de la valeur / des échantillons (pour générer une moyenne)
                # avec la valeur 0 par défaut pour la première boucle.
                result[key] = result.get(key, 0) + (data[key] / n_samples)

        return result
        
    #Etalonnage : si nous prenons un certain nombre de mesures de capteurs répétées dans le temps, 
    #nous pouvons déterminer l'écart type ou moyen par rapport à zéro dans le temps. 
    #Ce décalage peut ensuite être soustrait des mesures futures pour les corriger. 
    #L'appareil doit être au repos et ne pas changer pour que cela fonctionne de manière fiable.
    def calibrate(self, threshold=50, n_samples=100):
        """
        Obtenir la date d'étalonnage du capteur, en mesurant à plusieurs reprises tandis que le capteur est
        stable.  L'étalonnage résultant dictionnaire contient des décalages pour ce capteur dans sa
        position actuelle.
        """
        while True:
            v1 = self.get_smoothed_values(n_samples)
            v2 = self.get_smoothed_values(n_samples)
            # Vérifiez que toutes les mesures consécutives sont dans le seuil. Nous utilisons abs();  
            # donc tous les différences sont positives.
            if all(abs(v1[key] - v2[key]) < threshold for key in v1.keys()):
                return v1  # Calibrated.

    def get_smoothed_values_calibrate(self, n_samples=10, calibration=None):
        """
        Obtenir des valeurs lissées du capteur par échantillonnage le capteur `n_samples` fois et 
        retourne la moyenne. Si passé un dictionnaire `calibration`, soustrayez ces les valeurs 
        de la valeur finale du capteur avant de revenir.
        """    
        result = {}
        for _ in range(n_samples):
            data =  self.get_values()

            for key in data.keys():
                # Add on value / n_samples to produce an average
                # over n_samples, with default of 0 for first loop.
                result[key] = result.get(key, 0) + (data[key] / n_samples)

        if calibration: 
            # Remove calibration adjustment.
            for key in calibration.keys():
                result[key] -= calibration[key]

        return result

    def val_test(self):  # ONLY FOR TESTING! Also, fast reading sometimes crashes IIC
        from time import sleep
        while 1:
            print(self.get_values())
            sleep(0.05)

def main():
    #1
    from machine import I2C, Pin
    mpu = mpu6050(I2C(scl=Pin(5), sda=Pin(4))) # VCC=3V3, GND=GND
    print(mpu.get_values())
    # {'GyZ': 0, 'GyY': 0, 'GyX': 0, 'Tmp': 36.53, 'AcZ': 0, 'AcY': 0, 'AcX': 0} pour mon premier test
    print(mpu.get_smoothed_values())
    print(mpu.calibrate())
    print(mpu.get_smoothed_values_calibrate(n_samples=100, calibration=mpu.calibrate()))

if __name__ == "__main__":
    main()
    









