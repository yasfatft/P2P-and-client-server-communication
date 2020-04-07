// Client side C program to demonstrate Socket programming 
#include <stdio.h> 
#include <sys/socket.h> 
#include <arpa/inet.h> 
#include <unistd.h> 
#include <string.h> 
#include <time.h>
#include <stdlib.h>

struct timespec diff(struct timespec start, struct timespec end){
	struct timespec temp;
	temp.tv_sec = end.tv_sec - start.tv_sec;
	temp.tv_nsec = end.tv_nsec - start.tv_nsec;
	if (temp.tv_nsec < 0) {
		temp.tv_nsec += 1000000000 * temp.tv_sec;
		--temp.tv_sec;
	}
	return temp;
}

int main(int argc, char const *argv[]){ 
    char *serveraddress;
    int portnumber;
    char *text = "";

    // Parsing command params
    if (argc < 6){
        printf("Number of inputs is less than expected! Here is input structure:\n./client -h serveraddress -p port text\n");
        exit(EXIT_FAILURE);
    }
    else if (argc > 6){
        printf("Too much arquments! Use this structure:\n./client -h serveraddress -p port text\n");
        exit(EXIT_FAILURE);
    }

    int i;
    for (i =1; i < argc; i++)
    {
        if  (strcmp (argv[i], "-h") == 0)
        {
                serveraddress = (char *)argv[i+1];
                i++;
        }
        else if (strcmp(argv[i], "-p") == 0)
        {
                portnumber = atoi(argv[i+1]);
                i++;
        }
        else 
        {
            text = (char *)argv[i];
            break;
        }
    }
    printf("serveraddress = %s, portnumber = %d, text = %s\n", serveraddress, portnumber, text);

	// Defining & binding socket 
    int sock = 0, valread; 
	struct sockaddr_in serv_addr; 
	char buffer[1024] = {0}; 
	if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0) 
	{ 
		printf("\n Socket creation error \n"); 
		return -1; 
	} 

	serv_addr.sin_family = AF_INET; 
	serv_addr.sin_port = htons(portnumber); 
	
	// Convert IPv4 and IPv6 addresses from text to binary form 
	if(inet_pton(AF_INET, serveraddress, &serv_addr.sin_addr)<=0) 
	{ 
		printf("\nInvalid address/ Address not supported \n"); 
		return -1; 
	} 

	if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0) 
	{ 
		printf("\nConnection Failed \n"); 
		return -1; 
	}

	struct timespec time1, time2, elapsed;
	printf("Sending message...\n"); 

	clock_gettime(CLOCK_MONOTONIC, &time1);
	send(sock, text, strlen(text), 0 ); 
	valread = read(sock, buffer, 1024);
    clock_gettime(CLOCK_MONOTONIC, &time2);
    
	printf("Recived message:\n");
	printf("%s\n",buffer );
	elapsed = diff(time1,time2);
	printf("Roundtrip time: %ld.%ld sec.\n", elapsed.tv_sec, elapsed.tv_nsec);
	return 0; 
} 
