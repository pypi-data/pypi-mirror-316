"""
TokenHandler class for processing SAML callbacks.

This module implements a custom HTTP request handler for processing
SAML callbacks. It listens for authorization codes in the callback
requests and responds with an HTML template indicating success.
"""

import os
from http.server import SimpleHTTPRequestHandler


class TokenHandler(SimpleHTTPRequestHandler):
    """Custom HTTP request handler to process the SAML callback."""

    def do_GET(self):
        """Handle GET request to capture the auth code."""
        if "/callback?" in self.path:
            query_data = self.path.split("?")[1]
            token_info = dict(qc.split("=") for qc in query_data.split("&"))
            auth_code = token_info.get("code")

            if auth_code:
                # Send a response back to the browser indicating success
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()

                file_path = os.path.join(os.path.dirname(__file__), "template/callback.html")
                with open(file_path, "rb") as file:
                    html_content = file.read()

                self.wfile.write(html_content)
                self.server.auth_code = auth_code
            else:
                self.send_error(400, "Authorization code not found")
