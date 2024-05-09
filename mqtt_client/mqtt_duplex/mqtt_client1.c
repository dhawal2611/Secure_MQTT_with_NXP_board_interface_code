#include <stdio.h>
#include <mosquitto.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdarg.h>
#include <errno.h>
#include <ctype.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <sys/ioctl.h>
#include <netinet/in.h>
#include <net/if.h>
#include <arpa/inet.h>
#include <cjson/cJSON.h>
#include <time.h>


#define MQTT_DEBUG  0
#define BUFFER_SIZE 64

// ANSI color codes
#define RED_COLOR "\033[1;31m"      /**< Red color Define */
#define GREEN_COLOR "\033[1;32m"    /**< Green color Define */
#define RESET_COLOR "\033[0m"       /**< Reset color Define */
#define BLUE_COLOR "\033[1;34m"     /**< Blue color Define */

#define ANSI_COLOR_RED     "\x1b[31m"   /**< Ansi Color Red */
#define ANSI_COLOR_RESET   "\x1b[0m"    /**< Ansi color reset */

static struct mosquitto *mosq = NULL;
char *topic = NULL;
int rv;
int MQTT_PORT = 0;
int keepalive = 60;
bool clean_session = true;
char *CA_CERT = "../../../mqtt_broker/certs/mosquitto-certificate-authority.crt";
char *CLIENT_CRT = "../../../mqtt_broker/certs/listener03-client.crt";
char *CLIENT_KEY = "../../../mqtt_broker/certs/listener03-client.key";
char MQTT_BROKER[BUFFER_SIZE] = {0}; // IP address of the system on which broker is running
char *MQTT_TOPIC1 = "req_config_data";
char *MQTT_TOPIC2 = "config_data";
bool tls_flag = false;
bool timeout_flag = false;
bool valid_data_1 = false;

#define MQTT_QOS 1
#define MQTT_RETAIN 0
#define MAX_IP_LENGTH 16 // Maximum length of an IPv4 address (including null terminator)

char data[1024];
uint8_t flag = 0;

/**
 * @brief Debug Error
 * 
 * @param prefix 
 */
void _debugError(const char *prefix)
{
    fprintf(stderr," ==> %s%s: %s%s\n", RED_COLOR, prefix, strerror(errno), RESET_COLOR);

}

/**
 * @brief Function to print blue text to a file pointer
 * 
 * @param file 
 * @param format 
 * @param ... 
 */
void _fprintfBlue(FILE *file, const char *format, ...) 
{
    va_list args;
    va_start(args, format);
    fprintf(file,BLUE_COLOR);
    vfprintf(file,format,args);
    fprintf(file,RESET_COLOR);
    fflush(file);
    va_end(args);
}

/**
 * @brief Function to print Red text to a file pointer
 * 
 * @param file 
 * @param format 
 * @param ... 
 */
void _fprintfRed(FILE *file, const char *format, ...) 
{
    va_list args;
    va_start(args, format);
    fprintf(file,RED_COLOR);
    vfprintf(file,format,args);
    fprintf(file,RESET_COLOR);
    fflush(file);
    va_end(args);
}

/**
 * @brief Function to print Green text to a file pointer
 * 
 * @param file 
 * @param format 
 * @param ... 
 */
void _fprintfGreen(FILE *file, const char *format, ...) 
{
    va_list args;
    va_start(args, format);
    fprintf(file,GREEN_COLOR);
    vfprintf(file,format,args);
    fprintf(file,RESET_COLOR);
    fflush(file);
    va_end(args);
}

void cJSON_ErrorHandler()
{
    _fprintfRed(stderr,"Error Creating a cJSON Object! \n");
    exit(0);
}



/**
 * @brief Print Header for Chat
 * @callergraph
 * 
 */
void print_header()
{
    _fprintfBlue(stdout,"******************************* MQTT Client Example ***************************************\n");
    _fprintfBlue(stdout,"*DEMO Application to get Config Data from RMM device                                      *\n");
    _fprintfBlue(stdout,"*******************************************************************************************\n");
}

bool is_zero_initialized(const char *buffer, size_t size) 
{
    for (size_t i = 0; i < size; i++) 
    {
        if (buffer[i] != '\0') 
        {
            return false;
        }
    }

    if(!strcmp(buffer, "0.0.0.0"))
    {
        return true;
    }
    return true;
}


