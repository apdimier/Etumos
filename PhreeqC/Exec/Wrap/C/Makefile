srcdir=$(WRAPPER)/PhreeqC/Exec/Phreeqc_source
srcdir1=$(WRAPPER)/PhreeqC/Exec/Wrap/C
VPATH =.:$(srcdir)

PYINC=/usr/include/$(PYVERSION)
PYLIB=-L/usr/lib/$(PYVERSION)/config -l$(PYVERSION) -ldl -lutil
# compilateurs
CC=gcc
CFLAGS= -O2 -fPIC -w -pthread -Wall -std=c99 -I$(srcdir1) -I$(srcdir) -I$(PYINC)

OBJECTS  = $(patsubst %.c,%.o, $(notdir $(wildcard $(srcdir1)/*.c)))

LIB_PHREEQC=$(WRAPPER)/PhreeqC/Exec/Phreeqc_source/libPhreeqc2.17_mws.a

all:  clean $(OBJECTS) comp 


%.o: %.c %.h
	$(CC) -D NO_MPI -o $@ $(CFLAGS) -c $<

comp:
	$(CC) -o $@ $(OBJECTS) $(LIB_PHREEQC) -lm $(PYLIB) -lpthread

clean: 
	rm -f *.o
