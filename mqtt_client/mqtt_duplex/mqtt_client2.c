#include <stdio.h>
#include <mosquitto.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/ioctl.h>
#include <netinet/in.h>
#include <net/if.h>
#include <arpa/inet.h>

struct mosquitto *mosq = NULL;
char *topic = NULL;
int rv;
int MQTT_PORT = 8883;
int keepalive = 60;
bool clean_session = true;
char *CA_CERT = "../../../mqtt_broker/certs/ca.crt";
char *CLIENT_CRT = "../../../mqtt_broker/certs/client.crt";
char *CLIENT_KEY = "../../../mqtt_broker/certs/client.key";
char MQTT_BROKER[64] = "172.17.0.1"; // IP address of the system on which broker is running
char *MQTT_TOPIC1 = "/topic1";
char *MQTT_TOPIC2 = "/topic2";

#define MQTT_QOS 1
#define MQTT_RETAIN 0

uint8_t u8GetIP() {
    int n;
    struct ifreq ifr;
    char interface_name[] = "enp1s0";
 
    n = socket(AF_INET, SOCK_DGRAM, 0);
    //Type of address to retrieve - IPv4 IP address
    ifr.ifr_addr.sa_family = AF_INET;
    //Copy the interface name in the ifreq structure
    strncpy(ifr.ifr_name , interface_name , IFNAMSIZ - 1);
    ioctl(n, SIOCGIFADDR, &ifr);
    close(n);
    printf("IP Address is %s - %s\n" , interface_name , inet_ntoa(((struct sockaddr_in *)&ifr.ifr_addr )->sin_addr));
    if(strstr(inet_ntoa(((struct sockaddr_in *)&ifr.ifr_addr )->sin_addr), "0.0.0.0") != NULL) {
        return -1;
    }
    sprintf(MQTT_BROKER, "%s", inet_ntoa(((struct sockaddr_in *)&ifr.ifr_addr )->sin_addr));
    printf("IP Address of broker is %s\n" , MQTT_BROKER);
    return 0;
}

void message_callback(struct mosquitto *mosq, void *userdata, const struct mosquitto_message *message) {
    if(message->payloadlen){
        printf("%s %.*s\n", message->topic, (int)message->payloadlen, (char *)message->payload);
    } else {
        printf("%s (null)\n", message->topic);
    }
}

int main(int argc, char *argv[]) {
    struct mosquitto *mosq;
    int rc;

    if(u8GetIP() == -1) {
        printf("Invalide Interface name\n");
        return 0;
    }
    printf("IP is successfully\n");

    mosquitto_lib_init();

    mosq = mosquitto_new(NULL, true, NULL);
    if(!mosq) {
        fprintf(stderr, "Error: Out of memory.\n");
        return 1;
    }

    mosquitto_tls_set(mosq, CA_CERT, NULL, CLIENT_CRT, CLIENT_KEY, NULL);

    mosquitto_message_callback_set(mosq, message_callback);

    printf("MQTT Broker is : %s\n", MQTT_BROKER);

    rc = mosquitto_connect(mosq, MQTT_BROKER, MQTT_PORT, 60);
    if(rc != MOSQ_ERR_SUCCESS) {
        fprintf(stderr, "Error: Could not connect to MQTT broker. Return code: %d\n", rc);
        return 1;
    }

    // Publish a message
    //char payload[] = "Hello MQTT";
    //mosquitto_publish(mosq, NULL, MQTT_TOPIC1, sizeof(payload), payload, MQTT_QOS, MQTT_RETAIN);

    mosquitto_subscribe(mosq, NULL, MQTT_TOPIC2, MQTT_QOS);
    mosquitto_loop_start(mosq);

    // Wait for messages to arrive
    while(1) {
        char payload[] = "Hello MQTT1";
        mosquitto_publish(mosq, NULL, MQTT_TOPIC1, sizeof(payload), payload, MQTT_QOS, MQTT_RETAIN);

        
        // Main loop can be used for other tasks
        for(int i=0; i< 10; i++)
            usleep(1000000);
    }

    mosquitto_destroy(mosq);
    mosquitto_lib_cleanup();
    return 0;
}