char* get_first_ip_address() {
    FILE* fp;
    char* command = "hostname -I";
    char output[1024]; // Buffer to store command output
    char* ip_address = (char*)malloc(MAX_IP_LENGTH * sizeof(char)); // Allocate memory for IP address

    // Open a pipe to run the command and read its output
    fp = popen(command, "r");
    if (fp == NULL) {
        printf("Failed to execute command\n");
        exit(1);
    }

    // Read command output line by line
    if (fgets(output, sizeof(output), fp) != NULL) {
        // Tokenize the output by space to extract IP addresses
        char* token = strtok(output, " ");
        while (token != NULL) {
            // Check if the token is a valid IPv4 address
            if (strlen(token) <= MAX_IP_LENGTH && strchr(token, '.') != NULL) {
                strncpy(ip_address, token, MAX_IP_LENGTH);
                break; // Found the first IP address, exit the loop
            }
            token = strtok(NULL, " ");
        }
    }

    // Close the pipe
    pclose(fp);

    return ip_address;
}

uint8_t u8GetIP() {
    int n;
    struct ifreq ifr;
    char interface_name[] = "wlxe4fac4521afb";
    //char interface_name[] = "enp1s0";
 
    n = socket(AF_INET, SOCK_DGRAM, 0);
    //Type of address to retrieve - IPv4 IP address
    ifr.ifr_addr.sa_family = AF_INET;
    //Copy the interface name in the ifreq structure
    strncpy(ifr.ifr_name , interface_name , IFNAMSIZ - 1);
    ioctl(n, SIOCGIFADDR, &ifr);
    close(n);
    _fprintfGreen(stdout,"IP Address of Interface %s - %s\n" , interface_name , inet_ntoa(((struct sockaddr_in *)&ifr.ifr_addr )->sin_addr));
    if(strstr(inet_ntoa(((struct sockaddr_in *)&ifr.ifr_addr )->sin_addr), "0.0.0.0") != NULL) {
        return -1;
    }
    sprintf(MQTT_BROKER, "%s", inet_ntoa(((struct sockaddr_in *)&ifr.ifr_addr )->sin_addr));
    _fprintfGreen(stdout,"IP Address of broker is %s\n" , MQTT_BROKER);
    return 0;
}

void message_callback(struct mosquitto *mosq, void *userdata, const struct mosquitto_message *message) {

#if MQTT_DEBUG
    if(message->payloadlen){
        _fprintfGreen(stdout,"%s %.*s\n", message->topic, (int)message->payloadlen, (char *)message->payload);
        strncpy (data, (char *)message->payload, (int)message->payloadlen);
        flag = 1;
    } else {
        printf("%s (null)\n", message->topic);
    }
#endif
    timeout_flag = true;
    _fprintfBlue(stdout,"\r\nresponse: \r\n");
    cJSON *config_data = cJSON_Parse((char*)message->payload);

    if(config_data != NULL)
    {
        cJSON *fw_version_data = cJSON_GetObjectItem(config_data, "fw_version");
        if (fw_version_data != NULL)
        {
            valid_data_1 = true;
            _fprintfGreen(stdout,"\r\nreceived FW Version: %02x\r\n", fw_version_data->valueint);
        }
        cJSON *serial_no_data = cJSON_GetObjectItem(config_data, "serial_number");
        if (serial_no_data != NULL)
        {
            valid_data_1 = true;
            _fprintfGreen(stdout,"\r\nreceived Serial No: %s\r\n", serial_no_data->valuestring);
        }
        cJSON *usb_mode_data = cJSON_GetObjectItem(config_data, "usb_mode");
        if (usb_mode_data != NULL)
        {
            valid_data_1 = true;
            switch (usb_mode_data->valueint)
            {
            case 0:
                _fprintfGreen(stdout,"\r\nreceived USB Mode: USB_DeviceStateDisable\r\n");
                break;

            case 1:
                _fprintfGreen(stdout,"\r\nreceived USB Mode: USB_DeviceStateDownstream\r\n");
                break;

            case 2:
                _fprintfGreen(stdout,"\r\nreceived USB Mode: USB_DeviceStateDiagnostics\r\n");
                break;

            case 3:
                _fprintfGreen(stdout,"\r\nreceived USB Mode: USB_HostStateUpstream\r\n");
                break;

            default:
                _fprintfRed(stdout,"\r\nreceived USB Mode: UNKNOWN\r\n");
                break;
            }
        }

        cJSON_Delete(config_data);
    }
    else
    {
        //No response received
        _fprintfRed(stderr,"Invalid response received!\n");
    }

    if(valid_data_1 == false)
    {
        _fprintfRed(stderr,"Empty response received from Device!\n");
    }
}

