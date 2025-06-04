class APIConfig:
    """Configuration for the Flask API server"""
    SERVER_ENABLED = False  # Set to True to enable API server
    HOST = '0.0.0.0'  # Listen on all network interfaces
    PORT = 5000
    DEBUG = False