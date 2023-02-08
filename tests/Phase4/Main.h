#ifndef MAIN_H_
#define MAIN_H_

#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <openssl/bio.h> /* BasicInput/Output streams */
#include <openssl/err.h> /* errors */
#include <openssl/ssl.h> /* core library */
#include <openssl/evp.h>
#include <openssl/aes.h>
#include <openssl/rsa.h>
#include <openssl/x509.h>
#include <openssl/cmac.h>

extern void get_CMAC_tag(char line[], int count, char canData[]);

#endif /* MAIN_H_ */
