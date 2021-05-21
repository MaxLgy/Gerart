import struct
import time
import sys
import math

# LIS3DML 0x1e  (mag sensor)
# LSM6    0x6b  (accelero - gyro)

class Imu9IO():
    def __init__(self,sim=False, vsv=None):
        self.__sim = sim
        if self.__sim:
            self.vsv = vsv

        self.__bus_nb = 2
        self.__addr_mg = 0x1e  # mag sensor
        self.__addr_ag = 0x6b  # accelero - gyro

        # conditional i2c setup
        # if real robot , then we use actual i2c
        # if not , we are on simulated i2c
        if self.__sim:
            import i2csim as i2c
            self.__dev_i2c_mg=i2c.i2c(self.__addr_mg,self.__bus_nb,vsv=self.vsv)
            self.__dev_i2c_ag=i2c.i2c(self.__addr_ag,self.__bus_nb,vsv=self.vsv)
        else:
            import i2creal as i2c
            self.__dev_i2c_mg=i2c.i2c(self.__addr_mg,self.__bus_nb)
            self.__dev_i2c_ag=i2c.i2c(self.__addr_ag,self.__bus_nb)

    # place your imu functions here
