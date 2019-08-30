# vector3d.py 3D vector class for use in inertial measurement unit drivers
# Authors Peter Hinch, Sebastian Plamauer

import pyb
from math import sqrt, degrees, acos, atan2

def default_wait():
    pyb.delay(50)

class Vector3d(object):
    '''
    Represents a vector in a 3D space using Cartesian coordinates.
    Internally uses sensor relative coordinates.
    Returns vehicle-relative x, y and z values.

    Représente un vecteur dans un espace 3D à l'aide de coordonnées cartésiennes.
    Utilise en interne les coordonnées relatives du capteur.
    Retourne les valeurs x, y et z relatives au véhicule.
    '''
    def __init__(self, transposition, scaling, update_function):
        self._vector = [0,0,0]
        self._ivector = [0,0,0]
        self.cal = (0,0,0)
        self.argcheck(transposition, "Transposition")
        self.argcheck(scaling, "Scaling")
        if (len(transposition) != len(set(transposition))) or min(transposition) < 0 or max(transposition) > 2:
            raise ValueError('Transpose indices must be unique and in range 0-2')
        self._scale = scaling
        self._transpose = transposition
        self.update = update_function

    def argcheck(self, arg, name):
        if len(arg) != 3 or not (type(arg) is list or type(arg) is tuple):
            raise ValueError(name + ' must be a 3 element list or tuple')

    def calibrate(self, stopfunc, waitfunc = default_wait):
        self.update()
        maxvec = self._vector[:]                # Initialise max and min lists with current values
        minvec =self._vector[:]
        while not stopfunc():
            waitfunc()
            self.update()
            maxvec = list(map(max, maxvec, self._vector))
            minvec = list(map(min, minvec, self._vector))
        self.cal = tuple(map(lambda a, b: (a +b)/2, maxvec, minvec))

    @property
    def _calvector(self):                       # Vector adjusted for calibration offsets
        return list(map(lambda val, offset : val - offset, self._vector, self.cal))

    @property
    def x(self):                                # Corrected, vehicle relative floating point values
        self.update()
        return self._calvector[self._transpose[0]] * self._scale[0]

    @property
    def y(self):
        self.update()
        return self._calvector[self._transpose[1]] * self._scale[1]

    @property
    def z(self):
        self.update()
        return self._calvector[self._transpose[2]] * self._scale[2]

    @property
    def xyz(self):
        self.update()
        return (self._calvector[self._transpose[0]] * self._scale[0],
                self._calvector[self._transpose[1]] * self._scale[1],
                self._calvector[self._transpose[2]] * self._scale[2])

    @property
    def magnitude(self):
        x, y, z = self.xyz # All measurements must correspond to the same instant
        return sqrt(x**2 + y**2 + z**2)

    @property
    def elevation(self):
        return 90 - self.inclination

    @property
    def inclination(self):
        x, y, z = self.xyz
        return degrees(acos(z / sqrt(x**2 + y**2 + z**2)))

    @property
    def elevation(self):
        return 90 - self.inclination

    @property
    def azimuth(self):
        x, y, z = self.xyz
        return degrees(atan2(y, x))

    # Raw uncorrected integer values from sensor
    @property
    def ix(self):
        return self._ivector[0]

    @property
    def iy(self):
        return self._ivector[1]

    @property
    def iz(self):
        return self._ivector[2]

    @property
    def ixyz(self):
        return self._ivector
    @property
    def transpose(self):
        return tuple(self._transpose)
    @property
    def scale(self):
        return tuple(self._scale)


'''
mpu9150 is a micropython module for the InvenSense MPU9150 sensor.
It measures acceleration, turn rate and the magnetic field in three axis.

mpu9150 est un module de micropython pour le capteur InvenSense MPU9150.
Il mesure l'accélération, le taux de virage et le champ magnétique sur trois axes.
'''
# 15th June 2015 Now uses subclass of InvenSenseMPU

