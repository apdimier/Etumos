#! /usr/bin/env python
import math
def f(x,y):
	#valeur moyenne
	ztop=-1000;
	
	#topographie interpolee par krigeage
	A1 = 36
	A2 = 24
	A3 = 34
	A4 = -10
	B1 = 1
	B2 = 1
	B3 = 1
	B4 = 1
	x1 = 1750.
	x2 = 2000.
	x3 = 4000.
	x4 = 3200.
	y1 = 2200.
	y2 = 300.
	y3 = 1000.
	y4 = 700.
	r1 = 1000.
	r2 = 500.
	r3 = 1000.
	r4 = 2000.
	
	zk = A1*math.exp(-B1*((x-x1)**2+(y-y1)**2)/(r1**2)) + A2*math.exp(-B2*((x-x2)**2+(y-y2)**2)/(r2**2)) + A3*math.exp(-B3*((x-x3)**2+(y-y3)**2)/(r3**2)) + A4*math.exp(-B4*((x-x4)**2+(y-y4)**2)/(r4**2)) 
	
	#Perturbation locale pseudo-periodique
	zp = 2*math.sin(x*0.005 + math.sin(y)) * math.sin(y*0.01 + math.cos(x))
	
	#Deformation courbe grande distance
	zc = -0.000001*((x-2000)**2 + (y-2000)**2)
	
	#Surface finale
	return ztop + zk + zp + zc
	
	return 10.*((((x-2375.)/475.)**2)+(((y-1500.)/300.)**2))
	
	
f1 = open("benchmark3D1.msh","r")
f2 = open("benchmark3D1_z.msh","w")
for i in range(1,13) :
	a=f1.readline()
	f2.write(a)
nbrNoeuds=int(f1.readline())
print "nbr noeuds ",nbrNoeuds
f2.write(str(nbrNoeuds) + "\n")
format = "%i %15.10e %15.10e %15.10e\n"
for i in range(1,nbrNoeuds+1) :
    a=f1.readline().split(" ")
    b=f(float(a[1]),float(a[2]))+float(a[3])
    f2.write(format%(int(a[0]),float(a[1]),float(a[2]),b))
    pass
      
a=f1.read()
f2.write(a)
f1.close()
f2.close()
print "Hello world"


