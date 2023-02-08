#ifndef _CAN_DATA_H_
#define _CAN_DATA_H_

#include <stdint.h>

	typedef struct CAN_data_t {
		uint8_t valid;
		double timestamp_sec;
		uint32_t bus;
		uint32_t sender_ID;
		uint8_t send_recv;
		uint32_t data_len;
		uint8_t data[8];
		uint32_t CMAC_data_len;
		uint8_t CMAC_data[16];
	} CAN_data_s;

	CAN_data_s read_CAN_data(char CAN_Dataline[]);
	void print_CAN_data(CAN_data_s CAN_data);

#endif