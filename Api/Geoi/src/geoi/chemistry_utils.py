from re import sub, findall

def split_formula(string):
    return findall(r'[A-Z][a-z]*[0-9-.]*',string)
def split_valence(string):
    if '+' in string:
        string = string[0:string.find('+')]
    elif '-' in string:
        string = string[0:string.find('-')]
    return findall(r'[A-Z]*[a-z]*[0-9-.]*',string)
def ion_counter(string):
    #string = sub(r'([A-Za-z]*)(\d*)',r'\1 \2',string)
    string = sub(r'([A-Za-z]*)([0-9-.-0-9]*)',r'\1 \2',string)
    tu = string.split(' ')
    if tu[1] == '':
        tu[1]='1'
    tu[1] = float(tu[1])
    return tu
def ion_sumup(liste):
    tu = []
    ion = []
    for i in liste:
        if i[0] in ion:
            j = ion.index(i[0])
            tu[j][1]+= i[1]
            pass
        else:
            ion.append(i[0])
            tu.append(i)
            pass
    return tu
def stoech(string):
    newi = []
    for i in string:
        if i !='':
            newi.append(ion_counter(i))
    stoechfinal = ion_sumup(newi)
    return stoechfinal    
def stoechBilanzierung_old(links,rechts):
    ok = 1
    for i in links:
        num = i[1]
        for j in rechts:
            if i[0]==j[0]:
                num-=j[1]
        if num !=0:
            ok = 0
    return ok
def reactantListe(rechts):
    c = []
    for ion in rechts:
        a = split_valence(ion[0]) 
        b = ''
        for j in a:
            b = b+j
        a =split_formula(b)
        for j in a:
            if j !='':
                c.append(ion_counter(j))
                c[-1][1]*=ion[1]
    return c        



def stoechBilanzierung(links,rechts):
    ok = 1
    for k in rechts:
        k[1]*=-1
    for i in links+rechts:
        num = 0
        for j in links+rechts:
            if i[0]==j[0]:
                num-=j[1]
        if abs(num) >1.e-6:
            ok = 0
    return ok

