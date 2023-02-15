#include "CAN_CMAC.h"

CMAC_CTX *ctx;

void get_CMAC_tag(CAN_data_s *CAN_data, int count) {

  static uint8_t first_CMAC = 1;
	
  // First time (on system startup), initialize the CMAC
  if (first_CMAC == 1) {
    first_CMAC = 0;
    ctx = CMAC_CTX_new();
    CMAC_Init(ctx, CMAC_key, 16, EVP_aes_128_cbc(), NULL);
  }
  // CMAC_Init(CMAC_CTX *ctx, const void *key, size_t key_len, const EVP_CIPHER
  // *cipher, ENGINE *impl);
  // If ctx is already initialized, CMAC_Init() can be called again with key,
  // cipher, and impl all set to NULL and key_len set to 0. In that case, any
  // data already processed is discarded and ctx is re-initialized to start
  // reading data anew.

  if (count % CMAC_MSG_COUNT == 0) {
    CMAC_Init(ctx, NULL, 0, NULL, NULL);
  }

  // CMAC_Update(CMAC_CTX *ctx, const void *in_data, size_t in_len);
  // CMAC_Update() processes in_len bytes of input data pointed to by in_data.
  // Depending on the number of input bytes already cached in ctx, on in_len,
  // and on the block size, this may encrypt zero or more blocks. Unless in_len
  // is zero, this function leaves at least one byte and at most one block of
  // input cached but unprocessed inside the ctx object. CMAC_Update() can be
  // called multiple times to concatenate several chunks of input data of
  // varying sizes.
  CMAC_Update(ctx, CAN_data->data, CAN_data->data_len);

	uint8_t CMAC_data[16];
	uint8_t CMAC_data_len;
  if (count % CMAC_MSG_COUNT == CMAC_MSG_COUNT - 1) {
    CMAC_Final(ctx, CMAC_data, (size_t *)&CMAC_data_len);
		CAN_data->CMAC_data_len = CMAC_data_len;
		for (int i  = 0; i < CMAC_data_len; i++) {
			CAN_data->CMAC_data[i] = CMAC_data[i];
		}	
  }

	//CMAC_Final(CMAC_CTX *ctx, unsigned char *out_mac, size_t *out_len);
  // CMAC_Final() stores the length of the message authentication code in bytes,
  // which equals the cipher block size, into *out_len. Unless out_mac is NULL,
  // it encrypts the last block, padding it if required, and copies the
  // resulting message authentication code to out_mac. The caller is responsible
  // for providing a buffer of sufficient size.

  return;
}
