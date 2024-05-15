from flask import Flask,jsonify,request
import ssl

app = Flask(__name__)

@app.route('/')
def index():
    # Create a sample dictionary containing JSON data
    data = {
        "string": "Hello, World! This is an HTTPS Flask server."
    }
    return jsonify(data)

@app.route('/post_data', methods=['POST'])
def post_data():
    # Check if the request contains JSON data
    if request.is_json:
        # Access the JSON data from the request body
        data = request.json
        print(data)
        # Process the JSON data (e.g., validate, save to database, etc.)
        resp = {"response": "Valid API"}
        
        # Here, we'll simply echo back the received JSON data
        return jsonify(resp)
    else:
        # If the request does not contain JSON data, return an error response
        print(request.data)
        return jsonify({"error": "Request must contain JSON data"}), 400




if __name__ == '__main__':
    sslctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    sslctx.load_cert_chain("../mqtt_broker/certs/mqtt-server.crt", "../mqtt_broker/certs/mqtt-server.key")
    app.run(host="0.0.0.0", ssl_context=sslctx,port=443, debug=True)
    #app.run(host="0.0.0.0",port=80, debug=True)