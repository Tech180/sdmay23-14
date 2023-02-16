#include "CAN_data.h"
#include <stdio.h>

/*

        typedef struct CAN_data_t {
                uint8_t valid;
                double timestamp_sec;
                uint8_t bus;
                uint32_t sender_ID;
                uint8_t send_recv;
                uint8_t data_len;
                uint8_t data[8];
        } CAN_data_s;*/
// 4410.003274 1     0CFFFF8Cx        Rx    d 8 99 FF FF FF FF FF FF FF
// 4419.128278 1     0J1939Tx        Rx    d 0 FF FF FF FF FF FF FF FF

CAN_data_s read_CAN_data(char CAN_Dataline[]) {

  CAN_data_s CAN_data;
  uint32_t data[8];
  char sender_ID[8];
  // hard coding for now
  uint8_t source_address; // = {0x1F};
  uint16_t pgn;           // = {0x2F3F};
  uint8_t pgn_1;
  uint8_t pgn_2;
  unsigned maskForSA = 0x000000ff;
  unsigned maskForPGN_1 = 0x00ff0000;
  unsigned maskForPGN_2 = 0x0000ff00;

  CAN_data.valid = 1;
  CAN_data.CMAC_data_len = 0;
  int scan_matches = sscanf(
      CAN_Dataline,
      "%lf %d %08xx        Rx    d %d %02x %02x %02x %02x %02x %02x %02x %02x",
      &CAN_data.timestamp_sec, &CAN_data.bus, &CAN_data.sender_ID,
      &CAN_data.data_len, &data[0], &data[1], &data[2], &data[3], &data[4],
      &data[5], &data[6], &data[7]);

  source_address = CAN_data.sender_ID & maskForSA;
  pgn_1 = (CAN_data.sender_ID & maskForPGN_1) / 0x10000;
  pgn_2 = (CAN_data.sender_ID & maskForPGN_2) / 0x0100;

  if (scan_matches != 12) {
    CAN_data.valid = 0;
    return CAN_data;
  }

  // JAZ: a quick hack: If sender_ID = 0 this is not a valid packet
  if (CAN_data.sender_ID == 0) {
    CAN_data.valid = 0;
    return CAN_data;
  }
  int i;
  for (i = 0; i < CAN_data.data_len; i++) {
    CAN_data.data[i] = (uint8_t)data[i];
  }

  // bit logic found at
  // https://stackoverflow.com/questions/1289251/converting-a-uint16-value-into-a-uint8-array2
  CAN_data.data[8] = source_address;
  CAN_data.data[9] = pgn_1;
  CAN_data.data[10] = pgn_2;
  // printf("\ndata[8]=%02X\n", data[8]);
  // printf("\ndata[9]=%02X\n", data[9]);
  // printf("\ndata[10]=%02X\n", data[10]);

  return CAN_data;
}

void print_CAN_data(CAN_data_s CAN_data) {

  printf("%lf %1x %08Xx %1X %02X %02X %02X %02X %02X %02X %02X %02X %02X %02X "
         "%02X\n",
         CAN_data.timestamp_sec, CAN_data.bus, CAN_data.sender_ID,
         CAN_data.data_len, CAN_data.data[0], CAN_data.data[1],
         CAN_data.data[2], CAN_data.data[3], CAN_data.data[4], CAN_data.data[5],
         CAN_data.data[6], CAN_data.data[7], CAN_data.data[8], CAN_data.data[9],
         CAN_data.data[10]);

  if (CAN_data.CMAC_data_len == 0)
    return;
  printf("CMAC encrypted data[%d]: ", CAN_data.CMAC_data_len);
  int i;
  for (i = 0; i < CAN_data.CMAC_data_len; i++) {
    printf("%02X ", CAN_data.CMAC_data[i]);
  }
  printf("\n");

  return;
}
