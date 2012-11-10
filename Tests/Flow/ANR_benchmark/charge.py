chargeFile=open("benchmark/HeVel.dat",'r')
line = chargeFile.readline()
while "Number Of Nodes" not in line:
    line = chargeFile.readline()
#line.split()
nodesNumber =  line.split()[-1]
while "Perm" not in line:
    line = chargeFile.readline()
#
# We read the permutation
#
for i in range(int(nodesNumber)):
    chargeFile.readline()
#
# We read the charge
#
charge = []
for i in range(int(nodesNumber)):
    charge.append(float(chargeFile.readline()))
print len(charge)
