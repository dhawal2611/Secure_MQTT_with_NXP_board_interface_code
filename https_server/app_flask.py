from flask import Flask
import ssl

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World! This is an HTTPS Flask server."




if __name__ == '__main__':
    sslctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    sslctx.load_cert_chain("../mqtt_broker/certs/mqtt-server.crt", "../mqtt_broker/certs/mqtt-server.key")
    app.run(host="0.0.0.0", ssl_context=sslctx,port=443, debug=True)