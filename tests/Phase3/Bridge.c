#include "Main.h"

 //assuming we get the key
static const unsigned char key[] = {    
0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77,    
0x88, 0x99, 0xaa, 0xbb, 0xcc, 0xdd, 0xee, 0xff};

/**
 * method takes in line and lineNumber from function call in ECU.c and then prints it
 **/
void passLineFromFile(char line[], int count){
  int idx;
  int i;

 

  printf("\nline %d: ", count);
  for(idx=0; idx<70; idx++){
    printf("%c", line[idx]);    
  }

  // usleep(2500000);

  unsigned char mact[16] = {0}; 
    size_t mactlen;
    CMAC_CTX *ctx = CMAC_CTX_new();
    CMAC_Init(ctx, key, 16, EVP_aes_128_cbc(), NULL);
    CMAC_Update(ctx, mact, sizeof(mact));
    CMAC_Final(ctx, mact, &mactlen);
      
    printf("encrypted CMAC: ");
    for(i=0; i < mactlen; i++){
      printf("%X", mact[i]);
    }

    
  printf("\n");
  
  return;
}

//next add on encryption/decryption for each line passed in

