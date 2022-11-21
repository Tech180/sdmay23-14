CC=gcc
CFLAGS=-lssl -lcrypto
DEPS = Main.h
OBJ = ECU.o Bridge.o 

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

hellomake: $(OBJ)
	$(CC) -o $@ $^ $(CFLAGS)