void display_menu() 
{
    // Display the header

    // Display the options
    _fprintfBlue(stdout,"Options:\n");
    _fprintfBlue(stdout,"1. Request Configuration data\n");
    _fprintfBlue(stdout,"2. Request Incorrect Configuration Data \n");
    _fprintfBlue(stdout,"3. Exit\n");
}


int mqtt_connect()
{
    int rc;
    _fprintfGreen(stdout,"IP is obtained successfully\n");

    mosquitto_lib_init();

    mosq = mosquitto_new(NULL, true, NULL);
    if(!mosq) {
        _fprintfRed(stderr, "Error: Out of memory.\n");
        return 1;
    }

    if(tls_flag == true)
    {
        mosquitto_tls_set(mosq, CA_CERT, NULL, CLIENT_CRT, CLIENT_KEY, NULL);
    }

    mosquitto_message_callback_set(mosq, message_callback);

    _fprintfGreen(stdout,"MQTT Broker is : %s\n", MQTT_BROKER);

    rc = mosquitto_connect(mosq, MQTT_BROKER, MQTT_PORT, 60);
    if(rc != MOSQ_ERR_SUCCESS) {
        _fprintfRed(stderr, "Error: Could not connect to MQTT broker. Return code: %d\n", rc);
        return 1;
    }

    mosquitto_subscribe(mosq, NULL, MQTT_TOPIC2, MQTT_QOS);

    mosquitto_loop_start(mosq);

}

int get_port()
{
    char input[2];
    _fprintfBlue(stdout,"Select MQTT Port: (1 or 2)\n");
    while(1)
    {
        _fprintfBlue(stdout,"1. Secure MQTT Port (8883)\n");
        _fprintfBlue(stdout,"2. Unsecure MQTT Port (1883)\n");
        if (scanf("%1s", input) != 1) { // Read a single character
            _fprintfRed(stderr,"Invalid input. Please try again.\n");
            while (getchar() != '\n'); // Clear the input buffer
            continue;
        }
        
        
        if (strcmp(input, "1") == 0 || strcmp(input, "2") == 0) {
            break; // Valid input, exit the loop
        } else {
            _fprintfRed(stderr,"Invalid input. Please try again.\n");
        }
    }

    if(input[0] = '1')
    {
        //Secure MQTT
        MQTT_PORT = 8883;
        tls_flag = true;
        if(mqtt_connect() == 1)
        {
            return 1;
        }
    }
    else if(input[0] == '2')
    {
        //Unsecure MQTT
        MQTT_PORT = 1883;
        tls_flag = false;
        if(mqtt_connect() == 1)
        {
            return 1;
        }
    }

}

void timeout_func()
{
    time_t start_time, current_time;
    double elapsed_time;

    // Get the current time
    time(&start_time);

    // Start the timer for 10 seconds
    while (true) {
        // Check if the flag is turned on
        if (timeout_flag == true) {
            timeout_flag = false;
            break;
        }

        // Get the current time
        time(&current_time);

        // Calculate elapsed time
        elapsed_time = difftime(current_time, start_time);

        // Check if 10 seconds have elapsed
        if (elapsed_time >= 10.0) {
            _fprintfRed(stderr,"Timeout: MQTT data not received\n");
            break;
        }
    }

}

