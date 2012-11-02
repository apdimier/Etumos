def IS_NUMBER(x):
    try:
        x = float(x)
        return True
    except:
        return False

def IS_POSITIVE_NUMBER(x):
    return IS_NUMBER(x) and float(x) >= 0
    
def IS_ION(x):
    for i in x:
        if not i.isalpha() and i not in ['+','-']: return 0
    return 1
    
a = "Ca 1 H+ 2 Na 3.0e-3"
print a.split()
b = filter(lambda x: IS_POSITIVE_NUMBER(x), a.split())
b = filter(lambda x: IS_ION(x), a.split())

