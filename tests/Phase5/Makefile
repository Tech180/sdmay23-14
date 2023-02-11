CC=gcc
CFLAGS=-lssl -lcrypto -Wno-deprecated
DEPS = $(wildcard *.h)
EXEC = CAN_CMAC_test
SRC = $(wildcard *.c)

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

$(EXEC): $(SRC:%.c=%.o)
	$(CC) -o $@ $^ $(CFLAGS)

clean:
	rm -f $(OBJ) *.o $(EXEC) *~




