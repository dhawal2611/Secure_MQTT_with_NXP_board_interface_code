# MQTT Client Publish

mqtt_publish_secure.c
    Publish the data to secure mqtt connection using ssl certificate.
mqtt_publish_non_secure.c
    Publish the data to Non-secure mqtt connection.

Compilation steps
    gcc mqtt_publish_secure.c -o mqtt_publish_secure -lmosquitto
    gcc mqtt_publish_non_secure.c -o mqtt_publish_non_secure -lmosquitto

Run Executable Binaries
    ./mqtt_publish_secure
    ./mqtt_publish_non_secure