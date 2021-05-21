import dartv2b
import numpy
import time
rb = dartv2b.DartV2()
Data = array([])
rb.set_speed(100,100)
time0 = time.time()
for i in range(8):
	mes = self.sonars.read_sonars()["front"]
	dprev = self.left_filt.filtre(mes)
	Data += array([dprev])
	time.sleep(0.05)
while time.time()-time0<10:
	NewDist = self.sonars.read_sonars()["front"]	
	DistFilted = self.left_filt.filtre(NewDist)
	Data += array([DistFilted])
	time.sleep(0.05)
rb.set_speed(0,0)
rb.stop()
num.savetxt('Lignedroite.txt', Data, delimiter=" ", fmt="%s")
