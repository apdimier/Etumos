top_builddir=$(WRAPPER)
srcdir=$(WRAPPER)/PhreeqC/Exec/Wrap

vpath %.py $(srcdir)

EXPORT_PYSCRIPTS = phreeqccomponent.py

CC=gcc 
CFLAGS= -O2 -fPIC -fno-strict-aliasing -pthread -Wall -Wstrict-prototypes
LIB_PHREEQC=$(WRAPPER)/PhreeqC/Exec/Phreeqc_source/libPhreeqc2.18_mws.a
#
#OBJECTS= $(wildcard C/*.o)
OBJECTS= $(patsubst %.c,%.o, $(addprefix $(srcdir)/C/,$(notdir $(wildcard $(srcdir)/C/*.c))))
#
bin: all
all: dirC lib WPhreeqc.so 

inc depend depend_idl lib resources :;

dirC:
	cd Wrap/C; $(MAKE)

lib:
	cd Phreeqc_source; $(MAKE)

WPhreeqc.so: $(OBJECTS) $(LIB_PHREEQC)
	$(CC) $(CFLAGS) -shared $(OBJECTS) $(LIB_PHREEQC) $(LIB_NCURSES) $(LIB_G2C) -o $@
	cp  $@  $(top_builddir)/Wlib/.
	cd Wrap/C; $(MAKE) clean
	
lclean:
	rm -f core *~ *.so fort.* *.pyc
	rm -f *.dat
	rm -f *.pqi

clean: lclean 
	cd Wrap/C; make clean

