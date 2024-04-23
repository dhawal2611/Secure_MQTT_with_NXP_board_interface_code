#include <stdio.h>
#include <mosquitto.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

struct mosquitto *mosq = NULL;
char *topic = NULL;
int MQTT_PORT = 8883;
int keepalive = 60;
bool clean_session = true;
char *CA_CERT = "/workspaces/test/mqtt_server/certs/ca.crt";
char *CLIENT_CRT = "/workspaces/test/mqtt_server/certs/client.crt";
char *CLIENT_KEY = "/workspaces/test/mqtt_server/certs/client.key";
char *MQTT_BROKER = "127.0.0.1";
char *MQTT_TOPIC = "/topic";


void on_connect(struct mosquitto *mosq, void *obj, int rc) {
	printf("ID: %d\n", * (int *) obj);
	if(rc) {
		printf("Error with result code: %d\n", rc);
		exit(-1);
	}
	mosquitto_subscribe(mosq, NULL, MQTT_TOPIC, 0);
}

void on_message(struct mosquitto *mosq, void *obj, const struct mosquitto_message *msg) {
	printf("New message with topic %s: %s\n", msg->topic, (char *) msg->payload);
}

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

int main() {
	int rc, id=12;

	mosquitto_lib_init();

	struct mosquitto *mosq;

	mosq = mosquitto_new("subscribe-test", true, &id);
	mosquitto_connect_callback_set(mosq, on_connect);
	mosquitto_message_callback_set(mosq, on_message);


	mosquitto_log_callback_set(mosq, mosq_log_callback);

	rc = mosquitto_tls_set(mosq, CA_CERT, NULL, CLIENT_CRT, CLIENT_KEY, NULL);
	rc = mosquitto_tls_opts_set(mosq, 1, NULL, NULL);
	rc = mosquitto_connect(mosq, MQTT_BROKER, MQTT_PORT, keepalive);
	
	//rc = mosquitto_connect(mosq, "localhost", 1883, 10);
	if(rc) {
		printf("Could not connect to Broker with return code %d\n", rc);
		return -1;
	}

	mosquitto_loop_start(mosq);
	printf("Press Enter to quit...\n");
	getchar();
	mosquitto_loop_stop(mosq, true);

	mosquitto_disconnect(mosq);
	mosquitto_destroy(mosq);
	mosquitto_lib_cleanup();

	return 0;
}
