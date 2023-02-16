#define _GNU_SOURCE
#include <sys/types.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <sys/stat.h>


int main(int argc, char* argv[]) {
	FILE *f;
	f = fopen("sample-can.log", "r");
	char buffer[50];
	int i = 0;
	
	printf("-----------FILE OPENED-----------\n");
	while ((fgets (buffer, sizeof(buffer), f))!= NULL) {
		printf("%s",buffer);
		i++;

		if (i % 100 == 0){
			printf("EVIL MESSAGE!!!!! -----------------------------------------------\n");
			//printf("(1398128223.808970) can0 143#6A9B04D3\n");
			printf("%s",buffer);
			printf("EVIL MESSAGE!!!!! -----------------------------------------------\n");
		}
	}
	fclose(f);
}

int generateRandomCanMessage(){
	return 1;
}