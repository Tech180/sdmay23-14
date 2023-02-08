#include "Main.h"

 //assuming we get the key
static const unsigned char key[] = {    
0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77,    
0x88, 0x99, 0xaa, 0xbb, 0xcc, 0xdd, 0xee, 0xff};

/**
 * method takes in line and lineNumber from function call in ECU.c and then prints it
 **/


void initCMAC(int flag, CMAC_CTX *ctx)
{
	flag = 1;
	CMAC_Init(ctx, key, 16, EVP_aes_128_cbc(), NULL);
}
void get_CMAC_tag(char line[], int count, char canData[]){
  int idx; // index variable for line
  int i; // index for encrypted message
  int flag = 0; // to initialize cmac

  unsigned char finalCMAC[5];
 

  unsigned char mact[16]; // setting empty char array for 128 bit encryption (16bytes)
  size_t mactlen;
    CMAC_CTX *ctx = CMAC_CTX_new();
    if(flag == 0) //this is only true the first time we call this function, so it only initializes one time
	{
	  initCMAC(flag, ctx);
	}

    CMAC_Update(ctx, canData, sizeof(canData)); 

    CMAC_Final(ctx, mact, &mactlen); //CMAC tag is put into mact (size of 16)
     
    printf("\nCanData: ");
    //prints out the 80 chars (5 messages of 16 chars each went into canData)
    for(i=0; i < 80; i++){
      printf("%c", canData[i]);
    }
    printf("\nFull CMAC tag (should be 10 chars): ");
    for(i=0; i < 5; i++){
      printf("%X", mact[i]);//printing out all the hex values from mact array (should print out 10 digits each time)
    }
    
    printf("\n"); 
    // get the 5 bytes we want by moving hex values from mact to finalCMAC
    //should print out 2 chars (like "1F") for each index
    for(i=0; i < 5; i++){
      printf("mact[%d]: %2X\n", i, mact[i]);
      finalCMAC[i]=mact[i];
      printf("finalCMAC[%d]: %2X\n", i, finalCMAC[i]);
    }

  printf("\n");
  
  return;
}

//next add on encryption/decryption for each line passed in

