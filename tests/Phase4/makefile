CC=gcc
CFLAGS=-lssl -lcrypto
DEPS = Main.h
OBJ = Bridge.o Main.o 

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

Main: $(OBJ)
	$(CC) -o $@ $^ $(CFLAGS)
