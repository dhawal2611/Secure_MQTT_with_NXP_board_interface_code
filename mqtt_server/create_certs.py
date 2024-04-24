import os
import subprocess

def create_directory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Directory '{directory}' created successfully.")
        else:
            print(f"Directory '{directory}' already exists.")
    except OSError as e:
        print(f"Error: {e}")

def create_the_certificate_authority(certs_directory):
    try:
        command = f"openssl genrsa -out ca.key 2048"
        subprocess.run(command, shell=True, check=True)
        print(f"RSA key generated successfully at '{certs_directory}'.")
        
        # Generate self-signed certificate
        
        print("\033[1;31m Please enter a unique Command name. Other fields such as Country Name, State or Province Name are optional. To skip, simply press Enter.\033[0m")
        cert_command = f"openssl req -new -x509 -days 3650 -key ca.key -out ca.crt"
        subprocess.run(cert_command, shell=True, check=True)
        print(f"Self-signed certificate generated successfully at '{certs_directory}'.")
        
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        
        
def create_the_server_certificates(certs_directory):
    try:
        command = f"openssl genrsa -out server.key 2048"
        subprocess.run(command, shell=True, check=True)
        print(f"Server private key generated successfully at '{certs_directory}'.")
        
        print("\033[1;31m Please enter the IP address or hostname of your MQTT server as the common name.\033[0m")
        print("\033[1;31m Other fields such as Country Name, State or Province Name are optional. To skip, simply press Enter.\033[0m")
        cert_command = f"openssl req -new -key server.key -out server.csr"
        subprocess.run(cert_command, shell=True, check=True)
        print(f"Self-signed certificate generated successfully at '{certs_directory}'.")
        
        sign_command = f"openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 3650"
        subprocess.run(command, shell=True, check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        
        
        
def create_the_client_certificates(certs_directory):
    try:
        command = f"openssl genrsa -out client.key 2048"
        subprocess.run(command, shell=True, check=True)
        print(f"client private key generated successfully at '{certs_directory}'.")
        
        print("\033[1;31m Please enter a unique Command name\033[0m")
        print("\033[1;31m Other fields such as Country Name, State or Province Name are optional. To skip, simply press Enter.\033[0m")
        cert_command = f"openssl req -new -key client.key -out client.csr"
        subprocess.run(cert_command, shell=True, check=True)
        print(f"Self-signed certificate generated successfully at '{certs_directory}'.")
        
        sign_command = f"openssl x509 -req -in client.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out client.crt -days 3650"
        subprocess.run(command, shell=True, check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    	

def configure_mosquitto():
    current_directory = os.getcwd()
    print("Current working directory:", current_directory)
    
    
    

def main():
    certs_directory = "certs"
    create_directory(certs_directory)  #Create Directory in Current Path
    
    # Change directory to certs_directory
    os.chdir(certs_directory)
    print(f"Changed current directory to '{certs_directory}'.")
    

    #Create the Certificate Authority
    create_the_certificate_authority(certs_directory)
    
    #Create the Server Certificates
    create_the_server_certificates(certs_directory);
    
    #Create the Client Certificates
    create_the_client_certificates(certs_directory);
    
    #Configure Mosquitto
    configure_mosquitto();

if __name__ == "__main__":
    main()

