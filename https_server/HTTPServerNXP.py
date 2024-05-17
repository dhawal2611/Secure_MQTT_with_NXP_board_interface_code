import json
import logging
import re
import ssl
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer


HTTPS_ENABLED = True
VERIFY_USER = True

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

        GroupToken = "isActiveKvM8Eo6GWw9XJcW7zikUJQ==" #Read data dynamically and then store into it.
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
        ActiveState = "true"
        data = {
            "_id": ID,
            "createdAt": CreatedAt,
            "id": ID_Data,
            "updatedAt": UpdatedAt,
            "isActive": ActiveState,
        }
        DeviceMQTTData = json.dumps(data, indent=4).encode('utf-8')
        self.wfile.write(DeviceMQTTData)
        self.end_headers()
    else:
        self.send_response(404, 'Not Found: record does not exist')
        self.end_headers()

def OpenDeviceRegisterPostDetails(self):
    print("Device Device Register Post command")

    length = int(self.headers.get('content-length'))
    RecvData = self.rfile.read(length).decode('utf8')
    RecvData = json.loads(RecvData)
    print(RecvData)

    if RecvData["groupToken"] == "defaSample#123":
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

        ID = 0 #Read data dynamically and then store into it.
        ActiveState = "true"
        WYSEID = "wyse7825930884957594406"
        AUTHCode = "u4z84ZE1Y7WrYUWE/geYPg=="
        GRPToken = "defaSample#123"
        UserAss = "true"
        data = {
            "id": ID,
            "isActive": ActiveState,
            "wyseIdentifier": WYSEID,
            "authenticationCode": AUTHCode,
            "groupToken": GRPToken,
            "isUserAssociated" : UserAss #User to Device association completed successfully.
        }
        DeviceMQTTData = json.dumps(data, indent=4).encode('utf-8')
        self.wfile.write(DeviceMQTTData)
        self.end_headers()
    else:
        self.send_response(404, 'Not Found: record does not exist')
        self.end_headers()



def DeviceGetMQTT(self):
    print("Device Get MQTT command")
    self.send_response(200)
    self.send_header('Content-Type', 'application/json')
    self.end_headers()

    secure_mqtt_url = "tls://sample:8443"
    preferred_mqtt_url = "tcp://sample:1883"
    mqtt_url = "tcp://sample:1883"
    data = {
    "secureMqttUrl": secure_mqtt_url,
    "preferredMqttUrl": preferred_mqtt_url,
    "mqttUrl": mqtt_url
    }
    DeviceMQTTData = json.dumps(data, indent=4).encode('utf-8')

    self.wfile.write(DeviceMQTTData)
    self.end_headers()

def DeviceGetKey(self):
    print("Device Get Key command")
    self.send_response(200)
    self.send_header('Content-Type', 'application/json')
    self.end_headers()

    SendKeyData = "+HMHiWrt2QYULCj+VnQ0vb4UgxI1TtTqB9Xa+0bCZRE="
    SendKeyData = SendKeyData.encode('utf-8')
    self.wfile.write(SendKeyData)
    self.end_headers()

def PostDeviceCheckin(self):
    print("Device Device Checkin command")

    length = int(self.headers.get('content-length'))
    RecvData = self.rfile.read(length).decode('utf8')
    print(RecvData)
    RecvData = json.loads(RecvData)
    print(RecvData)

    if RecvData["serialNum"] == "55GMGK3":
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

        null = "null"
        false = "false"
        true = "true"
        data = {
            "deviceElements": null,
            "deviceElementsV2": null,
            "configSettings": null,
            "dynamicGroupPolicies": null,
            "deviceExceptionPolicies": null,
            "fullConfiguration": false,
            "shouldSendRemoteCommand": false,
            "isJailBroken": false,
            "compliantStatus": 1,
            "configCompliantStatus": 0,
            "passcodeCompliant": true,
            "encryptionCompliantStatus": 1,
            "computeJailbreak": true,
            "isCaValidationOn": true,
            "personInfoLean": null,
            "lastUpdatedAt": 1699619535748,
            "passcodeProfileDescription": null,
            "deviceQueryId": null,
            "deviceQueryStatus": null,
            "configurations": null,
            "allowUnregistration": true,
            "businessRuleInfo": null,
            "currentBiosAdminPassword": null,
            "mqttUrl": "tls://sqa2-pns-cms.amds.dell.com:443",
            "secureMqttUrl": "tls://sqa2-pns-cms.amds.dell.com:443",
            "preferredMqttUrl": "tls://sqa2-pns-cms.amds.dell.com:443",
            "wmsUrl": "https://sqa2-cms.amds.dell.com/ccm-web",
            "heartbeatIntervalInMins": 60,
            "checkInIntervalInHours": 8,
            "groupToken": "amds=l6LpK1%",
            "personalDeviceSettings": null,
            "policyGroups": {},
            "licenseType": "Prod",
            "licenseExpiry": 1735669799000,
            "repoInfo": null,
            "hashVersion": null,
            "authenticationCode": null,
            "secureToken": null,
            "policyIds": {
            "31340987191593270468785413242": 1698998320852,
            "31350756471194955797113398544": 1699527913517,
            },
            "dynamicGroups": null,
            "subscriptionStatus": 0,
            "maxCheckinIntervalInHours": 192,
            "wmsVersion": "4.7.5"
        }
        DeviceMQTTData = json.dumps(data, indent=4).encode('utf-8')
        self.wfile.write(DeviceMQTTData)
        self.end_headers()
    else:
        self.send_response(404, 'Not Found: record does not exist')
        self.end_headers()

