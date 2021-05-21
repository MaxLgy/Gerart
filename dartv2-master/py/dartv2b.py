import drivers.dartv2b_basis
import sys
import time
import numpy as np
import filt

class DartV2(drivers.dartv2b_basis.DartV2Basis):
    def __init__(self):
        # get init from parent class
        #drivers.dartv2b_basis.DartV2Basis.__init__(self)
        super().__init__()
        # define class variables
        self.__last_odometer_mesure = self.encoders.read_odometers()        
        self.left_filt = filt.SonarFilter()
        self.right_filt = filt.SonarFilter()
        self.front_filt = filt.SonarFilter()
        self.back_filt = filt.SonarFilter()
        self.recording = open("Enregistrement.txt", "w")        
        f_son = open("dist_wall.txt","r")
        self.target_left = float(f_son.readline())
        self.target_right = float(f_son.readline())
        
        if self.dart_sim():
            self.__dist_front = 35
            self.__Kp = 0.5
            self.__Kd = 0.35
            self.__noregul_speed = 70
            self.nb_ticks = 471
        else:
            self.__dist_front = 55
            self.__Kp = 0.9
            self.__Kd = 0.5
            self.__noregul_speed = 60
            f_odo = open("nb_ticks.txt",'r')
            self.nb_ticks = float(f_odo.readline())
            f_odo.close()

    @property
    def last_odometer_mesure(self):
        return self.__last_odometer_mesure

    @last_odometer_mesure.setter
    def last_odometer_mesure(self, new_odo):
        vmax = 2**16
        odol = new_odo["left"]
        odor = new_odo["right"]
        if odol < 0 and self.last_odometer_mesure["left"] > vmax-50:
            odol = odol + 2*vmax
        elif odol > 0 and self.last_odometer_mesure["left"] < -vmax + 50:
            odol = odol - 2*vmax
        
        if odor < 0 and self.last_odometer_mesure["right"] > vmax-50:
            odor = odor + 2*vmax
        elif odor > 0 and self.last_odometer_mesure["right"] < -vmax + 50:
            odor = odor - 2*vmax
        self.__last_odometer_mesure = {"left":odol, "right":odor}


    def delta_front_odometers(self):
        odo = self.encoders.read_odometers()
        dl = self.last_odometer_mesure["left"] - odo["left"]
        dr = self.last_odometer_mesure["right"] - odo["right"]
        self.last_odometer_mesure = odo
        time.sleep(0.01)
        return {"left":dl, "right":dr}


    def turn_angle(self, angle):
        odo_cap = (self.nb_ticks * ((angle) / 360.) * (26 / 12.5))
        odo_mes_init = self.encoders.read_odometers()['left']
        odo_mes = 0
        speed_max = 160
        speed_min = 120
        
        while abs(odo_cap - odo_mes) > 15.0:
            time.sleep(0.05)
            a = odo_mes_init - self.encoders.read_odometers()['left']
            if a >= 0:
                odo_mes = a % (self.nb_ticks * (26 / 12.5))
            else:
                odo_mes = - ((-a) % (self.nb_ticks * (26 / 12.5)))
            erreur = odo_cap - odo_mes

            speed = np.sign(erreur)*(((speed_max - speed_min)/624)*abs(erreur) + speed_min)

            self.set_speed(speed, -speed)
        self.set_speed(0, 0)


    def straight_line(self,wall):
        for i in range(8):
            mes = self.sonars.read_sonars()[wall]
            time.sleep(0.05)
        if wall=="left":
            dist_wall = self.target_left
            dprev = self.left_filt.filtre(mes)
        else:
            dist_wall = self.target_right
            dprev = self.right_filt.filtre(mes)
        while (not self.check_front_wall(self.__dist_front + 15)) and dprev < 1.3*dist_wall:
            dprev = self.follow_side_wall(wall,dprev)
            time.sleep(0.01)
        self.set_speed(0,0)
    
    
    def check_closest_wall(self):
        self.set_speed(0, 0)
        self.front_filt.reset()
        self.left_filt.reset()
        self.right_filt.reset()
        self.back_filt.reset()
        time.sleep(0.1)
        
        for k in range(15):
            sonar_values = self.sonars.read_sonars()
            filtered_left = self.left_filt.filtre(sonar_values["left"])
            filtered_right = self.right_filt.filtre(sonar_values["right"])
            filtered_back = self.back_filt.filtre(sonar_values["back"])
            self.recording.write("left"+ " " +str(filtered_left)+"\n")
            self.recording.write("right"+ " " +str(filtered_right)+"\n")
            self.recording.write("back"+ " " +str(filtered_back)+"\n")
            time.sleep(0.01)
            if self.dart_sim():
                time.sleep(0.1)
        if filtered_left < filtered_right:
            return "left"
        else:
            return "right"
    
    
    def check_front_wall(self, dist):
        dist_front = self.sonars.read_sonars()["front"]
        dist_front_filtered = self.front_filt.filtre(dist_front)
        self.recording.write("front"+ " " +str(dist_front_filtered)+"\n")
        if len(self.front_filt.filt) > 5:
            return dist_front_filtered < dist
        else:
            return False


    def goForward(self):
        odoinit = self.encoders.read_odometers()
        odo = self.encoders.read_odometers()
        while not self.check_front_wall(self.__dist_front):
            deltaodo = self.delta_front_odometers()
            if abs(deltaodo["right"]-deltaodo["right"]) <= 1 :
                self.set_speed(self.__noregul_speed,self.__noregul_speed)
            elif deltaodo["right"]-deltaodo["right"] > 1 :
                self.set_speed(self.__noregul_speed+5,self.__noregul_speed)
            elif deltaodo["right"]-deltaodo["right"] < -1 :
                self.set_speed(self.__noregul_speed,self.__noregul_speed+5)
            time.sleep(0.01)
            odo = self.encoders.read_odometers()
    
    
    def MenuCalibration(self):
        time.sleep(0.01)
        print(" Calibration odometres [1] \n Calibration sonars [2]  \n Retour au menu [3]")
        a = input()
        try:
            int(a)
        except:
            print("Non reconnu")
        if int(a) == 1:
            self.CalibrationOdo()
        elif int(a) == 2:
            self.CalibrationSonars()
        elif int(a) == 3:
            return None
        
    
    def CalibrationOdo(self):
        nb_tours = 1
        ticks = [self.nb_ticks]
        while nb_tours < 4:
            time.sleep(0.2)
            for k in range(4*nb_tours):
                self.turn_angle(90)
                time.sleep(0.1)
                self.set_speed(0,0)
            a = input("Situation par rapport a l'objectif : " + str(nb_tours)  + " tours \n + : objectif depasse \n - : objectif non atteint \n = : sur l'objectif \n")
            if a == '=':
                nb_tours += 1
            elif a == '+':
                self.nb_ticks = (1-0.2**nb_tours)*ticks[-1]
                ticks.append(self.nb_ticks)
            elif a == '-':
                self.nb_ticks = (1 + 0.2**nb_tours)*ticks[-1]
                ticks.append(self.nb_ticks)
            else:
                print("Utilisez '+', '-' ou '='")
            print(ticks)
        f_odo = open("nb_ticks.txt",'w')
        f_odo.write(str(self.nb_ticks))
        f_odo.close()


    def CalibrationSonars(self):
        if self.dart_sim() == False:
            print(" Mettre le robot pres d'un mur sur sa gauche et valider")
            input()
            for k in range(8):
                dist_left = self.left_filt.filtre(self.sonars.read_sonars()["left"])
                time.sleep(0.05)
            print("Distance a gauche : ", dist_left)
            print(" Retourner le robot et valider")
            input()
            for k in range(8):
                dist_right = self.right_filt.filtre(self.sonars.read_sonars()["right"])
                time.sleep(0.05)
            print("Distance a droite : ", dist_right)
            if dist_left > 150 and dist_right > 150:
                print(" /!\ sonars inverses")
            self.left_filt.reset()
            self.right_filt.reset()
            print(" Mettre le robot au centre du circuit et valider")
            input()
            for k in range(40):
                dist_left = self.left_filt.filtre(self.sonars.read_sonars()["left"])
                dist_right = self.right_filt.filtre(self.sonars.read_sonars()["right"])
                time.sleep(0.05)
            print(" Distance nominale gauche : ", dist_left, "\n Distance nominale droite : ", dist_right)
            f_son = open("dist_wall.txt","w")
            f_son.write(str(dist_left))
            f_son.write("\n")
            f_son.write(str(dist_right))
            self.MenuCalibration()
        else:
            print(" Valider pour configurer les sonars")
            input()
            for k in range(40):
                dist_left = self.left_filt.filtre(self.sonars.read_sonars()["left"])
                time.sleep(0.05)
            print(" Distance nominale gauche et droite : ", dist_left)
            f_son = open("dist_wall.txt","w")
            f_son.write(str(dist_left))
            f_son.write("\n")
            f_son.write(str(dist_left))
            self.MenuCalibration()


    def follow_side_wall(self,wall,dprev):
        Normal_speed = 80
        NewDist = self.sonars.read_sonars()[wall]
        if wall == "left":
            distdes = self.target_left
            DistFilted = self.left_filt.filtre(NewDist)
        else:
            distdes = self.target_right
            DistFilted = self.right_filt.filtre(NewDist)
        self.recording.write(wall+ " " +str(DistFilted)+"\n")
        Eprop =  DistFilted - distdes
        Eder = (DistFilted - dprev)/0.01
        Correction = self.__Kp*Eprop + self.__Kd*Eder 
        if wall == "right":
            SpeedGauche = Normal_speed - Correction
            SpeedDroite = Normal_speed + Correction
        else:
            SpeedGauche = Normal_speed + Correction
            SpeedDroite = Normal_speed - Correction
        self.set_speed(SpeedDroite,SpeedGauche)
        return DistFilted
		

    def doNothing(self, sec):
        self.set_speed(0, 0)
        time.sleep(sec)
