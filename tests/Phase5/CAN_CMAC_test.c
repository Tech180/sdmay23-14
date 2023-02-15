#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>

#include "CAN_data.h"
#include "CAN_CMAC.h"

/**
 * Overview:
 * 1) takes in a parameter (ex: ./CAN_CMAC_test file_name.asc 00x) where 
 *    file_name.asc is the CAN log, and the 00x value represents
 *    the ECU type / ID. Every line from the file that has a matching ECU type
 *    will be printed.
 * 2) uses difference of time stamps (from one 00x file line to the next 00x file line)
 *    in a usleep() call to delay the simulation of the bridge to make it more real-time
 **/

// Set to 0 to simulate as fast as possible (without the usleep() calls)
#define REALTIME_SIM 0

int main (int argc, char **argv) {

  if (argc != 3) {
		printf("Usage: %s file_name.asc CAN_IDx\n", argv[0]);
		return 0;
	}

	FILE *CAN_Datafile = fopen(argv[1], "r");
	if (!CAN_Datafile) {
		printf("Unable to open file %s\n", argv[1]);
		return 0;
	}

	// Read in the CAN_senderID from argv[2]
	uint32_t CAN_senderID;
	sscanf(argv[2], "%2xx", &CAN_senderID);
	

	// Read through the log file
	char CAN_Dataline[128];
  double lastTime = 0.0;
  double sleepTime = 0.0;
	uint32_t CMAC_count = 0;

	while (fgets(CAN_Dataline, sizeof(CAN_Dataline), CAN_Datafile) != NULL) {
		CAN_data_s CAN_data = read_CAN_data(CAN_Dataline);

		// Ignore invalid packets
		if (CAN_data.valid == 0) continue;

		// If really want real-time, have to use gettimeofday() or related functions
    if (lastTime > 0.0 && REALTIME_SIM) {
			sleepTime = (CAN_data.timestamp_sec - lastTime)*1000000;
			usleep(sleepTime);
			lastTime = CAN_data.timestamp_sec;
		}
			
		// We care about the CAN_senderID only	
		if ((CAN_data.sender_ID & 0x000000FF) == CAN_senderID) {
			print_CAN_data(CAN_data);
			get_CMAC_tag(&CAN_data, CMAC_count++);
			if (CAN_data.CMAC_data_len != 0)
				print_CAN_data(CAN_data);
			//getchar();
		}		
	}

	fclose(CAN_Datafile);
	return 0;
}