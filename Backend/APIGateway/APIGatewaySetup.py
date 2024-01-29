# APIGateway/APIGatewaySetup.py
from flask import Flask, request, jsonify
import requests
import logging
from werkzeug.exceptions import HTTPException

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

class AppError(Exception):
    """ Custom application error class. """
    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

# Error handling functions
def handle_error(error):
    logger.error(f"AppError: {error.message}")
    response = {'error': error.message}
    return jsonify(response), error.status_code

def handle_generic_error(error):
    logger.error(f"Unexpected Error: {error}", exc_info=True)
    response = {'error': 'An unexpected error occurred'}
    return jsonify(response), 500

# Define additional specific error handlers as needed

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
        
        response.raise_for_status()
        return jsonify(response.json()), response.status_code
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP Error: {http_err}", exc_info=True)
        return jsonify({'error': 'Microservice error', 'details': str(http_err)}), 500
    except requests.exceptions.RequestException as err:
        logger.error(f"Request Error: {err}", exc_info=True)
        return jsonify({'error': 'Network error', 'details': str(err)}), 500
    except Exception as err:
        logger.error(f"General Error: {err}", exc_info=True)
        return jsonify({'error': 'An error occurred', 'details': str(err)}), 500

# Register error handlers
app.register_error_handler(AppError, handle_error)
app.register_error_handler(HTTPException, handle_generic_error)

if __name__ == '__main__':
    app.run(port=8080, debug=True)

