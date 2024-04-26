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
#include <cjson/cJSON.h>

struct mosquitto *mosq = NULL;
char *topic = NULL;
int rv;
int MQTT_PORT = 8883;
int keepalive = 60;
bool clean_session = true;
char *CA_CERT = "../../../mqtt_broker/certs/ca.crt";
char *CLIENT_CRT = "../../../mqtt_broker/certs/client.crt";
char *CLIENT_KEY = "../../../mqtt_broker/certs/client.key";
char MQTT_BROKER[64] = "192.168.1.16"; // IP address of the system on which broker is running
char *MQTT_TOPIC1 = "req_config_data";
char *MQTT_TOPIC2 = "config_data";

#define MQTT_QOS 1
#define MQTT_RETAIN 0

char data[1024];
uint8_t flag = 0;

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

    cJSON *config_data = cJSON_Parse((char*)message->payload);

    cJSON *fw_version_data = cJSON_GetObjectItem(config_data, "fw_version");
    cJSON *serial_no_data = cJSON_GetObjectItem(config_data, "serial_number");

    printf("\r\nreceived FW Version: %02x\r\n", fw_version_data->valueint);
    printf("\r\nreceived FW Version: %s\r\n", serial_no_data->valuestring);

    cJSON_Delete(config_data);
}

void display_menu() 
{
    // Display the header
    printf("MQTT Client Example\n");
    printf("-------------------\n");

    // Display the options
    printf("Options:\n");
    printf("1. Request Configuration data\n");
    printf("2. Exit\n");
}

int main(int argc, char *argv[]) {
    struct mosquitto *mosq;
    int rc;

    if(u8GetIP() == -1) {
        printf("Invalid Interface name\n");
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

    mosquitto_subscribe(mosq, NULL, MQTT_TOPIC2, MQTT_QOS);

    mosquitto_loop_start(mosq);

    // Publish a message
    //char payload[] = "Hello MQTT";
    //mosquitto_publish(mosq, NULL, MQTT_TOPIC2, sizeof(payload), payload, MQTT_QOS, MQTT_RETAIN);
    display_menu();
    printf("Enter your choice: ");
    // Wait for messages to arrive
    while (1)
    {
        

        // Get user input
        int choice;
        
        scanf("%d", &choice);

        // Process the user choice
        switch (choice)
        {
        case 1:
            printf("Requesting Configuration data...\n");
            cJSON *req_config_data = cJSON_CreateObject();
            if(req_config_data != NULL)
            {
                cJSON_AddBoolToObject(req_config_data,"req_fw_version", true);
                cJSON_AddBoolToObject(req_config_data,"req_serial_no", true);
            }
            char* payload = cJSON_Print(req_config_data);
            // Call function to request configuration data
            //printf("sending payload: %s with size: %lu", payload, strlen(payload));
            mosquitto_publish(mosq, NULL, MQTT_TOPIC1, strlen(payload), payload, MQTT_QOS, MQTT_RETAIN);
            flag = 0;
            cJSON_Delete(req_config_data);
            printf("\r\nresponse: \r\n");

            break;
        case 2:
            printf("Exiting...\n");
            // Call function to exit
            break;
        default:
            printf("Invalid choice!\n");
            break;
        }
    }

    mosquitto_destroy(mosq);
    mosquitto_lib_cleanup();
    return 0;
}