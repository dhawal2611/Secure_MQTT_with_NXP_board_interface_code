import json
import logging
import re
import ssl
from http.server import BaseHTTPRequestHandler, HTTPServer


class LocalData(object):
    records = {}

class HTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if re.search('/api/post/*', self.path):
            length = int(self.headers.get('content-length'))
            data = self.rfile.read(length).decode('utf8')

            record_id = self.path.split('/')[-1]
            LocalData.records[record_id] = data

            logging.info("add record %s: %s", record_id, data)
            self.send_response(200)
        else:
            self.send_response(403)
        self.end_headers()

    def do_GET(self):
        if re.search('/api/get/*', self.path):
            record_id = self.path.split('/')[-1]
            if record_id in LocalData.records:
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()

                # Return json, even though it came in as POST URL params
                data = json.dumps(LocalData.records[record_id]).encode('utf-8')
                logging.info("get record %s: %s", record_id, data)
                self.wfile.write(data)

            else:
                self.send_response(404, 'Not Found: record does not exist')
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

