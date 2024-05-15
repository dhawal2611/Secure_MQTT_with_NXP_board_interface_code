import json
import logging
import re
import ssl
from http.server import BaseHTTPRequestHandler, HTTPServer


class LocalData(object):
    records = {}

class HTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
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
        self.end_headers()

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
            elif self.path.split('/')[2] == 'getKey':
                print("input is getKey")
            elif re.search('getCommand', self.path):
                print("input is getCommand?wyseId=<wyseid>", self.path)
                print("Key: ", self.path.split('/')[2].split('?')[1].split('=')[0])
                print("Value: ", self.path.split('/')[2].split('?')[1].split('=')[1])
                print("Value: ", self.path.split('=')[1])
                print("Key: ", self.path.split('=')[0].split('?')[-1])
                print("Key: ", re.search(r"(?<=\?).+?(?=\=)", self.path).group())
            elif self.path.split('/')[2] == 'getInProgressCommand':
                print("input is getInProgressCommand")
            else:
                self.send_response(404, 'Not Found: record does not exist')
            
            
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            LocalData.records[0] = "Hello"
            # Return json, even though it came in as POST URL params
            data = json.dumps(LocalData.records[0]).encode('utf-8')
            logging.info("get record %d: %s", 0, data)
            self.wfile.write(data)
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

