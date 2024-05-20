from flask import Flask,jsonify,request
import ssl
import sys
import pprint

HTTPS_ENABLED = True
VERIFY_USER = True

API_HOST = "0.0.0.0"
API_PORT = 443
API_CRT = "../mqtt_broker/certs/mqtt-server.crt"
API_KEY = "../mqtt_broker/certs/mqtt-server.key"
API_CA_T = "../mqtt_broker/certs/mosquitto-certificate-authority.crt"

context = None
if(HTTPS_ENABLED):
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    
    if(VERIFY_USER):
        context.verify_mode = ssl.CERT_REQUIRED
        context.load_verify_locations(API_CA_T)

    try:
        context.load_cert_chain(API_CRT, API_KEY)
    except Exception as e:
        sys.exit("Error starting server: {}".format(e))


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
    print(request.data)
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
    
    
@app.route('/device/mqtt')
def device_mqtt():
    print(request.headers)
    print(request.data)
    data = {
    "secureMqttUrl": "tls://sample:8443",
    "preferredMqttUrl": "tcp://sample:1883",
    "mqttUrl": "tcp://sample:1883"
    }
    return jsonify(data)

@app.route('/device/getKey')
def device_getKey():
    print(request.headers)
    print(request.data)
    data = "+HMHiWrt2QYULCj+VnQ0vb4UgxI1TtTqB9Xa+0bCZRE="
    return data

@app.route('/device/checkin', methods=['POST'])
def device_checkin():
    print(request.data)
    # Check if the request contains JSON data
    if request.is_json:
        # Access the JSON data from the request body
        data = request.json
        print(data)
        # Process the JSON data (e.g., validate, save to database, etc.)
        resp = {
        "deviceElements": 0,
        "deviceElementsV2": 0,
        "configSettings": 0,
        "dynamicGroupPolicies": 0,
        "deviceExceptionPolicies": 0,
        "fullConfiguration": False,
        "shouldSendRemoteCommand": False,
        "isJailBroken": False,
        "compliantStatus": 1,
        "configCompliantStatus": 0,
        "passcodeCompliant": True,
        "encryptionCompliantStatus": 1,
        "computeJailbreak": True,
        "isCaValidationOn": True,
        "personInfoLean": 0,
        "lastUpdatedAt": 1699619535748,
        "passcodeProfileDescription": 0,
        "deviceQueryId": 0,
        "deviceQueryStatus": 0,
        "configurations": 0,
        "allowUnregistration": True,
        "businessRuleInfo": 0,
        "currentBiosAdminPassword": 0,
        "mqttUrl": "tls://sqa2-pns-cms.amds.dell.com:443",
        "secureMqttUrl": "tls://sqa2-pns-cms.amds.dell.com:443",
        "preferredMqttUrl": "tls://sqa2-pns-cms.amds.dell.com:443",
        "wmsUrl": "https://sqa2-cms.amds.dell.com/ccm-web",
        "heartbeatIntervalInMins": 60,
        "checkInIntervalInHours": 8,
        "groupToken": "amds=l6LpK1%",
        # "personalDeviceSettings": 0,
        # "policyGroups": {},
        # "licenseType": "Prod",
        # "licenseExpiry": 1735669799000,
        # "repoInfo": 0,
        # "hashVersion": 0,
        # "authenticationCode": 0,
        # "secureToken": 0,
        # "policyIds": {
        #     "31340987191593270468785413242": 1698998320852,
        #     "31350756471194955797113398544": 1699527913517,
        # },
        # "dynamicGroups": 0,
        # "subscriptionStatus": 0,
        # "maxCheckinIntervalInHours": 192,
        # "wmsVersion": "4.7.5"
        }
        
        # Here, we'll simply echo back the received JSON data
        return jsonify(resp)
    else:
        # If the request does not contain JSON data, return an error response
        print(request.data)
        return jsonify({"error": "Request must contain JSON data"}), 400

class LoggingMiddleware(object):
    def __init__(self, app):
        self._app = app

    def __call__(self, env, resp):
        errorlog = env['wsgi.errors']
        pprint.pprint(('REQUEST', env), stream=errorlog)

        def log_response(status, headers, *args):
            pprint.pprint(('RESPONSE', status, headers), stream=errorlog)
            return resp(status, headers, *args)

        return self._app(env, log_response)


if __name__ == '__main__':
    sslctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    sslctx.load_cert_chain("../mqtt_broker/certs/mqtt-server.crt", "../mqtt_broker/certs/mqtt-server.key")
    #app.run(host="0.0.0.0", ssl_context=sslctx,port=443, debug=True)
    #app.run(host="0.0.0.0",port=80, debug=True)
    #app.wsgi_app = LoggingMiddleware(app.wsgi_app)
    app.run(ssl_context=context, host=API_HOST, port=API_PORT, debug=True)