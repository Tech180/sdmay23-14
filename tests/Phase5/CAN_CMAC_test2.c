#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>

#include "CAN_data.h"
#include "CAN_CMAC.h"

#define REALTIME_SIM 0

int main (int argc, char **argv) {
  uint32_t data_len;
  char CAN_Dataline2[] = "6bc1bee22e409f96e93d7e117393172a";
  uint8_t CMAC_data[16];
	uint8_t CMAC_data_len;
  
  ctx = CMAC_CTX_new();
  CMAC_Init(ctx, CMAC_key2, 16, EVP_aes_128_cbc(), NULL);

	CMAC_Update(ctx, CAN_Dataline2, data_len);

  CMAC_Final(ctx, CMAC_data, (size_t *)&CMAC_data_len);

	return 0;
}
