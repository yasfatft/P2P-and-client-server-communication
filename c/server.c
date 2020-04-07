// Server side C/C++ program to demonstrate Socket programming 
#include <unistd.h> 
#include <arpa/inet.h>
#include <netinet/in.h>
#include <stdio.h> 
#include <sys/socket.h> 
#include <stdlib.h> 
#include <netinet/in.h> 
#include <string.h> 
#include <stdbool.h>
#include <ctype.h>
#include <sys/wait.h> 
#include <unistd.h>


// Will be used to convert a string into uppercase (each single char)
char *touppercase(char []);


int main(int argc, char const *argv[]) {
    int clientsconnected = 0;
    char *listenaddress;
    int portnumber;

    if (argc < 5){
        printf("Number of inputs is less than expected! Here is input structure:\n./server -h listenaddress -p port text\n");
        exit(EXIT_FAILURE);
    }
    else if (argc > 5){
        printf("Too much arquments! Use this structure:\n./server -h listenaddress -p port text\n");
        exit(EXIT_FAILURE);
    }

    // Parsing command params
    int i;
    for (i =1; i < argc; i++)
    {
        if  (strcmp (argv[i], "-h") == 0)
        {
                listenaddress = (char *)argv[i+1];
                i++;
        }
        else if (strcmp(argv[i], "-p") == 0)
        {
                portnumber = atoi(argv[i+1]);
                i++;
        }
    }
    printf("listenaddress = %s, portnumber = %d\n" ,listenaddress,
           portnumber);

    // Define % bind server socket
	int server_fd, new_socket, valread; 
	struct sockaddr_in address; 
	int opt = 1; 
	int addrlen = sizeof(address); 
	char buffer[1024] = {0}; 
	
	// Creating socket file descriptor 
	if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) 
	{ 
		perror("socket failed"); 
		exit(EXIT_FAILURE); 
	} 
	
	// Forcefully attaching socket to the port portnumber 
	if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &opt,
                   sizeof(opt))) 
	{ 
		perror("setsockopt"); 
		exit(EXIT_FAILURE); 
	}

	address.sin_family = AF_INET; 
	address.sin_addr.s_addr = inet_addr(listenaddress); 
	address.sin_port = htons(portnumber); 
	
	if (bind(server_fd, (struct sockaddr *)&address, sizeof(address))<0) 
	{ 
		perror("bind failed"); 
		exit(EXIT_FAILURE); 
	}

	if (listen(server_fd, 3) < 0) 
	{ 
		perror("listen"); 
		exit(EXIT_FAILURE); 
	}

    while (true){
	    if ((new_socket = accept(server_fd, (struct sockaddr *)&address, 
			(socklen_t*)&addrlen))<0){ 
		    perror("accept"); 
		    exit(EXIT_FAILURE); 
        }

        // Increase number of clients
        clientsconnected++;
        printf("Client #%d connects...\n", clientsconnected);
            
        // Handeling each client by a seprate proccess 
        pid_t pid = fork();

        if (pid == 0){
            // Client-Server message communication
            valread = read(new_socket, buffer, 1024); 
	        printf("%d)Recievd message:\n", clientsconnected);
            printf("%d)%s\n",clientsconnected, buffer ); 

            char *answer = touppercase(buffer);
	        send(new_socket, answer, strlen(answer), 0 ); 
	        printf("%d)Answer sent.\n", clientsconnected); 

            close(new_socket);
            printf("Client #%d finished it's operations.\n", clientsconnected);
	        return 0; 
        }
    }
    wait(NULL); 
    return 0;
} 


char *touppercase(char request[])
{
    int j =0;
    while (request[j])
    {
        request[j] = toupper(request[j]);
        j++;
    }
    return request;
}
