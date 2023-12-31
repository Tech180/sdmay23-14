#define _GNU_SOURCE
#include <sys/types.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <sys/stat.h>
#include <unistd.h>

void printGoodMessage(int i);
const char* decToHexa(int n);
int genCanMsg();
int genRandom(int low, int high);

int main(int argc, char* argv[]) {
	int i = 0;

	printf("-----------PROGRAM BEGIN-----------\n");

	while (1) {
        sleep(0.1);
        printGoodMessage(i);
        i++;
		if (i % 10 == 0){
			genCanMsg(i);
            i++;
		}
	}
}

/**
  * Prints a valid CAN message with its monotonic value.
  */
void printGoodMessage(int i){
    char canValues[10][30] = {"183#0000000400001007","1DC#0200002A","1CF#80050000002D","17C#0000000010000003","13A#000000000000000A","18E#00007A","1B0#000F0000000175","18E#00006B","158#0000000000000019","166#D0320018"};
    int msgNum = rand() % 10;

    printf("%d ",i);
	for(int j = 0; j < 30; j++){
        printf("%c",canValues[msgNum][j]);
    }
    printf("\n");
}

/**
  * Generates a random CAN message (used for simulating a 'inserted message' attack)
  */
int genCanMsg(int i){
    printf("%d %X#",i,genRandom(256,1000));
    printf("%X                           <--------------------------- FAKE\n",genRandom(100000,1000000000));
    return 1;
}

/**
  * Generates a random number between two values
  */
int genRandom(int low, int high){
    return (rand() % (high - low + 1)) + low;
}