def PostWMSFullConfig(self):
    print("Device WMS Full config command")

    length = int(self.headers.get('content-length'))
    RecvData = self.rfile.read(length).decode('utf8')
    print(RecvData)
    RecvData = json.loads(RecvData)
    print(RecvData)

    self.send_response(200)
    self.send_header('Content-Type', 'application/json')
    self.end_headers()

    null = "null"
    false = "false"
    true = "true"
    data = {
        "deviceElements": null,
        "deviceElementsV2": null,
        "configSettings": {
            "version": "0.0.1",
            "sequence": 1699601161680,
            "parameters": {
                "pPersonalizationWallpaperMode": {
                    "value": "center"
                },
                "BIOS enableBiosAdminPassword": {
                    "value": "2"
                },
                "BIOS Primary Battery Charge Configuration": {
                    "value": "2"
                },
                "BIOS Peak Shift Battery Threshold": {
                    "value": "65"
                },
                "pPersonalizationDesktopBitmap": {
                    "files": [
                        {
                            "_id": "31104925687402558010766243877",
                            "id": 0,
                            "updatedAt": 1686201400083,
                            "isActive": true,
                            "name": "Ferrari.jpg",
                            "type": "wallpaper",
                            "checksum":"d3d56a4b0d96dfe914efbf648afcbf0266b0217ed794df27e8b6aced20832e1552d39215b70121b33e68f42b69f4d4fc2bfa7c06b7072549386075aa1c3eed64",
                            "size": 374310,
                            "url": "/device/serviceProviderFile/WmU8JywPD!387/global/wallpaper/Ferrari.jpg",
                            "externalGroupId": "global",
                            "repoType": 3,
                            "uploadedByCustomer": false,
                            "tikaContentType": "image/jpeg",
                            "tags": [
                                "image/jpeg"
                            ],
                            "vendors": []
                        }
                    ]
                },
                "BIOS Peak Shift": {
                    "value": "2"
                },
                "BIOS biosAdminPassword": {
                    "value": "kVqUd8z1hyN/AdFW08vGFBhUxban2o2esHHiZuYMMQqVgc+v5RQDJqGEeUpl227BUYqPYvNoQa8Q+ISMVp3Ddw=="
                }
            }
        },
        "dynamicGroupPolicies": null,
        "deviceExceptionPolicies": null,
        "fullConfiguration": false,
        "shouldSendRemoteCommand": false,
        "isJailBroken": false,
        "compliantStatus": 0,
        "configCompliantStatus": 0,
        "passcodeCompliant": true,
        "encryptionCompliantStatus": 1,
        "computeJailbreak": true,
        "isCaValidationOn": true,
        "personInfoLean": null,
        "lastUpdatedAt": 1699601163997,
        "passcodeProfileDescription": null,
        "deviceQueryId": null,
        "deviceQueryStatus": null,
        "configurations": null,
        "allowUnregistration": true,
        "businessRuleInfo": null,
        "currentBiosAdminPassword": null,
        "mqttUrl": "tcp://sqa2-pns-cms.amds.dell.com:1883",
        "secureMqttUrl": null,
        "preferredMqttUrl": null,
        "wmsUrl": "https://sqa2-cms.amds.dell.com/ccm-web",
        "heartbeatIntervalInMins": 0,
        "checkInIntervalInHours": 0,
        "groupToken": null,
        "personalDeviceSettings": null,
        "policyGroups": null,
        "licenseType": null,
        "licenseExpiry": 0,
        "repoInfo": null,
        "hashVersion": null,
        "authenticationCode": null,
        "secureToken": null,
        "policyIds": null,
        "dynamicGroups": null,
        "cmaMaintenanceKey": null,
        "agentExpiredDate": null,
        "subscriptionStatus": 0,
        "intakeFormCompleted": false,
        "maxCheckinIntervalInHours": 0,
        "wmsVersion": "4.7.5"
    }
    DeviceMQTTData = json.dumps(data, indent=4).encode('utf-8')
    self.wfile.write(DeviceMQTTData)
    self.end_headers()

