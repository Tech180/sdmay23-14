#include "Main.h"

static const unsigned char key[] = {
    0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77,
    0x88, 0x99, 0xaa, 0xbb, 0xcc, 0xdd, 0xee, 0xff,
    0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
    0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f
};

int main(int argc, char *argv[]){

  // 1. locate file & open with read permission
    FILE *testDataFile;
     testDataFile = fopen("../../CAN_log_files/Sept 13th Files/Full_CAN_Bus_Log.asc", "r");

  // 2. make sure file was found
     if(testDataFile == NULL){
       printf("couldn't make it to file :(");
       return;
     }

  // 3. define variables for encryption/decryption process
    char *line = NULL;
    size_t len = 0;
    ssize_t read;
    unsigned char lineFromFile[70];
    unsigned char canData[128]; //readLine

  // 4. read in first line from file & copy it into array
    read = getline(&line, &len, testDataFile);
    strcpy(lineFromFile, line);
    printf("read = %d", read); //count of how much was read from file

  // 5. identifies start off message to encrypt & breaks when it finds it
    int startingPoint;
    for(startingPoint=0; lineFromFile[startingPoint]!='\0' ; startingPoint++){
      if(lineFromFile[startingPoint] == 'd' && lineFromFile[startingPoint+2] == '8'){
	startingPoint+= 4;
	break;
      }
    }

  // 6. gets 16 digits to encrypt
    int positionInFrame;
    int indexLineFromFile = 0;
    for(positionInFrame=startingPoint; lineFromFile[positionInFrame]!='\0'; positionInFrame++){
      if(lineFromFile[positionInFrame] != ' '){
	canData[indexLineFromFile]=lineFromFile[positionInFrame];
        indexLineFromFile++;
      }
    }

  // 7. declare variables for encryption/decryption process
    unsigned char enc_out[128];
    unsigned char dec_out[17];

    AES_KEY enc_key, dec_key;

    AES_set_encrypt_key(key, 128, &enc_key);
    AES_encrypt(canData, enc_out, &enc_key);      

    AES_set_decrypt_key(key,128,&dec_key);
    AES_decrypt(enc_out, dec_out, &dec_key);


    printf("\n canData:   ");
    int c;
    for(c=0; canData[c] != '\0'; c++){
      printf("%c", canData[c]);
    }

    printf(" encrypted: ");
    for(c=0; enc_out[c] != '\0'; c++){
      printf("%c", enc_out[c]);
    }

    printf("\n decrypted: "); //get a weird character when doing dec_out[c] != '\0' but not when c<16
    for(c=0; dec_out[c] != '\0'; c++){
      printf("%c", dec_out[c]);
    }
    printf("\n");

    return 0;
}
