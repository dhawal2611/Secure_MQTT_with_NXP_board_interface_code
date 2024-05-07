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
    # Get the output of `hostname -I`
    output=$(hostname -I)

    # Use grep with a regular expression to extract the IPv4 address starting with "192.168."
    ipv4_address=$(echo "$output" | grep -oE '192\.168\.[0-9]+\.[0-9]+')

    certs_directory=$1

    # Define the openssl command as a string
    cert_command="openssl req -new -x509 -days 400 -extensions v3_ca -subj '/C=IN/L=Some City/CN=$ipv4_address' -keyout mosquitto-certificate-authority.key -out mosquitto-certificate-authority.crt"

    # Execute the openssl command
    eval "$cert_command"
}

create_the_server_certificates() {
    # Get the output of `hostname -I`
    output=$(hostname -I)

    # Use grep with a regular expression to extract the IPv4 address starting with "192.168."
    ipv4_address=$(echo "$output" | grep -oE '192\.168\.[0-9]+\.[0-9]+')
    certs_directory=$1
    #command="openssl genrsa -out server.key 2048"
    #$command
    command="openssl genrsa -out mqtt-server.key 2048"
    eval "$command"
    echo "Server private key generated successfully at '$certs_directory'."

    cert_command="openssl req -new -out mqtt-server.csr -key mqtt-server.key -subj '/C=FI/L=Some City/CN=$ipv4_address'"
    eval "$cert_command"
    echo "Self-signed certificate generated successfully at '$certs_directory'."

    sign_command="openssl x509 -req -days 367 -CA    mosquitto-certificate-authority.crt -CAkey mosquitto-certificate-authority.key -CAcreateserial -in  mqtt-server.csr -out mqtt-server.crt -extfile <(printf \"subjectAltName=IP:$ipv4_address\")"
    eval "$sign_command"
}

create_the_client_certificates() {
    certs_directory=$1
    command="openssl genrsa -out listener03-client.key 2048"
    eval "$command"
    echo "Client private key generated successfully at '$certs_directory'."

    cert_command="openssl req -new -out listener03-client.csr -key listener03-client.key -subj '/C=FI/L=Some City/CN=test'"
    eval "$cert_command"
    echo "Self-signed certificate generated successfully at '$certs_directory'."

    echo "Please Enter NXP Device IP Address:"
    read nxp_ip
    sign_command="openssl x509 -req -days 367 -CA mosquitto-certificate-authority.crt \
        -CAkey mosquitto-certificate-authority.key \
        -CAcreateserial \
        -in  listener03-client.csr \
        -out listener03-client.crt \
        -extfile <(printf \"subjectAltName=IP:$nxp_ip\")"
    eval "$sign_command"
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