def PostDeviceHeartBeat(self):
    print("Device Device Heartbeat command")

    length = int(self.headers.get('content-length'))
    RecvData = self.rfile.read(length).decode('utf8')
    print(RecvData)
    RecvData = json.loads(RecvData)
    print(RecvData["lastComplianceCheckTime"])

    self.send_response(200)
    self.send_header('Content-Type', 'application/json')
    self.end_headers()


def PostGenericAudit(self):
    print("Device Generic Audit command")

    length = int(self.headers.get('content-length'))
    RecvData = self.rfile.read(length).decode('utf8')
    print(RecvData)
    self.end_headers()


def PostDeviceStatus(self):
    print("Device Device Status command")

    length = int(self.headers.get('content-length'))
    RecvData = self.rfile.read(length).decode('utf8')
    print(RecvData)
    RecvData = json.loads(RecvData)
    print(RecvData["id"])
    print(RecvData["status"])


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

    self.wfile.write(DeviceGetCommandData)
    self.end_headers()

def DeviceGetInProgressCommand(self):
    print("Device get In Progress Command")
    self.send_response(200)
    self.send_header('Content-Type', 'application/json')
    self.end_headers()

    data = []
    data.append("Hello")
    data.append("World")
    print(data)
    DeviceGetCommandData = str(data).encode('utf-8')
    print(DeviceGetCommandData)

    self.wfile.write(DeviceGetCommandData)
    self.end_headers()


class HTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        print("Data is: ", self.path)
        if self.path.split('/')[1] == 'device':
            print("Data is:", self.path.split('/')[1])
            if self.path.split('/')[2] == 'checkin':
                print("input is checkin")
                PostDeviceCheckin(self)
            elif self.path.split('/')[2] == 'wms20' and self.path.split('/')[3] == 'fullConfig':
                print("input is wms20/fullConfig")
                PostWMSFullConfig(self)
            elif self.path.split('/')[2] == 'heartbeat':
                print("input is heartbeat")
                PostDeviceHeartBeat(self)
            elif self.path.split('/')[2] == 'genericAudit':
                print("input is genericAudit")
                PostGenericAudit(self)
            elif self.path.split('/')[2] == 'status':
                print("input is status")
                PostDeviceStatus(self)
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
                OpenDeviceGroupLoginPostDetails(self)
            elif self.path.split('/')[2] == 'deviceRegister':
                print("input is deviceRegister")
                OpenDeviceRegisterPostDetails(self)
            else:
                self.send_response(404, 'Not Found: record does not exist')
        else:
            self.send_response(403)

    def do_GET(self):
        print("Data is: ", self.path)
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
                DeviceGetInProgressCommand(self)
            else:
                self.send_response(404, 'Not Found: record does not exist')
        else:
            self.send_response(403)
        self.end_headers()

if __name__ == '__main__':
    #ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ##ctx.load_cert_chain(certfile='server.crt', keyfile='server.key')
    #ctx.load_cert_chain("../mqtt_broker/certs/mqtt-server.crt", "../mqtt_broker/certs/mqtt-server.key")
    #server = HTTPServer(('192.168.60.109', 443), HTTPRequestHandler)
    #server.socket = ctx.wrap_socket(server.socket, server_side=True)

    context = None
    if(HTTPS_ENABLED):
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        
        if(VERIFY_USER):
            ctx.verify_mode = ssl.CERT_REQUIRED
            ctx.load_verify_locations("../mqtt_broker/certs/mosquitto-certificate-authority.crt")

        try:
            ctx.load_cert_chain("../mqtt_broker/certs/mqtt-server.crt", "../mqtt_broker/certs/mqtt-server.key")
        except Exception as e:
            sys.exit("Error starting server: {}".format(e))
    
    server = HTTPServer(('192.168.60.109', 443), HTTPRequestHandler)
    server.socket = ctx.wrap_socket(server.socket, server_side=True)

    logging.info('Starting httpd...\n')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()
    logging.info('Stopping httpd...\n')

