# APIGateway/APIGatewaySetup.py
from flask import Flask, request, jsonify, redirect
import requests
from Utilities.ErrorHandling import AppError, handle_error

app = Flask(__name__)

# Define URLs for microservices
USER_AUTH_SERVICE_URL = 'http://user-auth-service/'
SPEED_DATA_SERVICE_URL = 'http://speed-data-service/'
DATA_PROCESSING_SERVICE_URL = 'http://data-processing-service/'

@app.route('/auth/<action>', methods=['POST', 'GET'])
def user_auth(action):
    service_url = USER_AUTH_SERVICE_URL + action
    return proxy_request(service_url)

@app.route('/speeddata/<action>', methods=['POST', 'GET'])
def speed_data(action):
    service_url = SPEED_DATA_SERVICE_URL + action
    return proxy_request(service_url)

@app.route('/dataprocessing/<action>', methods=['POST', 'GET'])
def data_processing(action):
    service_url = DATA_PROCESSING_SERVICE_URL + action
    return proxy_request(service_url)

def proxy_request(service_url):
    try:
        if request.method == 'POST':
            response = requests.post(service_url, json=request.json)
        else:
            response = requests.get(service_url)
        
        # Check if the response from microservice is successful
        response.raise_for_status()
        return jsonify(response.json()), response.status_code
    except requests.exceptions.HTTPError as http_err:
        # Handle HTTP errors from microservices
        return jsonify({'error': 'Microservice error', 'details': str(http_err)}), 500
    except requests.exceptions.RequestException as err:
        # Handle other requests errors
        return jsonify({'error': 'Network error', 'details': str(err)}), 500

app.register_error_handler(AppError, handle_error)

if __name__ == '__main__':
    app.run(port=8080, debug=True)
