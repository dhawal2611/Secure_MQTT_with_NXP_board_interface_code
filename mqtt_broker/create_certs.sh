#!/bin/bash

create_directory() {
    directory=$1
    if [ ! -d "$directory" ]; then
        mkdir -p "$directory"
        echo "Directory '$directory' created successfully."
    else
        echo "Directory '$directory' already exists."
    fi
}

create_the_certificate_authority() {
    certs_directory=$1
    command="openssl genrsa -out ca.key 2048"
    $command
    echo "RSA key generated successfully at '$certs_directory'."

    echo -e "\033[1;31m Please enter a unique Common Name. Other fields such as Country Name, State or Province Name are optional. To skip, simply press Enter.\033[0m"
    cert_command="openssl req -new -x509 -days 3650 -key ca.key -out ca.crt"
    $cert_command
    echo "Self-signed certificate generated successfully at '$certs_directory'."
}

create_the_server_certificates() {
    certs_directory=$1
    command="openssl genrsa -out server.key 2048"
    $command
    echo "Server private key generated successfully at '$certs_directory'."

    echo -e "\033[1;31m Please enter the IP address or hostname of your MQTT server as the common name.\033[0m"
    echo -e "\033[1;31m Other fields such as Country Name, State or Province Name are optional. To skip, simply press Enter.\033[0m"
    cert_command="openssl req -new -key server.key -out server.csr"
    $cert_command
    echo "Self-signed certificate generated successfully at '$certs_directory'."

    sign_command="openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 3650"
    $sign_command
}

create_the_client_certificates() {
    certs_directory=$1
    command="openssl genrsa -out client.key 2048"
    $command
    echo "Client private key generated successfully at '$certs_directory'."

    echo -e "\033[1;31m Please enter a unique Common Name\033[0m"
    echo -e "\033[1;31m Other fields such as Country Name, State or Province Name are optional. To skip, simply press Enter.\033[0m"
    cert_command="openssl req -new -key client.key -out client.csr"
    $cert_command
    echo "Self-signed certificate generated successfully at '$certs_directory'."

    sign_command="openssl x509 -req -in client.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out client.crt -days 3650"
    $sign_command
}

configure_mosquitto() {
    current_directory=$(pwd)
    echo "Current working directory: $current_directory"
}

main() {
    certs_directory="certs"
    create_directory "$certs_directory"  # Create Directory in Current Path

    # Change directory to certs_directory
    cd "$certs_directory" || exit
    echo "Changed current directory to '$certs_directory'."

    # Create the Certificate Authority
    create_the_certificate_authority "$certs_directory"

    # Create the Server Certificates
    create_the_server_certificates "$certs_directory"

    # Create the Client Certificates
    create_the_client_certificates "$certs_directory"

    # Configure Mosquitto
    configure_mosquitto
}

main
