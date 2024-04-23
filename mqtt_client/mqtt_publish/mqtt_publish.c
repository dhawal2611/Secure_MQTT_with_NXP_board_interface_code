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
char *CA_CERT = "/workspaces/test/mqtt_server/certs/ca.crt";
char *CLIENT_CRT = "/workspaces/test/mqtt_server/certs/client.crt";
char *CLIENT_KEY = "/workspaces/test/mqtt_server/certs/client.key";
char *MQTT_BROKER = "127.0.0.1";
char *MQTT_TOPIC = "/topic";


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
	rv = mosquitto_tls_opts_set(mosq, 1, NULL, NULL);
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

		rv = mosquitto_publish(mosq, NULL, MQTT_TOPIC, 11, "hello world", 0, false);

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