from constant import epspH
from datamodel import *
import fields
from listtools import normMaxListComparison, subtractLists
from chemicaltransport import *
from chemicaltransportmodule import *
from mt3d import Mt3d              # mt3d
from cartesianmesh import *        # Cartesian mesh
from phreeqc import *              # phreeqc


Phreeqc_file = "guitest1.txt"      # bounded to Phreeqc
ProblemName  = "guitest1"          # Phreeqc file 
mesh = CartesianMesh2D("global","XY")
mesh = CartesianMesh2D("global","XY")
nx  = 1001
ny  = 1
#~~~~~~~~~~~~~~~~~~
#~ Mesh extension ~
#~~~~~~~~~~~~~~~~~~
deltax = []
dx = [1e-05/1]*1
deltax.extend(dx)
dx = [0.4/(nx-1)]*(nx-1)
deltax.extend(dx)
deltay = []
dy = [1.0/1]*1
deltay.extend(dy)
mesh.setdAxis("X",deltax)
mesh.setdAxis("Y",deltay)
boundary0Body = CartesianMesh2D("boundary", "XY")
boundary0Body.setZone("boundary",index_min = Index2D (1,1), index_max = Index2D (1,1))
column1Body = CartesianMesh2D("column", "XY")
column1Body.setZone("column",index_min = Index2D (2,1), index_max = Index2D (nx,1))
#~~~~~~~~~~~~~
#~ Materials ~
#~~~~~~~~~~~~~
columnMaterial = Material (name = "column",effectiveDiffusion = EffectiveDiffusion (3e-10,unit="m**2/s"),\
permeability = Permeability(value = 1.0),\
porosity = Porosity(value = 0.3),\
kinematicDispersion = KinematicDispersion (0.000667,0))

#~~~~~~~~~~~
#~ Regions ~
#~~~~~~~~~~~
boundary0Region = Region(support=boundary0Body, material= columnMaterial)
column1Region = Region(support=column1Body, material= columnMaterial)
#~~~~~~~~~~~~~~~~~~~
# Chemical Addenda ~
#~~~~~~~~~~~~~~~~~~~
speciesAddenda = []
NaAMS = AqueousMasterSpecies(symbol = "Na+",\
                             name = "Na",\
                             element = "Na",\
                             molarMass = MolarMass(22.9898,"g/mol"),\
                             alkalinity = 0.0)
speciesAddenda.append(NaAMS)
KAMS = AqueousMasterSpecies(symbol = "K+",\
                            name = "K",\
                            element = "K",\
                            molarMass = MolarMass(39.102,"g/mol"),\
                            alkalinity = 0.0)
speciesAddenda.append(KAMS)
TAMS = AqueousMasterSpecies(symbol = "T+",\
                            name = "T",\
                            element = "T",\
                            molarMass = MolarMass(35,"g/mol"),\
                            alkalinity = 0)
speciesAddenda.append(TAMS)
ClAMS = AqueousMasterSpecies(symbol = "Cl-",\
                             name = "Cl",\
                             element = "Cl",\
                             molarMass = MolarMass(35.453,"g/mol"),\
                             alkalinity = 0.0)
speciesAddenda.append(ClAMS)
NaSSp = AqueousSecondarySpecies(symbol = "Na+",\
                                formationReaction = [\
                                                     ("Na+",1)],\
                                logK25 = 0.0,\
                                name = "Na")
speciesAddenda.append(NaSSp)
KSSp = AqueousSecondarySpecies(symbol = "K+",\
                               formationReaction = [\
                                                    ("K+",1)],\
                               logK25 = 0.0,\
                               name = "K")
speciesAddenda.append(KSSp)
TSSp = AqueousSecondarySpecies(symbol = "T+",\
                               formationReaction = [\
                                                    ("T+",1)],\
                               logK25 = 0.0,\
                               name = "T")
speciesAddenda.append(TSSp)
ClSSp = AqueousSecondarySpecies(symbol = "Cl-",\
                                formationReaction = [\
                                                     ("Cl-",1)],\
                                logK25 = 0.0,\
                                name = "Cl")
speciesAddenda.append(ClSSp)
NaXESp = SorbedSecondarySpecies(symbol = "NaX",\
                                formationReaction = [("Na+",1),("X-",1)],\
                                logK25 = 0.0,\
                                name = "NaX",)
speciesAddenda.append(NaXESp)
KXESp = SorbedSecondarySpecies(symbol = "KX",\
                               formationReaction = [("K+",1),("X-",1)],\
                               logK25 = 0.301,\
                               name = "KX",)
speciesAddenda.append(KXESp)
#~~~~~~~~~~~~~~~~~~
# Chemical States ~
#~~~~~~~~~~~~~~~~~~
ChemicalStateList = []
columnIonicExchangers = IonicExchangers([ExchangeBindingSpecies("X-", MolesAmount(0.01, "mol"))])
columnAqueousSolution = AqueousSolution (elementConcentrations = [ElementConcentration ("Na",1.e-2,"mol/l"),
                                                                  ElementConcentration ("Cl",1.e-2,"mol/l"),
                                                                  ElementConcentration ("K",1.e-10,"mol/l")
                                                                 ],\
                                         pH = 7.0,\
                                         pe = 4,
                                         temperature = 25.0)
columnChemicalState = ChemicalState ("column",columnAqueousSolution ,ionicExchanger = columnIonicExchangers)

