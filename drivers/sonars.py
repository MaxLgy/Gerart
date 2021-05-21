import time
import sys
import os
import platform

class SonarsIO ():
    def __init__(self,sim=False,vsv=None):
        self.__sim = sim
        if self.__sim:
            self.vsv = vsv
        #print ("vsv",vsv,self.vsv)
        self.__bus_nb = 2
        self.__addr_4_sonars = 0x21
        self.__addr_front_left = 0x070
        self.__addr_front_right = 0x072

        # conditional i2c setup
        # if real robot , then we use actual i2c
        # if not , we are on simulated i2c
        if self.__sim:
            import i2csim as i2c
            self.__dev_i2c_4_sonars=i2c.i2c(self.__addr_4_sonars,bus_nb=self.__bus_nb,vsv=self.vsv)
            self.__dev_i2c_front_left=i2c.i2c(self.__addr_front_left,bus_nb=self.__bus_nb,vsv=self.vsv)
            self.__dev_i2c_front_right=i2c.i2c(self.__addr_front_right,bus_nb=self.__bus_nb,vsv=self.vsv)
        else:
            import i2creal as i2c
            self.__dev_i2c_4_sonars=i2c.i2c(self.__addr_4_sonars,self.__bus_nb)
            self.__dev_i2c_front_left=i2c.i2c(self.__addr_front_left,self.__bus_nb)
            self.__dev_i2c_front_right=i2c.i2c(self.__addr_front_right,self.__bus_nb)
            
        # place your new class variables here
        for isn in range(4):
            self.set_mode(isn + 1, 2)
            self.set_dist_max(isn + 1, 1.5)

    def set_mode(self, num, mode):
        vals = [mode]
        self.__dev_i2c_4_sonars.write(0xB0 + num - 1, vals)

    def set_dist_max(self, num, dist):
        offs = 0xA0 + (num - 1) * 2
        idist = int(round(dist * 100.0))
        vals = [idist % 256, idist // 256]
        self.__dev_i2c_4_sonars.write(offs, vals)
        
    def read_diag_left_word(self):
        try:
            self.__dev_i2c_front_left.write(0,[0x51])
            time.sleep(0.065)
            try:
                vms,vls = self.__dev_i2c_front_left.read(2,2)
                #print (vms,vls)
                self.diag_left_w = float(vls + (vms << 8))/100.0
            except:
                self.diag_left_w = -1
        except:
            self.diag_left_w = -1
        return self.diag_left_w

    # read two data bytes at once
    def read_diag_right_word(self):
        try:
            self.__dev_i2c_front_right.write(0,[0x51])
            time.sleep(0.065)
            try:
                vms,vls = self.__dev_i2c_front_right.read(2,2)
                #print (vms,vls)
                self.diag_right_w = float(vls + (vms << 8))/100.0
            except:
                self.diag_right_w = -1
        except:
            self.diag_right_w = -1
        return self.diag_right_w

    # read two bytes separately
    def read_diag_left(self):
        #self.bus.write_i2c_block_data(self.addr_l,0,[0x51])
        try:
            self.__dev_i2c_front_left.write(0,[0x51])
            time.sleep(0.065)
            try:
                vms = self.__dev_i2c_front_left.read_byte(2)
                vls = self.__dev_i2c_front_left.read_byte(3)
                #print (vms,vls)
                self.diag_left = float(vls + (vms << 8))/100.0
            except:
                self.diag_left = -1
        except:
            self.diag_left = -1
        return self.diag_left

    # read two bytes separately
    def read_diag_right(self):
        #self.bus.write_i2c_block_data(self.addr_r,0,[0x51])
        try:
            self.__dev_i2c_front_right.write(0,[0x51])
            time.sleep(0.065)
            try:
                vms = self.__dev_i2c_front_right.read_byte(2)
                vls = self.__dev_i2c_front_right.read_byte(3)
                #print (vms,vls)
                self.diag_right = float(vls + (vms << 8))/100.0        
            except:
                self.diag_right = -1
        except:
            self.diag_right = -1
        return self.diag_right

    def read_diag_all(self):
        self.read_diag()
        return [self.diag_left,self.diag_right]

    def read_diag_both(self):
        #self.bus.write_i2c_block_data(self.addr_l,0,[0x51])
        #self.bus.write_i2c_block_data(self.addr_r,0,[0x51])
        try:
            self.__dev_i2c_front_left.write(0,[0x51])
            self.__dev_i2c_front_right.write(0,[0x51])
            time.sleep(0.065)
            try:
                vms = self.__dev_i2c_front_left.read_byte(2)
                vls = self.__dev_i2c_front_left.read_byte(3)
                #vms = self.bus.read_byte_data(self.addr_l,2)
                #vls = self.bus.read_byte_data(self.addr_l,3)
                #print (vms,vls)
                self.diag_left = float(vls + (vms << 8))/100.0
            except:
                self.diag_left = -1
            try:
                vms = self.__dev_i2c_front_right.read_byte(2)
                vls = self.__dev_i2c_front_right.read_byte(3)
                #vms = self.bus.read_byte_data(self.addr_r,2)
                #vls = self.bus.read_byte_data(self.addr_r,3)
                #print (vms,vls)
                self.diag_right = float(vls + (vms << 8))/100.0        
            except:
                self.diag_right = -1
        except:
            self.diag_left = -1
            self.diag_right = -1
        return [self.diag_left,self.diag_right]

    def get_version(self):
        return self.__dev_i2c_4_sonars.read_byte(0xC0)

    def get_mode(self,num):
        return self.__dev_i2c_4_sonars.read_byte(0xB0+num-1)

    def get_state(self,num):
        return self.__dev_i2c_4_sonars.read_byte(0xB4+num-1)

    def set_mode(self,num,mode):
        vals = [mode]
        self.__dev_i2c_4_sonars.write(0xB0+num-1,vals)

    def set_dist_max(self,num,dist):
        offs = 0xA0+(num-1)*2
        idist = int(round(dist*100.0))
        vals = [idist%256,idist//256]
        self.__dev_i2c_4_sonars.write(offs,vals)
        
    def read_4_sonars(self):
        vf = self.read_front()
        vl = self.read_left()
        vb = self.read_rear()
        vr = self.read_right()
        return [vf, vl, vb, vr]

    def read_front(self):
        self.front = self.__read(1)
        return self.front
    
    def read_front_bytes (self):
        addr = 0x00
        vl = self.__dev_i2c_4_sonars.read_byte(addr)
        addr = 0x01
        vh = self.__dev_i2c_4_sonars.read_byte(addr)
        self.front = vl+vh*256 
        return self.front

    def read_left(self):
        self.left = self.__read(3)
        return self.left

    def read_rear(self):
        self.rear = self.__read(2)
        return self.rear
    
    def read_right(self):
        self.right = self.__read(4)
        return self.right

    def __read(self,num_sonar):
        try:
            addr = 0x00+2*(num_sonar-1)
            #print ("addr",addr)
            v = self.__dev_i2c_4_sonars.read(addr,2)
            #print ("v",v)
            v = v[0] + 256*v[1]
            #print ("v",v)
        except:
            print ("------ error I2C sonar")
            v = 10000
        return v

    def __write(self,cmd):
        #self.bus.write_i2c_block_data(self.addr,0,cmd)
        self.__dev_i2c_4_sonars.write(0,cmd)
        
        

    def read_sonars(self):
        try:
            low_1 = self.__dev_i2c_4_sonars.read(0x00, 1)
            high_1 = self.__dev_i2c_4_sonars.read(0x01, 1)
        except:
            low_1 = 0
            high_1 = 127
        try:
            low_2 = self.__dev_i2c_4_sonars.read(0x02, 1)
            high_2 = self.__dev_i2c_4_sonars.read(0x03, 1)
        except:
            low_2 = 0
            high_2 = 127
        try:
            low_3 = self.__dev_i2c_4_sonars.read(0x04, 1)
            high_3 = self.__dev_i2c_4_sonars.read(0x05, 1)
        except:
            low_3 = 0
            high_3 = 127
        try:
            low_4 = self.__dev_i2c_4_sonars.read(0x06, 1)
            high_4 = self.__dev_i2c_4_sonars.read(0x07, 1)
        except:
            low_4 = 0
            high_4 = 127
        
        sonar_1 = low_1 + 256*high_1
        try :
            sonar_1 = sonar_1[0]
        except :
            sonar_1 = sonar_1
        if sonar_1 > 32767:
            sonar_1 -= 65536
        sonar_2 = low_2 + 256*high_2
        try:
            sonar_2 = sonar_2[0]
        except:
            sonar_2 = sonar_2
        if sonar_2 > 32767:
            sonar_2 -= 65536
        sonar_3 = low_3 + 256*high_3
        try:
            sonar_3 = sonar_3[0]
        except:
            sonar_3 = sonar_3
        if sonar_3 > 32767:
            sonar_3 -= 65536
        sonar_4 = low_4 + 256*high_4
        try:
            sonar_4 = sonar_4[0]
        except:
            sonar_4 = sonar_4
        if sonar_4 > 32767:
            sonar_4 -= 65536
        time.sleep(0.01)
        return {"front":sonar_1, "back":sonar_2, "left":sonar_3, "right":sonar_4}       

