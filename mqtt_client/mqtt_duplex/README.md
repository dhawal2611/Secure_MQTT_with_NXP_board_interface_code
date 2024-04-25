# MQTT Secure duplex communication.

mqtt_client1.c
mqtt_client2.c
    Duplex communication of Pub and Sub between Client1 and Client2
    via secure channel.

**Note: Update the interface name with the system generated interface name**

Compilation steps
    gcc mqtt_client1.c -o mqtt_client1 -lmosquitto
    gcc mqtt_client2.c -o mqtt_client2 -lmosquitto

Run Executable Binaries
    ./mqtt_client1
    ./mqtt_client2