from imu import InvenSenseMPU, bytes_toint, MPUException
import pyb

def default_mag_wait():
    pyb.delay(1)

# MPU9150 constructor arguments
# 1.    side_str 'X' or 'Y' depending on the Pyboard I2C interface being used
# 2.    optional device_addr 0, 1 depending on the voltage applied to pin AD0 (Drotek default is 1)
#       if None driver will scan for a device (if one device only is on bus)
# 3, 4. transposition, scaling optional 3-tuples allowing for outputs to be based on vehicle
#       coordinates rather than those of the sensor itself. See readme.

# Arguments de constructeur MPU9150
# 1. side_str 'X' ou 'Y' en fonction de l'interface Pyboard I2C utilisée
# 2. facultatif device_addr 0, 1 en fonction de la tension appliquée à la broche AD0 (la valeur par défaut de Drotek est 1)
#  si aucun pilote recherchera un périphérique (si un seul périphérique est sur le bus)
# 3, 4. Transposition, mise à l'échelle de 3 tuples optionnels permettant aux sorties d'être basées sur 
# le véhicule coordonnées plutôt que celles du capteur lui-même. Voir le readme.


class MPU9150(InvenSenseMPU):
    '''
    Module for the MPU9150 9DOF IMU. Pass X or Y according to on which side the
    sensor is connected. Pass 1 for the first, 2 for the second connected sensor.
    By default interrupts are disabled while reading or writing to the device. This
    prevents occasional bus lockups in the presence of pin interrupts, at the cost
    of disabling interrupts for about 250uS.

    Module pour l'IMU MPU9150 9DOF. Passez X ou Y en fonction de quel côté la
    le capteur est connecté. Passez 1 pour le premier, 2 pour le deuxième capteur connecté.
    Par défaut, les interruptions sont désactivées lors de la lecture ou de l'écriture sur le périphérique. 
    Ce empêche les blocages occasionnels du bus en présence d'interruptions de la broche, au prix de
    de désactiver les interruptions pour environ 250uS.
    '''

    _mpu_addr = (104, 105)  # addresses of MPU9150
                            # there can be two devices
                            # connected, first on 104,
                            # second on 105
    _mag_addr = 12
    _chip_id = 104
    def __init__(self, side_str, device_addr = None, transposition = (0,1,2), scaling = (1,1,1)):
        super().__init__(side_str, device_addr, transposition, scaling)
        self._mag = Vector3d(transposition, scaling, self._mag_callback)
        self.filter_range = 0           # fast filtered response
        self._mag_stale_count = 0       # Count of consecutive reads where old data was returned
        self.mag_triggered = False      # Ensure mag is triggered once only until it's read
        self.mag_correction = self._magsetup()  # Returns correction factors.
        self.mag_wait_func = default_mag_wait

    @property
    def sensors(self):
        return self._accel, self._gyro, self._mag

    # get temperature
    @property
    def temperature(self):
        '''
        Returns the temperature in degree C.
        '''
        try:
            self._read(self.buf2, 0x41, self.mpu_addr)
        except OSError:
            raise MPUException(self._I2Cerror)
        return bytes_toint(self.buf2[0], self.buf2[1])/340 + 35 # I think

    # Low pass filters
    @property
    def filter_range(self):
        '''
        Returns the gyro and temperature sensor low pass filter cutoff frequency
        Pass:               0   1   2   3   4   5   6
        Cutoff (Hz):        250 184 92  41  20  10  5
        Sample rate (KHz):  8   1   1   1   1   1   1
        '''
        try:
            self._read(self.buf1, 0x1A, self.mpu_addr)
            res = self.buf1[0] & 7
        except OSError:
            raise MPUException(self._I2Cerror)
        return res

    @filter_range.setter
    def filter_range(self, filt):
        # set range
        if filt in range(7):
            try:
                self._write(filt, 0x1A, self.mpu_addr)
            except OSError:
                raise MPUException(self._I2Cerror)
        else:
            raise ValueError('Filter coefficient must be between 0 and 6')

    @property                   # Triggers mag, waits for it to be ready, then returns the instance
    def mag(self):              # should be ready in 9mS max
        while not self.mag_ready:
            self.mag_wait_func()
        return self._mag

    @property
    def mag_nonblocking(self):
        return self._mag        # ready or not

    def mag_trigger(self):      # Initiate a mag reading. Can be called repeatedly.
        if not self.mag_triggered:
            try:
                self._write(0x01, 0x0A, self._mag_addr) # single measurement mode
            except OSError:
                raise MPUException(self._I2Cerror)
            self.mag_triggered = True

    @property
    def mag_stale_count(self):  # Number of consecutive times old data was returned
        return self._mag_stale_count

    @property
    def mag_ready(self):       # Initiates a reading if necessary. Returns ready state.
        self.mag_trigger()
        try:
            self._read(self.buf1, 0x02, self._mag_addr)
        except OSError:
            raise MPUException(self._I2Cerror)
        return bool(self.buf1[0] & 1)

    def _mag_callback(self):
        '''
        Update magnetometer Vector3d object (if data available)
        '''
        try:                                    # If read fails, returns last valid data
            if self.mag_ready:                  # Starts mag if necessary
                self._read(self.buf6, 0x03, self._mag_addr)
                self.mag_triggered = False
            else:
                self._mag_stale_count += 1      # Data not ready: retain last value
                return                          # but increment stale count
            self._read(self.buf6, 0x03, self._mag_addr) # Mag was ready
            self._read(self.buf1, 0x09, self._mag_addr) # Read ST2
        except OSError:
            self.mag_triggered = False
            raise MPUException(self._I2Cerror)
        if self.buf1[0] & 0x0C > 0:             # An overflow or data error has occurred
            self._mag_stale_count +=1           # transitory condition? User checks stale count.
            return
        self._mag._ivector[1] = bytes_toint(self.buf6[1], self.buf6[0])  # Note axis twiddling and little endian
        self._mag._ivector[0] = bytes_toint(self.buf6[3], self.buf6[2])
        self._mag._ivector[2] = -bytes_toint(self.buf6[5], self.buf6[4])
        scale = 0.3                             # 0.3uT/LSB
        self._mag._vector[0] =  self._mag._ivector[0]*self.mag_correction[0]*scale
        self._mag._vector[1] =  self._mag._ivector[1]*self.mag_correction[1]*scale
        self._mag._vector[2] =  self._mag._ivector[2]*self.mag_correction[2]*scale
        self._mag_stale_count = 0

    def  _magsetup(self):
        '''
        Read magnetometer correction values from ROM. Perform the maths as decribed
        on page 59 of register map and store the results.
        '''
        try:
            self._write(0x0F, 0x0A, self._mag_addr)
            data = self._read(self.buf3, 0x10, self._mag_addr)
            self._write(0, 0x0A, self._mag_addr)        # Power down mode 
        except OSError:
            raise MPUException(self._I2Cerror)
        x = (0.5*(self.buf3[0] -128))/128 + 1
        y = (0.5*(self.buf3[1] -128))/128 + 1
        z = (0.5*(self.buf3[2] -128))/128 + 1
        return (x, y, z)

    def get_mag_irq(self):                      # Uncorrected values because floating point uses heap
        if not self.mag_triggered:              # Can't do exception handling here
            self._write(1, 0x0A, self._mag_addr)
            self.mag_triggered = True
        self._read(self.buf1, 0x02, self._mag_addr)
        if self.buf1[0] == 1:
            self._read(self.buf6, 0x03, self._mag_addr) # Note axis twiddling
            self._mag._ivector[1] = bytes_toint(self.buf6[1], self.buf6[0])
            self._mag._ivector[0] = bytes_toint(self.buf6[3], self.buf6[2])
            self._mag._ivector[2] = -bytes_toint(self.buf6[5], self.buf6[4])
            self.mag_triggered = False