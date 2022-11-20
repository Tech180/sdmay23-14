#include "Main.h"

void main(int argc, char *argv[]) {   
    FILE *testDataFile;
    testDataFile = fopen("../../CAN_log_files/Sept 13th Files/Full_CAN_Bus_Log.asc", "r");

    if(testDataFile == NULL){
        printf("couldn't make it to file :(");
        return;
    }
     
    int i;
    while((read = getline(&line, &len, testDataFile)) != -1 && cycle<3){
        printf("original:\t");      
        for(i=0;(read+i)!=0x00;i++)       
	        printf("%X ",(read+i)); 
     }   
     fclose(testDataFile);
     
}
