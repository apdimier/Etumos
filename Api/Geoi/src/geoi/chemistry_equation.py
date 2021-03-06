import re

EQUALS = ' = '
PLUS = ' +'
DOT = '.'

ELECTRON = 'e'

EPSILON = 1e-10

def IS_CLOSE_TO_ZERO(v):
    return abs(v) < EPSILON

def PARSE_AND_SIMPLIFY_NB(s):
    f = float(s)
    if f == int(f):
        f = int(f)
    return f

class Equation:

    def __init__(self, string):
        """
        may raise exceptions

        N.B the equation line may be slighlty different from the input because of simplifications and
        standardization
        """

        if string is None or string == "":
            raise ValueError, "equation string is empty"

        left, right = self.parseLeftMembers(string), self.parseRightMembers(string)
        self.line = self._listToString(left) + EQUALS + self._listToString(right)
        if self._listToString(right)!="H2O-0.01":
            if not self.isStoichiometricBalanced(left, right):
                raise ValueError, "bad stoichiometry balance in equation : " + string
            if not self.isChargeBalanced(left, right):
                raise ValueError, "bad charge balance in equation : " + string

    def parseLeftMembers(self, line=None):
        "may raise exceptions"
        if line is None:
            line = self.getString()
        left = line.split(EQUALS)[0]
        return self._breakMember(left)

    def parseRightMembers(self,  line=None):
        "may raise exceptions"
        if line is None:
            line = self.getString()
        l = line.split(EQUALS)
        if len(l) < 2:
            raise ValueError, "No equal sign in the equation %s" % line
        right = l[1]
        if right != "H2O-0.01":
            return self._breakMember(right)
        else:
            return [["H2O-0.01",1]]

    def getMainTerm(self):
        "get the first term of right part"
        return self.parseRightMembers()[0][0]

    def isChargeBalanced(self, left_members=None, right_members=None):
        if left_members is None:
            left_members = self.parseLeftMembers()
        if right_members is None:
            right_members = self.parseRightMembers()
        charge = 0
        for (members, sign) in [(left_members, 1), (right_members,-1)]:
            for (mol, coef) in members:
                charge += sign*coef*mol.getCharge()
        return IS_CLOSE_TO_ZERO(charge)

    def isStoichiometricBalanced(self, left_members=None, right_members=None):
        if left_members is None:
            left_members = self.parseLeftMembers()
        if right_members is None:
            right_members = self.parseRightMembers()
        hash = {}
        for (members, sign) in [(left_members, 1), (right_members,-1)]:
            for (mol, coef) in members:

                for (elt, nb) in mol.getElements().iteritems():
                    if elt not in hash:
                        hash[elt] = 0
                    hash[elt] += sign * coef * nb

        # remove electron if any
        if ELECTRON in hash:
            hash.pop(ELECTRON)
        for v in hash.values():
            if not IS_CLOSE_TO_ZERO(v):
                return False
        return True

    def _listToString(self, list):
        s = ""
        for member in list:
            coef = member[1]
            if coef != 1:
                s += str(member[1]) + " "
            s += str(member[0]) + " + "
        return s[:-3]

    def getString(self):
        return self.line

    def _breakMember(self, s):
        "parse a member of an equation in a list of terms with coef"
        list = []
        l = s.split(PLUS)
        for term in l:
            term = term.lstrip().rstrip()
            st = term.split()
            if not st: # may happen when the coefs are signed
                continue

            if len(st) == 1:
                # 2 possibilities : either implicit coef 1, or no space between
                # the coef and the specie
                if term[0].isdigit() or term[0] == DOT : # no space
                    # try to figure out where to split it
                    p = re.compile(r'(\d*\.\d+)|\d+')
                    m = p.match(term)
                    coef = PARSE_AND_SIMPLIFY_NB(m.group())
                    specie = term[m.end():]

                else:
                    coef = 1
                    specie = term

            else:
                coef = PARSE_AND_SIMPLIFY_NB(st[0])
                specie = st[1]

            if not specie:
                raise ValueError, "specie should not be empty for member %s of line %s" % (term, s)

            if specie[0].isdigit():
                raise ValueError,"specie " + specie + " should not start with a digit"

            mol = MolecularFormula(specie)
            list.append( [mol, coef] )
        return list

    def __str__(self):
        return self.getString()

    def __repr__(self):
        return self.getString()

    def __cmp__(self, o):
        return cmp(self.getString(), o.getString())


