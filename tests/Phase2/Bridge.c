#include "Main.h"

 //assuming we get the key
static const unsigned char key[] = {    
0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77,    
0x88, 0x99, 0xaa, 0xbb, 0xcc, 0xdd, 0xee, 0xff,     
0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,     
0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f };

/**
 * method takes in line and lineNumber from function call in ECU.c and then prints it
 **/
void passLineFromFile(char line[], int count){
  int idx;
  printf("\nline %d: ", count);
  for(idx=0; idx<70; idx++){
    printf("%c", line[idx]);
  }

  return;
}

//next add on encryption/decryption for each line passed in
