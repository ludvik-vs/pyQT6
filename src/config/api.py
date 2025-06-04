class APIConfig:
    """Configuration for the Flask API server"""
    SERVER_ENABLED = True  # Set to True to enable API server
    HOST = '0.0.0.0'  # Listen on all network interfaces
    PORT = 8000
    DEBUG = False  # Activate debug mode temporarily