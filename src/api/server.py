from flask import Flask, jsonify
from threading import Thread
from src.config.api import APIConfig

class APIServer:
    def __init__(self):
        self.app = Flask(__name__)
        self.setup_routes()
        self.server_thread = None

    def setup_routes(self):
        @self.app.route('/health', methods=['GET'])
        def health_check():
            return jsonify({"status": "running"})

    def start(self):
        """Start the Flask server in a separate thread"""
        if APIConfig.SERVER_ENABLED:
            self.server_thread = Thread(target=self._run_server)
            self.server_thread.daemon = True  # Thread will be terminated when main program exits
            self.server_thread.start()
            print(f"API Server started on http://{APIConfig.HOST}:{APIConfig.PORT}")

    def _run_server(self):
        """Run the Flask server"""
        self.app.run(
            host=APIConfig.HOST,
            port=APIConfig.PORT,
            debug=APIConfig.DEBUG
        )

    def stop(self):
        """Stop the Flask server"""
        if self.server_thread and self.server_thread.is_alive():
            # Implement shutdown logic if needed
            pass