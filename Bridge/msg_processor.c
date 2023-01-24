#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <pthread.h>

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
