struct message;
struct extended_message;

void packMsg(char input[]);
void export(struct extended_message* canfd_msg);