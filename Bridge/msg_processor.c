#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <pthread.h>
#include "msg_processor.h"

#define CAN_WIDTH 8

struct queue {
	struct message * head, * tail;
	int num_messages; 
} queue; 

struct message {	
   	int dataField[CAN_WIDTH];              
};

struct extended_message { 
	struct message* can_msgs;
   	int freshnessField[16];
	int trailerField[8];
};

int main (int argc, char **argv) { 
	char input[10];

	while(1) {
		fgets(input, 10, stdin);
		packMsg(input);
	}
}

void packMsg(char input[]) {
	static int msgCounter = 0;
	struct message can_msg = { input }; 
	struct extended_message canfd_msg = { can_msg, 0, 0};	
	msgCounter++;
	
	if(msgCounter == 5) {
		export(canfd_msg);
		msgCounter = 0; 
		canfd_msg = { struct message can_msgs, 0, 0 }
	}
}

void export(struct extended_message* canfd_msg) {
	printf("%d\n %d\n %d\n %d\n %d\n", canfd_msg->can_msgs[0], canfd_msg->can_msgs[1], 
										canfd_msg->can_msgs[2], canfd_msg->can_msgs[3], canfd_msg->can_msgs[4]);	
}