boundaryAqueousSolution = AqueousSolution (elementConcentrations = [ElementConcentration ("K",1.e-6,"mol/l"),
                                                                    ElementConcentration ("T",1.e-6,"mol/l"),
                                                                    ElementConcentration ("Na",1.e-2,"mol/l"),
                                                                    ElementConcentration ("Cl",1.e-2,"mol/l")
                                                                   ],\
                                           pH = 7.0,\
                                           pe = 4,
                                           temperature = 25.0)
boundaryChemicalState = ChemicalState ("boundary", boundaryAqueousSolution)

#~~~~~~~~~~~~~~~~~~~~
# Initial condition ~
#~~~~~~~~~~~~~~~~~~~~
columnIC = InitialCondition (body  = column1Body, value = columnChemicalState)
#~~~~~~~~~~~~~~~~~~~~~
# Boundary condition ~
#~~~~~~~~~~~~~~~~~~~~~
boundaryBC = BoundaryCondition (boundary = boundary0Body, btype="Dirichlet", value = boundaryChemicalState)
#~~~~~~~~~~~~~~~~~~~
# Expected outputs ~
#~~~~~~~~~~~~~~~~~~~
expectedOutputs = [ExpectedOutput("Concentration","T",format="table",name="TOutput"),
ExpectedOutput("Concentration","KX",format="table",name="KXOutput"),
ExpectedOutput("Concentration","K",format="table",name="KOutput")]
#~~~~~~~~~
# Module ~
#~~~~~~~~~
module = ChemicalTransportModule()
problem  = ChemicalTransportProblem(name               = "guitest1",\
                                    regions            = [boundary0Region,column1Region],\
                                    initialConditions  = [columnIC],\
                                    boundaryConditions = [boundaryBC],\
                                    calculationTimes   = [0.0,54000.0],\
                                    sources            = None,\
                                    darcyVelocity      = Velocity(Vector([0.000000278,0.0,0.0])),\
                                    mpiSize = 2,\
                                    chemistryDB        = "water_gui.dat",\
                                    speciesBaseAddenda = speciesAddenda,\
                                    kineticLaws        = None,\
                                    activityLaw        = None,\
                                    outputs            = expectedOutputs)
module.setData (problem, trace = 0, mesh = mesh, algorithm="CC")

module.setComponent("mt3d","phreeqc")
module.setTransportParameters("T.V.D.")
module.setTransportParameters("Jacobi",1e-15)
module.setCouplingParameter(initialTimeStep        = 2.0,
                            minTimeStep            = 20,
                            maxTimeStep            = 300,
                            couplingPrecision      = 1e-03,
                            optimalIterationNumber = 20,
                            maxIterationNumber     = 30,
                            decreaTimeStepCoef     = 0.5,
                            increaTimeStepCoef     = 1.05)
module.run()
communicator = MPI.COMM_WORLD.Dup()
if communicator.rank == 0:

    #~~~~~~~~~~~~~~~~~~
    # Post processing ~
    #~~~~~~~~~~~~~~~~~~
    K_unk     = module.getOutput('KOutput')
    KX_unk     = module.getOutput('KXOutput')
    T_unk     = module.getOutput('TOutput')
    time        = K_unk[-1][0]
    print "time",time
    KY      = K_unk[-1][1]
    TY      = T_unk[-1][1]

    XListe   = KY.getColumn(0)
    dx0 = dx[1]
    dxListe = [dx0] * (len(XListe))

    from posttables import Table

    tab1  = Table('KY')
    tab1.addColumn('X',XListe)
    tab1.addColumn('Y',KY.getColumn(1))
    tab1.addColumn('K',KY.getColumn(2))
    KY = tab1
    tab2  = Table('KT')
    tab2.addColumn('X',XListe)
    tab2.addColumn('Y',TY.getColumn(1))
    tab2.addColumn('K',TY.getColumn(2))
    TY = tab2

    from _erffunctions import *

    C0 = 1.00058350e-06
    porosity = 0.3
    darcy = 1.e-3/3600

    R = 1.  #Retardation factor for the tracer
    longDis = 6.67e-4
    AnalT = []
    from math import exp
    den = 1./(2.*sqrt(longDis*darcy*time/(porosity*R)))
    C1 = darcy*time/(porosity*R)
    x = 0.
    dx = 0.0008
    for dx in dxListe:
        x+=dx
        value = erfc((x-C1)*den)
        value1 = exp(x/longDis)*erfc((x+C1)*den)
        value = 0.5*C0*(value+value1)
        AnalT.append(value)
    tracerNorm = normMaxListComparison(TY.getColumn(2)[0:20],AnalT[0:20])
    print 'tracer norm  = ',tracerNorm

#
# R = 1 + Kd*2500*(1-porosity)/porosity (pho = 1 here)
#
    R = 1. + 2 #Retardation factor
    longDis = 6.67e-4
    AnalK = []
    from math import exp
    den = 1./(2.*sqrt(longDis*darcy*time/(porosity*R)))
    C1 = darcy*time/(porosity*R)
    x = 0.0002
    dx = 0.0004
    for dx in dxListe:
        value = erfc((x-C1)*den)
        value1 = exp(x/longDis)*erfc((x+C1)*den)
        value = 0.5*C0*(value+value1)
        AnalK.append(value)
        x+=dx
    sorptionNorm = normMaxListComparison(KY.getColumn(2)[0:20],AnalK[0:20])
    print 'sorption norm = ',sorptionNorm
    if sorptionNorm < 0.05 and tracerNorm < 0.01 :
        print "the Kd test is ok"
    else:
        print "the Kd test is ko"

    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    print "        End of the guitest1 case ~"
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

module.end()
