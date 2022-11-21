CC=gcc
CFLAGS=-lssl -lcrypto
DEPS = Main.h
OBJ = Bridge.o ECU.o 

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

Main: $(OBJ)
	$(CC) -o $@ $^ $(CFLAGS)
