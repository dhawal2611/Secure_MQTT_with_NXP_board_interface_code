# MQTT broker setup

- To Create SSL-TSL certificates
    [Setup Secure Mosquitto borker](https://medium.com/gravio-edge-iot-platform/how-to-set-up-a-mosquitto-mqtt-broker-securely-using-client-certificates-82b2aaaef9c8)

 - **Follow steps in section "Now let’s make it secure using Client Certificates"
        in above link to create certificates.**

* OR To create SSL-TSL certificates automatically
<<<<<<< HEAD
    * sh create_certs.sh
    * Note: Make sure use different "common name" wherever required.
    * Note: Common name while creating server certificate use system IP address on which broker is running.

* To start the broker use below command
    * sh start_server.sh

- Command to start mosquitto broker manually 
    ```
    mosquitto -c <Path to mosquitto1.conf file> -v
    ```
=======
    ``` sh create_certs.sh ```

> [!NOTE]
> Note: Make sure use different "common name" wherever required.
> Note: Common name while creating server certificate use system IP address on which broker is running.

* To start the broker use below command
    * sh start_server.sh

- Command to start mosquitto broker manually 
    ``` mosquitto -c <Path to mosquitto_c.conf file> -v ```
>>>>>>> 9f7ab2e (Update README files)





