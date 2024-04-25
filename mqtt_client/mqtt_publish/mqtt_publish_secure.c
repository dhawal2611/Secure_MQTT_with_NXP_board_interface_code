#include <stdio.h>
#include <mosquitto.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

struct mosquitto *mosq = NULL;
char *topic = NULL;
int rv;
int MQTT_PORT = 8883;
int keepalive = 60;
bool clean_session = true;
char *CA_CERT = "../../../mqtt_broker/certs/ca.crt";
char *CLIENT_CRT = "../../../mqtt_broker/certs/client.crt";
char *CLIENT_KEY = "../../../mqtt_broker/certs/client.key";
char *MQTT_BROKER = "192.168.1.16";
char *MQTT_TOPIC = "lwip_topic/2";


void mosq_log_callback(struct mosquitto *mosq, void *userdata, int level, const char *str)
{
	switch (level)
	{
	//case MOSQ_LOG_DEBUG:
	//case MOSQ_LOG_INFO:
	//case MOSQ_LOG_NOTICE:
	case MOSQ_LOG_WARNING:
	case MOSQ_LOG_ERR:
	{
		printf("%i:%s\n", level, str);
	}
	}
}

int mqtt_setup(void)
{
	mosquitto_lib_init();

	mosq = mosquitto_new(NULL, clean_session, NULL);
	if (!mosq)
	{
		fprintf(stderr, "Error: Out of memory.\n");
		return -1;
	}

	mosquitto_log_callback_set(mosq, mosq_log_callback);

	rv = mosquitto_tls_set(mosq, CA_CERT, NULL, CLIENT_CRT, CLIENT_KEY, NULL);
	rv = mosquitto_tls_opts_set(mosq, 1, "tlsv1.2", NULL);
	rv = mosquitto_connect(mosq, MQTT_BROKER, MQTT_PORT, keepalive);

	if (rv != 0)
		fprintf(stderr, "mosquitto_connect failed. rv = %d\n", rv);

	return 0;
}

int main(int argc, char *argv[])
{
	if (mqtt_setup() == 0)
	{
		printf("Setup done, connected to broker. \n");
		char buffer[10];
		sprintf(buffer,"%02X", 0x09);
		rv = mosquitto_publish(mosq, NULL, MQTT_TOPIC, 2, buffer, 0, false);

		if (rv != 0)
		{
			fprintf(stderr, "mosquitto_publish failed. rv = %d\n", rv);
		}
		else
		{
			printf("mosquitto_publish successful. \n");
		}
		mosquitto_loop_forever(mosq, -1, 1);
		return 0;
	}
	else
	{
		printf("setup failed");
		return -1;
	}

	mosquitto_lib_cleanup();
	return 0;
}