int main(int argc, char *argv[]) {
    
    char input[2];

    print_header();

    //Get the MQTT Broker Address and Port
    _fprintfBlue(stdout,"Auto Getting the MQTT Broker Address... \n");

    // if(u8GetIP() == -1) 
    // {
    //     _fprintfRed(stdout,"Invalid Interface name\n");
    //     //return 0;
    // }
    strcpy(MQTT_BROKER, get_first_ip_address());
    while(1)
    {
        _fprintfBlue(stdout,"Is this MQTT Broker Address Correct? : %s (y/n)\t", MQTT_BROKER);
        if (scanf("%1s", input) != 1) { // Read a single character
            _fprintfRed(stdout,"Invalid input. Please try again.\n");
            while (getchar() != '\n'); // Clear the input buffer
            continue;
        }
        // Convert input to lowercase
        input[0] = tolower(input[0]);
        
        if (strcmp(input, "y") == 0 || strcmp(input, "n") == 0) {
            break; // Valid input, exit the loop
        } else {
            _fprintfRed(stdout,"Invalid input. Please try again.\n");
        }
    }

    if(input[0] == 'y')
    {
        //Yes, success in auto getting the address
        if(get_port() == 1)
        {
            return 1;
        }

    }
    else if(input[0] == 'n')
    {
        while (1)
        {
            // Ask the user to manually enter the addr
            memset(MQTT_BROKER, 0x00, BUFFER_SIZE);
            _fprintfBlue(stdout,"Enter Server Address: ");
            scanf("%63s", MQTT_BROKER);
            _fprintfBlue(stdout,"Is this MQTT Broker Address Correct? : %s (y/n)\t", MQTT_BROKER);
            if (scanf("%1s", input) != 1)
            { // Read a single character
                _fprintfRed(stdout,"Invalid input. Please try again.\n");
                while (getchar() != '\n')
                    ; // Clear the input buffer
                continue;
            }
            // Convert input to lowercase
            input[0] = tolower(input[0]);

            if (strcmp(input, "y") == 0 || strcmp(input, "n") == 0)
            {
                break; // Valid input, exit the loop
            }
            else
            {
                _fprintfRed(stdout,"Invalid input. Please try again.\n");
            }
        }

        if (get_port() == 1)
        {
            return 1;
        }
    }
    
    display_menu();
    _fprintfBlue(stdout,"Enter your choice: ");
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
            _fprintfBlue(stdout,"Requesting Configuration data...\n");
            cJSON *req_config_data = cJSON_CreateObject();
            if(req_config_data != NULL)
            {
                cJSON_AddBoolToObject(req_config_data,"req_fw_version", true);
                cJSON_AddBoolToObject(req_config_data,"req_serial_no", true);
                cJSON_AddBoolToObject(req_config_data,"req_usb_mode", true);
            }
            else
            {
                cJSON_ErrorHandler();
            }
            char* payload = cJSON_Print(req_config_data);
            // Call function to request configuration data
            //printf("sending payload: %s with size: %lu", payload, strlen(payload));
            mosquitto_publish(mosq, NULL, MQTT_TOPIC1, strlen(payload), payload, MQTT_QOS, MQTT_RETAIN);
            valid_data_1 = false;
            flag = 0;
            cJSON_Delete(req_config_data);
            //Implement a timeout function
            timeout_func();

            break;
        case 2:
        cJSON *req_w_config_data = cJSON_CreateObject();
            if(req_w_config_data != NULL)
            {
                cJSON_AddBoolToObject(req_w_config_data,"random_topic", true);
                cJSON_AddBoolToObject(req_w_config_data,"lorem_ipsum", true);
                cJSON_AddBoolToObject(req_w_config_data,"acv", true);
            }
            else
            {
                cJSON_ErrorHandler();
            }
            char* w_payload = cJSON_Print(req_w_config_data);
            // Call function to request configuration data
            //printf("sending payload: %s with size: %lu", payload, strlen(payload));
            mosquitto_publish(mosq, NULL, MQTT_TOPIC1, strlen(w_payload), w_payload, MQTT_QOS, MQTT_RETAIN);
            valid_data_1 = false;
            flag = 0;
            cJSON_Delete(req_w_config_data);
            timeout_func();

            break;
        case 3:
            _fprintfRed(stdout,"Exiting...\n");
            // Call function to exit
            exit(0);
            break;
        default:
            _fprintfRed(stdout,"Invalid choice!\n");
            break;
        }
    }

    mosquitto_destroy(mosq);
    mosquitto_lib_cleanup();
    return 0;
}