class MolecularFormula:
    def __init__(self, line):
        (mol, charge) = self.splitFormulaFromCharge(line)
        self._line = line
        self._charge = charge
        self._elts = self.splitMoleculInElements(mol)

    @staticmethod
    def splitFormulaFromCharge(line):
        """
        return a 2-list  [mol_formula_string, charge]

        raise an exception if invalid

        Example: 'BF2(OH)2- => ('BF2(OH)', -2)
        """

        charge = 1
        l = re.split("\+|\-", line)
        if '-' in line:
            charge = -1

        if len(l) == 1:
            return [line,0]

        if len(l) > 2:
            # could be the ---- and +++ syntax
            # check it : all elements besides the first should be empty
#            if any(l[1:]):
#                raise ValueError,"too many signs in Molecular Formula " + line

            return [l[0], charge * (len(l)-1)]

        else:

            # parse and check charge
            if l[1] == "":
                l[1] = 1
            charge *= int(l[1])
            l[1] = charge
        return l

    @staticmethod
    def splitMoleculInElements(line, hash=None, multiplier=1):
        "see getElements()"
        if hash is None:
            hash = {}
        if line == ELECTRON: # special case
            if ELECTRON not in hash:
                hash[ELECTRON] = 0
            hash[ELECTRON] += 1
            return hash

        # deal recursively with parenthesis
        if '(' in line:
            for b in MolecularFormula.splitParenthesisBlocks(line):
                if '(' in b: # parse number
                    m = re.search("((\d*\.\d+)|\d+)$", b)
                    if m is None:
                        nb = 1
                        block = b[1:-1]
                    else:
                        nb = PARSE_AND_SIMPLIFY_NB( m.group() )
                        block = b[1:m.start()-1] # remove nb anfd outer parenth

                    MolecularFormula.splitMoleculInElements(block, hash, multiplier*nb)
                else:
                    MolecularFormula.splitMoleculInElements(b, hash, multiplier)
        else:
            l = re.findall('([A-Z][a-z]?)((?:\d*\.\d+)|\d*)', line)

            for (elt,nb) in l:
                if not nb:
                    nb = 1
                else:
                    nb = PARSE_AND_SIMPLIFY_NB(nb)

                nb *= multiplier

                if elt not in hash:
                    hash[elt] = 0
                hash[elt] += nb

        return hash


    @staticmethod
    def splitParenthesisBlocks(line):
        "split the line into consecutive non-overlappings blocks"

        if '(' not in line:
            return [line]

        pcount = 0
        waiting_for_number = False
        block = ""
        blocks = []
        for c in line:
            if waiting_for_number:
                if not c.isdigit() and c != DOT:
                    blocks.append(block)
                    block = ""
                    waiting_for_number = False
            if c == '(':
                if pcount == 0:
                    if block:
                        blocks.append(block)
                    block = ""

                pcount += 1
            elif c == ')':
                pcount -= 1
                if pcount == 0: # end of block
                    waiting_for_number = True
                elif pcount < 0:
                    raise ValueError, "bad parenthesized expression: " + line
            block += c

        if block:
            blocks.append(block)
        return blocks


    def getString(self):
        return self._line

    def getCharge(self):
        return self._charge

    def getElements(self):
        """"
        return a dictionary where elements are keys and numbers are values

        For instance, for Fe2(OH)2, it will return {'Fe':2, 'H':2, 'O':2 }
        """
        return self._elts


    def __str__(self):
        return self.getString()

    def __repr__(self):
        return self.getString()

    def __cmp__(self, o):
        return cmp(self.getString(), o.getString())

if __name__ == '__main__':
    t1 = "2 Fe+3 + 2 H2O = Fe2(OH)2+4 + 2 H+"
    t2 = "K4Fe(CN)6 + 6 H2SO4 + 6 H2O = 2 K2SO4 + FeSO4 + 3 (NH4)2SO4 + 6 CO"
    eq1 = Equation(t1)
    print eq1


    for i in ["H2O", "(NH4)3.467Al3.45Fe.017Si14.533O36","Ca2NaBF3(OH(CaF)3)52Zn", "K4Fe(CN)6", "H2O", "(NH4)2SO4", "Fe", "CO"
              ,"BF2(OH)2-", "Fe3(OH)2-", "Fe2(OH)2+4", "Zn(CO3)2-2", "SO4--", "Cu+++++",
              "(NpO2)2(OH)2++", "Ca.165Al2.33Si3.67O10(OH)2" ,"(UO2)3(OH)7-"]:
        mol = MolecularFormula(i)
        print mol, " : ", mol.getElements(), ", charge=", mol.getCharge()

    for i in ["4 Cl- + Ag+ + H2O = H2O + AgCl4---", "(UO2.3333)2 + 8.0000 H+  =  0.3333 O2 + 2.0000 U++++ + 4.0000 H2O"
              , "CaSO4 + 0.5H2O  =  + 0.5000 H2O + 1.0000 Ca++ + 1.0000 SO4--"]:
        eq = Equation(i)
        print i, " ====> ", eq


