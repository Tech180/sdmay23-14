#define _GNU_SOURCE
#include <sys/types.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <sys/stat.h>
#include <windows.h>
#include <io.h>
#include <conio.h>

void printGoodMessage(int i);
const char* decToHexa(int n);
int genCanMsg();
int genRandom(int low, int high);

void changeMessage(char c, char *buf);

int main(int argc, char* argv[]) {
	int i = 0;
    char c;
	int press = 0;
	char *buf = " 183#0000000400001007\n";
	printf("-----------PROGRAM BEGIN-----------\n");

	while (1) {
		
		if(kbhit()){
			c = getch();
		}
		
		if(c != 79){
			Sleep(10);
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
	
		changeMessage(c,buf);
		
		char iValue[50] = "";
		itoa(i,iValue,10);
		strcat(iValue,buf);
		_write(fileno(stdout),iValue,strlen(iValue)+1);
		i++;
	}
}