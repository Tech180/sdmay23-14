#include "Main.h"

/**
 * Overview: takes in a parameter (ex: ./ECU 00x) where the 00x represents 
 * the ECU type. Every line from the file that has a matching ECU type
 * will be printed.
 **/
void main(int argc, char *argv[]) {
    char *ECU_type;
    int a;
    if(argc > 0){
        ECU_type = argv[1]; //arguement passed in - something like 00x
        printf("parameter passed in: ");
	for(a=0; a < strlen(ECU_type); a++){
	  printf("%c", ECU_type[a]);
	}
	printf("\n");
    }
    //example frame: 4419.967450 1     18FEDF00x        Rx    d 8 89 AE 41 FF FF FF FF 05
    // the 00x represents engine
  
    FILE *testDataFile;
    testDataFile = fopen("../../CAN_log_files/Sept 13th Files/Full_CAN_Bus_Log.asc", "r");
    if(testDataFile == NULL){
        printf("couldn't make it to file :(");
        return;
    }
     
    int i;
    char * line = NULL;
    unsigned char lineFromFile[70];
    size_t len = 0;
    ssize_t read;
    char *lineType;
    char type[4];
    int counter=0;
    int z;

    //prints out all the lines where the main parameter (ex: 00x) 
    // is the same type as the identifier from the line in the file
    while((read = getline(&line, &len, testDataFile)) != -1){
      counter++;
      strcpy(lineFromFile, line);

      memcpy(type, &line[24], 3);
      type[3]= '\0';
      lineType = &type[0]; //set pointer to start of type array (so that we can use strcmp()

       //checking that types are equal -
      //if the parameter to main is '00x' and the line of the file has '00x' they are both engine 
      if(strcmp(ECU_type, lineType)==0){ 
	printf("\npassed if statement \n ");
	printf("line %d: %c%c%c  \n", counter, lineFromFile[24], lineFromFile[25], lineFromFile[26]);
      }
    }   
    fclose(testDataFile);
}
