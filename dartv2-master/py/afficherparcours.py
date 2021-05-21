import matplotlib.pyplot as plt 
from numpy import array,concatenate

donnees = open("Enregistrement.txt", "r")
Wall_x = []
Wall_y = []
Robotpos = array([[0],[0]],dtype="float64")
x,y = [],[]
dt = 1.
v = 1.
i = 0
locki = 0
save_front = []
orientation = 0
mursuivi = None
plt.figure()
#plt.xlim(-100,300)
#plt.ylim(-100,300)
for ligne in donnees:
	i += 1
	if i==22:
		side1,val1 = ligne.split(" ")
	elif i==23:
		side2,val2 = ligne.split(" ")
	elif i==24:
		side3,val3 = ligne.split(" ")
		if val1 > val2:
			xbegin=float(val2)
			dist_prev = float(val2)
		else: 	
			xbegin = float(val1)
			dist_prev = float(val1)
		Wall_x.append(0)
		Wall_y.append(float(val3))
		Wall_x.append(xbegin)
		Wall_y.append(float(val3))
		Wall_x.append(xbegin)
		Wall_y.append(0)			
		x.append(Robotpos[0,0])
		y.append(Robotpos[1,0])
		plt.plot(Robotpos[0,0],Robotpos[1,0],'oy')
	line = ligne.split()
	if line == ["TURNINGLEFT"]:
		if orientation == 0:
			Wall_x.append(Robotpos[0,0]-10)
			Wall_y.append(Wall_y[-1])
		elif orientation == 1:
			Wall_x.append(Wall_x[-1])
			Wall_y.append(Robotpos[0,0]+10)
		elif orientation == 2:
			Wall_x.append(Robotpos[0,0]+10)
			Wall_y.append(Wall_y[-1])
		elif orientation == 3:
			Wall_x.append(Wall_x[-1])
			Wall_y.append(Robotpos[0,0]-10)
		#plt.plot(Wall_x[-1],Wall_y[-1],'ob')
		plt.plot(Robotpos[0,0],Robotpos[1,0],'ob')
		orientation = (orientation+1)%4
		locki = i 
	elif line ==["TURNINGRIGHT"]:
		if orientation == 0:
			Wall_x.append(Robotpos[0,0]-10)
			Wall_y.append(Wall_y[-1])
		elif orientation == 1:
			Wall_x.append(Wall_x[-1])
			Wall_y.append(Robotpos[0,0]+10)
		elif orientation == 2:
			Wall_x.append(Robotpos[0,0]+10)
			Wall_y.append(Wall_y[-1])
		elif orientation == 3:
			Wall_x.append(Wall_x[-1])
			Wall_y.append(Robotpos[0,0]-10)
		#plt.plot(Wall_x[-1],Wall_y[-1],'og')
		plt.plot(Robotpos[0,0],Robotpos[1,0],'og')
		orientation = (orientation-1)%4
		locki = i
	elif i>locki+24 and ligne !="TURNINGRIGHT" and ligne !="TURNINGLEFT":
		side,val = ligne.split(" ")
		if side == "front":
			save_front.append(val)
			prevside="front"		
		if side !="front" or (side=="front" and prevside=="front"): 
			variation = (float(val)-dist_prev)/50
			if side == "front":
				v = 2.5
			else : 
				v = 0.6
			if orientation == 0:
				Robotpos += array([[variation],[-dt*v]])
			if orientation == 1:
				Robotpos += array([[dt*v],[variation]])
			if orientation == 2:
				Robotpos += array([[variation],[+dt*v]])
			if orientation == 3:
				Robotpos += array([[-dt*v],[variation]])
			dist_prev = float(val)
			prevside= side
		x.append(Robotpos[0,0])
		y.append(Robotpos[1,0])
		#plt.plot(Robotpos[0,0],Robotpos[1,0],'or')	
		
plt.plot(x,y,'-r')
#plt.plot(Wall_x,Wall_y,'-k')
plt.show()
