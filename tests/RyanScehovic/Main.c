#include "Main.h"

/**
 * We're assuming we get the key, so for now, we'll use this
 **/
static const unsigned char key[] = {    
0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77,    
0x88, 0x99, 0xaa, 0xbb, 0xcc, 0xdd, 0xee, 0xff,     
0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,     
0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f };

/**
 * Attempting AES-128 CTR encryption
 * 
 * 1. What it uses?
 *    - symmetric key (Sx)
 *    - plaintext (PT) 
 *    - ciphertext (CT)
 *    - counter mode 
 *
 * 2. encrpytion
 *    - inputs:  nonce, count, and Sx sent into encryption algorithm
 *    - encryption algorithm output and plaintext are XOR'ed to produce ciphertext
 * 
 * 3. decryption 
 *    - inputs: none, count+1, and Sx sent into decryption algorithm
 *    - decryption algorithm output and ciphertext are XOR'ed to produce plaintext 
 **/


void main(int argc, char *argv[]) {   
     FILE *testDataFile;
     testDataFile = fopen("../../CAN_log_files/Sept 13th Files/Full_CAN_Bus_Log.asc", "r");

     if(testDataFile == NULL){
       printf("couldn't make it to file :(");
       return;
     }

     char * line = NULL;
     size_t len = 0;
     ssize_t read;
     unsigned char text[]="hello world!";      
     unsigned char enc_out[80];      
     unsigned char dec_out[80];  
     AES_KEY enc_key, dec_key;  
     int i;
     int cycle = 0;

     // https://stackoverflow.com/questions/3501338/c-read-file-line-by-line
     // https://www.programiz.com/c-programming/c-file-input-output
     // https://wiki.openssl.org/index.php/EVP_Symmetric_Encryption_and_Decryption
     while((read = getline(&line, &len, testDataFile)) != -1 && cycle<3){
       cycle++;
       AES_set_encrypt_key(key, 128, &enc_key);      
       AES_encrypt(read, enc_out, &enc_key);       
       AES_set_decrypt_key(key,128,&dec_key);      
       AES_decrypt(enc_out, dec_out, &dec_key);       

       printf("original:\t");      
     
       for(i=0;(read+i)!=0x00;i++)       
	 printf("%X ",(read+i)); 
     
       printf("\nencrypted:\t");      
       for(i=0;*(enc_out+i)!=0x00;i++)          
	 printf("%X ",*(enc_out+i));      

       printf("\ndecrypted:\t");      
       for(i=0;*(dec_out+i)!=0x00;i++)          
	 printf("%X ",(dec_out+i));      

       printf("\n----------- end of %d cycle ------------- \n  \n  \n", cycle);

     }   
     fclose(testDataFile);
     
} 

