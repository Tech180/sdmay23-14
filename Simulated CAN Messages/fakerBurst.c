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
    	char c;
	int press = 0;
	char *buf = " 183#0000000400001007\n";
	printf("-----------PROGRAM BEGIN-----------\n");

	while (1) {
		
		if(getc(stdin) > 0){
			c = getc(stdin);
		}
		
		if(c != 79){
			sleep(1);
		}
		
		if(c == 49){
			buf = " 183#0000000400001007\n";
		}
	
		if(c == 50){
			buf = " 1DC#0200002A\n";
		}
	
		if(c == 51){
			buf = " 1CF#80050000002D\n";
		}
	
		if(c == 52){
			buf = " 17C#0000000010000003\n";
		}
	
		if(c == 53){
			buf = " 13A#000000000000000A\n";
		}
		
		char iValue[50] = "";
		sprintf(iValue, "%d", i);
		strcat(iValue,buf);
		write(fileno(stdout),iValue,strlen(iValue)+1);
		i++;
	}
}