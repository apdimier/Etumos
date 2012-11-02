
#CaCO3 = CO3-2 + Ca+2
string = "CaCO3 = CO3-2 + Ca+2"
string = 'H4SiO4  = H3SiO4- + H+'
string = "SiO2 + 2 H2O = H4SiO4"
#string = "Ca5(PO4)3OH + 4 H+ = H2O + 3 HPO4-2 + 5 Ca+2"
string = "NH4+ = NH3 + H+"

#a = string.split(" ")[1:]
a = string.split(" ")
print a
liste = []
print a
ind = a.index("=")
print " a before ",a
a.remove(a[ind+1])
print " a after ",a
dig = 1
for i in a:

    if i.isdigit():
        dig = i
    elif i not in ["+","-","=",""]:
#        if a.index(i) < ind:
        if a.index(i) > ind:
            print "dig",dig
            digi = dig
            dig = "-"+str(digi)
            liste.append((i,dig))
        else:
            liste.append((i,dig))
        dig = 1        

print liste

