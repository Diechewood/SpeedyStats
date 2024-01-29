# Utilities/ErrorHandling.py
import logging
from flask import jsonify

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

class AppError(Exception):
    """ Custom application error class. """
    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

def handle_error(error):
    """ Handler for AppError. """
    logger.error(f"AppError: {error.message}")
    response = {'error': error.message}
    return jsonify(response), error.status_code

def handle_generic_error(error):
    """ Generic error handler for unexpected errors. """
    logger.error(f"Unexpected Error: {error}", exc_info=True)
    response = {'error': 'An unexpected error occurred'}
    return jsonify(response), 500

def handle_database_error(error):
    """ Handler for database-related errors. """
    logger.error(f"Database Error: {error}", exc_info=True)
    response = {'error': 'Database operation failed'}
    return jsonify(response), 500

def handle_gps_data_error(error):
    """ Handler for errors related to GPS data processing. """
    logger.error(f"GPS Data Error: {error}", exc_info=True)
    response = {'error': 'GPS data processing error'}
    return jsonify(response), 400

# Additional specific error handlers can be added here
