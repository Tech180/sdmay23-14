CC=gcc
CFLAGS=-lssl -lcrypto
DEPS = Main.h
OBJ = CMAC.o Main.o 

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

Main: $(OBJ)
	$(CC) -o $@ $^ $(CFLAGS)
