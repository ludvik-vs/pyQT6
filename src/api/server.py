from flask import Flask, jsonify, request
from threading import Thread
from src.config.api import APIConfig
from waitress import serve
import socket
import requests
import time

class APIServer:
    def __init__(self):
        self.app = Flask(__name__)
        self.setup_routes()
        self.setup_error_handlers()
        self.server_thread = None
        self.is_running = False

    def get_local_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except Exception as e:
            print(f"Error obtaining local IP: {e}")
            return "127.0.0.1"

    def check_server_accessibility(self):
        local_ip = self.get_local_ip()
        urls = [
            f"http://localhost:{APIConfig.PORT}/health",
            f"http://{local_ip}:{APIConfig.PORT}/health"
        ]

        for url in urls:
            try:
                response = requests.get(url, timeout=2)
                if response.status_code == 200:
                    print(f"Server accessible at: {url}")
                    self.is_running = True
                    return True
            except requests.RequestException as e:
                print(f"Server not accessible at: {url}, error: {e}")

        self.is_running = False
        return False

    def start(self):
        """Start the Flask server in a separate thread"""
        if APIConfig.SERVER_ENABLED:
            local_ip = self.get_local_ip()
            self.server_thread = Thread(target=self._run_server)
            self.server_thread.daemon = True
            self.server_thread.start()

            # Wait for server to start and verify accessibility
            time.sleep(2)  # Give server time to start
            if self.check_server_accessibility():
                print(f"API Server running and accessible at:")
                print(f"- Local: http://localhost:{APIConfig.PORT}")
                print(f"- Network: http://{local_ip}:{APIConfig.PORT}")
            else:
                print("Warning: Server may not be accessible on the network")

    def _run_server(self):
        """Run the Flask server"""
        if APIConfig.DEBUG:
            self.app.run(
                host=APIConfig.HOST,
                port=APIConfig.PORT,
                debug=APIConfig.DEBUG,
                use_reloader=False
            )
        else:
            serve(
                self.app,
                host=APIConfig.HOST,
                port=APIConfig.PORT,
                threads=4
            )

    def setup_routes(self):
        @self.app.route('/', methods=['GET'])
        def root():
            return jsonify({
                "message": "ACRIL CAR API Server",
                "version": "1.0",
                "status": "running"
            })

        @self.app.route('/health', methods=['GET'])
        def health_check():
            return jsonify({"status": "running"})

        @self.app.route('/api', methods=['GET'])
        def api_info():
            return jsonify({
                "available_endpoints": [
                    "/",
                    "/health",
                    "/api"
                ]
            })

    def setup_error_handlers(self):
        @self.app.errorhandler(404)
        def not_found(error):
            return jsonify({
                "error": "Not Found",
                "message": "The requested endpoint does not exist.",
                "available_endpoints": [
                    "/",
                    "/health",
                    "/api"
                ]
            }), 404

        @self.app.errorhandler(500)
        def server_error(error):
            return jsonify({
                "error": "Internal Server Error",
                "message": "An unexpected error occurred."
            }), 500

    def stop(self):
        """Stop the Flask server"""
        # Implement shutdown logic if needed
        pass

# To start the server
if __name__ == "__main__":
    server = APIServer()
    server.start()