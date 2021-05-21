import time
import sys
import os

# rear wheels encoders and direction, battery level
# encoders reset

class EncodersIO ():
    def __init__(self, bus_nb = 2, addr = 0x14, sim=False, vsv=None):
        self.__sim = sim
        if self.__sim:
            self.vsv = vsv

        self.__bus_nb = 2
        self.__addr = 0x14 

        # conditional i2c setup
        # if real robot , then we use actual i2c
        # if not , we are on simulated i2c
        sys.path.append('./drivers')
        if self.__sim:
            sys.path.append('../vDartV2')
            import i2csim as i2c
            self.__dev_i2c=i2c.i2c(self.__addr,self.__bus_nb,vsv=self.vsv)
        else:
            import i2creal as i2c
            self.__dev_i2c=i2c.i2c(self.__addr,self.__bus_nb)

        # place your new class variables here

    def read_odometers(self):
        read = False
        while not read:
            try:
                low_g, high_g, low_d, high_d = self.__dev_i2c.read(0x00, 4)
                read = True
            except:
                time.sleep(0.1)
        odo_g = low_g + 256*high_g
        if odo_g > 32767:
            odo_g -= 65536
        odo_d = low_d + 256*high_d
        if odo_d > 32767:
            odo_d -= 65536
        return {"left":odo_g, "right": odo_d}


    def read_battery(self):
        low_bat, high_bat = self.__dev_i2c.read(0x06, 2)
        bat = low_bat + 256*high_bat
        if bat > 32767:
            bat -= 65536
        return bat


if __name__ == "__main__":
    encoder = EncodersIO()
    print(encoder.read_odometers())
    print(encoder.read_battery())
