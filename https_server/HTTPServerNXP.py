import json
import logging
import re
import ssl
from http.server import BaseHTTPRequestHandler, HTTPServer


class LocalData(object):
    records = {}


def APIPreProvisionlingPostDetails(self):
    print("Device PreProvisionling command")

    length = int(self.headers.get('content-length'))
    RecvData = self.rfile.read(length).decode('utf8')
    print(RecvData)
    RecvData = json.loads(RecvData)
    print(RecvData)
    print(RecvData["serviceTag"])

    if RecvData["serviceTag"] == "60Z6Z32":
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

        GroupToken = "KvM8Eo6GWw9XJcW7zikUJQ==" #Read data dynamically and then store into it.
        data = {
        "groupToken": GroupToken
        }
        DeviceMQTTData = json.dumps(data, indent=4).encode('utf-8')
        self.wfile.write(DeviceMQTTData)
        self.end_headers()
    else:
        self.send_response(404, 'Not Found: record does not exist')
        self.end_headers()

def OpenDeviceGroupLoginPostDetails(self):
    print("Device DeviceGroupLogin command")

    length = int(self.headers.get('content-length'))
    RecvData = self.rfile.read(length).decode('utf8')
    print(RecvData)
    RecvData = json.loads(RecvData)
    print(RecvData["groupToken"])

    if RecvData["groupToken"] == "defaSample#123":
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

        ID = "null" #Read data dynamically and then store into it.
        CreatedAt = "null"
        ID_Data = 740893355
        UpdatedAt = "null"
        ActiveState = True
        data = {
            "id": 0,
            "isActive": true,
            "wyseIdentifier": "wyse7825930884957594406",
            "authenticationCode": "u4z84ZE1Y7WrYUWE/geYPg==",
            "groupToken": "defaSample#123",
            "isUserAssociated" : true #User to Device association completed successfully.
        }
        DeviceMQTTData = json.dumps(data, indent=4).encode('utf-8')
        self.wfile.write(DeviceMQTTData)
        self.end_headers()
    else:
        self.send_response(404, 'Not Found: record does not exist')
        self.end_headers()


def DeviceGetMQTT(self):
    print("Device MQTT command")
    self.send_response(200)
    self.send_header('Content-Type', 'application/json')
    self.end_headers()

    #DeviceMQTTData = json.dumps({})
    # Define the values at runtime
    secure_mqtt_url = "tls://sample:8443"
    preferred_mqtt_url = "tcp://sample:1883"
    mqtt_url = "tcp://sample:1883"
    data = {
    "secureMqttUrl": secure_mqtt_url,
    "preferredMqttUrl": preferred_mqtt_url,
    "mqttUrl": mqtt_url
    }
    DeviceMQTTData = json.dumps(data, indent=4).encode('utf-8')

    #LocalData.records[0] = "Hello from Device MQTT"
    ## Return json, even though it came in as POST URL params
    #data = json.dumps(LocalData.records[0]).encode('utf-8')
    #logging.info("get record %d: %s", 0, data)
    self.wfile.write(DeviceMQTTData)
    self.end_headers()

def DeviceGetKey(self):
    print("Device Key command")
    self.send_response(200)
    self.send_header('Content-Type', 'application/json')
    self.end_headers()

    SendKeyData = "+HMHiWrt2QYULCj+VnQ0vb4UgxI1TtTqB9Xa+0bCZRE="
    SendKeyData = SendKeyData.encode('utf-8')
    self.wfile.write(SendKeyData)
    self.end_headers()

def DeviceGetCommand(self):
    print("Device get Command")
    self.send_response(200)
    self.send_header('Content-Type', 'application/json')
    self.end_headers()

    data = []
    data.append("Hello")
    data.append("World")
    print(data)
    DeviceGetCommandData = str(data).encode('utf-8')
    print(DeviceGetCommandData)

    #LocalData.records[0] = "Hello from Device MQTT"
    ## Return json, even though it came in as POST URL params
    #data = json.dumps(LocalData.records[0]).encode('utf-8')
    #logging.info("get record %d: %s", 0, data)
    self.wfile.write(DeviceGetCommandData)
    self.end_headers()

class HTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        print("Data is: ", self.path)
        print("Data is 0 : ", self.path.split('/')[0])
        print("Data is 1 : ", self.path.split('/')[1])
        print("Data is 2 : ", self.path.split('/')[2])
        print("Data is 3 : ", self.path.split('/')[3])
        if self.path.split('/')[1] == 'device':
            length = int(self.headers.get('content-length'))
            data = self.rfile.read(length).decode('utf8')
            print("Data is:", self.path.split('/')[1])
            if self.path.split('/')[2] == 'checkin':
                print("input is checkin")
            elif self.path.split('/')[2] == 'wms20' and self.path.split('/')[3] == 'fullConfig':
                print("input is wms20/fullConfig")
            elif self.path.split('/')[2] == 'heartbeat':
                print("input is heartbeat")
            elif self.path.split('/')[2] == 'genericAudit':
                print("input is genericAudit")
            elif self.path.split('/')[2] == 'status':
                print("input is status")
            else:
                self.send_response(404, 'Not Found: record does not exist')
        elif self.path.split('/')[1] == 'api':
            print("Data is:", self.path.split('/')[1])
            if self.path.split('/')[2] == 'stub-devices' and self.path.split('/')[3] == 'pre-provisioning-device':
                print("input is stub-devices/pre-provisioning-device")
                APIPreProvisionlingPostDetails(self)
            else:
                self.send_response(404, 'Not Found: record does not exist')
        elif self.path.split('/')[1] == 'open':
            print("Data is:", self.path.split('/')[1])
            if self.path.split('/')[2] == 'deviceGroupLogin':
                print("input is deviceGroupLogin")
            elif self.path.split('/')[2] == 'deviceRegister':
                print("input is deviceRegister")
            else:
                self.send_response(404, 'Not Found: record does not exist')
        else:
            self.send_response(403)
        #self.send_response(200)
        #self.send_header('Content-Type', 'application/json')
        #self.end_headers()
        #LocalData.records[0] = "{\"Hello\":\"Dhawal\"}"
        #data = json.dumps(LocalData.records[0]).encode('utf-8')
        #logging.info("get record %d: %s", 0, data)
        #self.wfile.write(data)
        #self.end_headers()

    def do_GET(self):
        print("Data is: ", self.path)
        print("Data is 0 : ", self.path.split('/')[0])
        print("Data is 1 : ", self.path.split('/')[1])
        print("Data is 2 : ", self.path.split('/')[2])
        #request_headers = self.headers
        #site_id = request_headers["Device_MAC"]
        #print("Site data is: ", site_id)
        if self.path.split('/')[1] == 'device':
            print("Data is:", self.path.split('/')[1])
            if self.path.split('/')[2] == 'mqtt':
                print("input is mqtt")
                DeviceGetMQTT(self)
            elif self.path.split('/')[2] == 'getKey':
                print("input is getKey")
                DeviceGetKey(self)
            elif re.search('getCommand', self.path):
                print("input is getCommand?wyseId=<wyseid>", self.path)
                print("Key: ", self.path.split('/')[2].split('?')[1].split('=')[0])
                print("Value: ", self.path.split('/')[2].split('?')[1].split('=')[1])
                print("Value: ", self.path.split('=')[1])
                print("Key: ", self.path.split('=')[0].split('?')[-1])
                print("Key: ", re.search(r"(?<=\?).+?(?=\=)", self.path).group())
                DeviceGetCommand(self)
            elif self.path.split('/')[2] == 'getInProgressCommand':
                print("input is getInProgressCommand")
            else:
                self.send_response(404, 'Not Found: record does not exist')


            #self.send_response(200)
            #self.send_header('Content-Type', 'application/json')
            #self.end_headers()
            #LocalData.records[0] = "Hello"
            ## Return json, even though it came in as POST URL params
            #data = json.dumps(LocalData.records[0]).encode('utf-8')
            #logging.info("get record %d: %s", 0, data)
            #self.wfile.write(data)
        else:
            self.send_response(403)
        self.end_headers()

if __name__ == '__main__':
    server = HTTPServer(('192.168.60.109', 443), HTTPRequestHandler)
    
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    #ctx.load_cert_chain(certfile='server.crt', keyfile='server.key')
    ctx.load_cert_chain("../mqtt_broker/certs/mqtt-server.crt", "../mqtt_broker/certs/mqtt-server.key")
    server.socket = ctx.wrap_socket(server.socket, server_side=True)
    logging.info('Starting httpd...\n')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()
    logging.info('Stopping httpd...\n')

