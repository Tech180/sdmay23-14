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
void get_CMAC_tag(char line[], int count){
  int idx; // index variable for line
  int i; // index for encrypted message
  int flag = 0; // to initialize cmac
  unsigned char canData[128]; //readLine
  int startingPoint;
  int positionInFrame;
  int indexLineFromFile = 0;
  unsigned char finalCMAC[6];
 

   printf("\nline %d: ", count); // prints line #
  // for(idx=0; idx<70; idx++){
  //  printf("%c", line[idx]);    //prints line from file data
  // }

   //usleep(1000000);

  unsigned char mact[16] = {0}; // setting empty char array for 128 bit encryption (16bytes)
    size_t mactlen;
    CMAC_CTX *ctx = CMAC_CTX_new();
	if(flag == 0)
	{
		initCMAC(flag, ctx);
	}
    //CMAC_Init(ctx, key, 16, EVP_aes_128_cbc(), NULL);

    // 5. identifies start off message to encrypt & breaks when it finds it
    //first line of file: 4410.000868 1     18FFFA13x        Rx    d 8 00 14 FF 3F FF FF FF FF
    //from that first line, this loop identifies the 'd 8' and then adds 4 which is where the 
    //     16 digits start
    for(startingPoint=0; line[startingPoint]!='\0' ; startingPoint++){
	if(line[startingPoint] == 'd' && line[startingPoint+2] == '8'){
	  startingPoint+= 4;
	  break;
	}
    }

      // 6. gets 16 digits to encrypt
      indexLineFromFile = 0;
      for(positionInFrame=startingPoint; line[positionInFrame]!='\0'; positionInFrame++){
	if(line[positionInFrame] != ' '){
	  canData[indexLineFromFile]=line[positionInFrame];
	  indexLineFromFile++;
	}
      }
    CMAC_Update(ctx, canData, sizeof(canData));
    CMAC_Final(ctx, mact, &mactlen);
     
    printf("\nCanData:");
    for(i=0; i < 16; i++){
      printf("%c", canData[i]);
    }
    printf("\nFull CMAC tag: ");
    for(i=0; i < mactlen; i++){
      printf("%X", mact[i]);
    }
    
    printf("\n"); // get the 5 bytes we want
    for(i=0; i < 5; i++){
      printf("mact[%d]: %X\n", i, mact[i]);
      finalCMAC[i]=mact[i];
      printf("finalCMAC[%d]: %X\n", i, finalCMAC[i]);
    }

  printf("\n");
  
  return;
}

//next add on encryption/decryption for each line passed in

