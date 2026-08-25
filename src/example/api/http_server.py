#!/usr/bin/env python3
"""HTTP server wrapper for MCP stdio server."""

import json
import subprocess
import os
from http.server import HTTPServer, BaseHTTPRequestHandler


class MCPHandler(BaseHTTPRequestHandler):
    """HTTP handler that forwards requests to MCP server via stdio."""

    def do_POST(self):
        """Handle POST requests to MCP."""
        if self.path != "/mcp":
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'{"error": "Not found"}')
            return

        # Read request body
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8")

        try:
            # Send to MCP server via stdin
            process = subprocess.Popen(
                ["python", "-m", "src.example.mcp.server"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            stdout, stderr = process.communicate(input=body, timeout=5)

            # Send response
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(stdout.encode("utf-8"))

        except subprocess.TimeoutExpired:
            self.send_response(504)
            self.end_headers()
            self.wfile.write(b'{"error": "Gateway Timeout"}')
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

    def do_GET(self):
        """Handle GET requests for health check."""
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status": "ok", "service": "mcp-server"}')
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'{"error": "Not found"}')

    def log_message(self, format, *args):
        """Suppress default logging."""
        pass


def run_server():
    """Start the HTTP server."""
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), MCPHandler)
    print(f"HTTP MCP Server running on port {port}")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
