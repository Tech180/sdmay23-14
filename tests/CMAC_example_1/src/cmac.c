#include "cmac.h"
#include "aes.h"
#include "common.h"
#include "utils.h"

//comments by Ryan Scehovic and Ryan Campbell
// cmac encryption
unsigned char* aes_cmac(unsigned char* in, unsigned int length, unsigned char* out, unsigned char* key)
{
    unsigned char* K1;
    unsigned char* K2;
    K1 = (unsigned char*)malloc(16);
    K2 = (unsigned char*)malloc(16);
    GenerateSubkey(key, K1, K2);

    // length is the size of the message passed in from the main method (rn it's easily 200+ chars)
    int n = (length / const_Bsize); //const_Bsize is 16 -> set in cmac.h file
    bool flag = false;
    if (length % const_Bsize != 0) { //if length is not evenly divisible by Bsize (16) add 1 because 
      n++;                           // for example 65/16 = 4.0625 then we need to cycle 5 times to 
    }                                // account for all the characters
    
    if (n == 0) { //if n=0 we know length > Bsize so we need to cycle 1 time to get all those chars
        n = 1;
    } else if (length % const_Bsize == 0) { // flag true if evenly divisble
        flag = true;
    }

    unsigned char M[n][const_Bsize]; //2d array size n(encryption rounds)  x Bsize(16)
    memset(M[0], 0, n * const_Bsize);
    memcpy(M[0], in, length);
    if (!flag) { //if flag is false (message not evenly divisible)
        memset(M[0] + length, 0x80, 1);
    }
    if (flag) {  //if flag is true (message is evenly divisible)
        block_xor(M[n - 1], M[n - 1], K1);
    } else {    //if flag is false (message not evenly divisisble)
        block_xor(M[n - 1], M[n - 1], K2);
    }

    unsigned char X[] = {
        0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00
    };
    unsigned char Y[const_Bsize];

    // will encrypt n rounds
    for (auto int i = 0; i < n - 1; i++) {
        block_xor(Y, M[i], X);
        aes_128_encrypt(Y, X, key);
    }
    block_xor(Y, M[n - 1], X); //XOR one last time (with the last output) -for message authentication?
    aes_128_encrypt(Y, out, key); //encrypting the result of XORing, pass key with it
    free(K1);
    free(K2);
    return out;
}

// Verify the CMAC
bool verify_mac(unsigned char* in, unsigned int length, unsigned char* out, unsigned char* key)
{
    bool flag = true;
    unsigned char result[16];
    aes_cmac(in, length, (unsigned char*)result, key);
    for (auto int i = 0; i < const_Bsize; i++) {
        if (!(result[i] ^ out[i])) {
            flag = false;
            break;
        }
    }

    printf("\nflag is: %d \n", flag);
    return flag;
}

// Generate the Sub keys
void GenerateSubkey(unsigned char* key, unsigned char* K1, unsigned char* K2)
{
    unsigned char const_Zero[] = {
        0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00
    };

    unsigned char const_Rb[] = {
        0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x87
    };

    unsigned char L[16];
    aes_128_encrypt(const_Zero, L, key);
    block_leftshift(K1, L);
    if (L[0] & 0x80) {
        block_xor(K1, K1, const_Rb);
    }

    block_leftshift(K2, K1);
    if (K1[0] & 0x80) {
        block_xor(K2, K2, const_Rb);
    }
}
