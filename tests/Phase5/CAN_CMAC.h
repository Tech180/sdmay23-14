#ifndef _CAN_CMAC_H_
#define _CAN_CMAC_H_


#include <openssl/bio.h> /* BasicInput/Output streams */
#include <openssl/err.h> /* errors */
#include <openssl/ssl.h> /* core library */
#include <openssl/evp.h>
#include <openssl/aes.h>
#include <openssl/rsa.h>
#include <openssl/x509.h>
#include <openssl/cmac.h>
#include <stdint.h>
#include "CAN_data.h"


#pragma GCC diagnostic ignored "-Wdeprecated-declarations"

// Receive this many 8-byte packets before sending the CMAC value
#define CMAC_MSG_COUNT 5

// The CMAC key - hard-coded is fine for now
static const uint8_t CMAC_key[] = {
    0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77,
    0x88, 0x99, 0xaa, 0xbb, 0xcc, 0xdd, 0xee, 0xff};


void get_CMAC_tag(CAN_data_s *CAN_data, int count);
extern CMAC_CTX *ctx;


#endif