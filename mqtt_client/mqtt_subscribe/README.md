# MQTT Client subscribe

- mqtt_subscribe_secure.c
    - subscribe the data from secure mqtt connection using ssl certificate.
- mqtt_subscribe_non_secure.c
    - subscribe the data from Non-secure mqtt connection.

* Compilation steps
    * gcc mqtt_subscribe_secure.c -o mqtt_publish_mqtt_subscribe_securesecure -lmosquitto
    * gcc mqtt_subscribe_non_secure.c -o mqtt_subscribe_non_secure -lmosquitto

* Run Executable Binaries
    * ./mqtt_subscribe_secure
    * ./mqtt_subscribe_non_secure