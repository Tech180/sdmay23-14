#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <pthread.h>

void* msgThread();                  //initializing threads and mutexes
pthread_mutex_t msgMutex;

struct queue {
	struct message * head, * tail;
	int num_messages; 
} queue; 

struct threadWork { 
	struct threadWork * next; 
	struct threadWork * prev;
	struct message * msg; 
	int msg_id; 
} threadWork; 

typedef struct message {	
	int startOfFrame;	
   	int arbitrationField;
   	int controlField;
   	int dataField;                   //all these add up to the 25bit CanFD frame
   	int CRCField;
   	int ACKField;
   	int endOfFrame;

} message;


void* msgThread(char msg){          //thread function

   	pthread_mutex_lock(&msgMutex);      //lock
   	//do something
   	pthread_mutex_unlock(&msgMutex);    //unlock
}

int main (int argc, chat **argv) {    //main method
   	startOfFrame = 0x1;
   	arbitrationField = 0x5;
   	controlField = 0x8;
   	dataField = 0x3;
   	CRCField = 0x9;
   	ACKField = 0x2;
   	endOfFrame = 0x3;
}
