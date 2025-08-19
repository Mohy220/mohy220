#!/usr/bin/env python3
"""
Simple HTTP server for serving static files.
Uses Python's built-in http.server module instead of custom implementation.
"""

import http.server
import socketserver
import os
import urllib.parse

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Extended SimpleHTTPRequestHandler with custom routes"""
    
    def do_GET(self):
        # Handle root path - serve Index.html
        if self.path == "/":
            self.path = "/Index.html"
        
        # Handle legacy CSS path
        elif self.path == "/Untitled-2":
            self.path = "/Untitled-2.css"
        
        # Handle contact form submission (for compatibility)
        elif self.path.startswith("/submit"):
            self.handle_contact_form()
            return
        
        # Use the default handler for all other requests
        return super().do_GET()
    
    def handle_contact_form(self):
        """Handle contact form submissions"""
        parsed_path = urllib.parse.urlparse(self.path)
        parsed_query = urllib.parse.parse_qs(parsed_path.query)
        
        name = parsed_query.get("name", ["Anonymous"])[0]
        message = parsed_query.get("message", ["No message provided"])[0]
        
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
        response_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contact Form Submitted</title>
    <link rel="stylesheet" href="Untitled-2.css">
</head>
<body>
    <div style="max-width: 800px; margin: 2rem auto; padding: 2rem; text-align: center;">
        <h1>Thank You, {name}!</h1>
        <p>Your message has been received:</p>
        <blockquote style="background-color: #333; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
            "{message}"
        </blockquote>
        <p>We will get back to you shortly!</p>
        <a href="/" style="color: #00bfae; text-decoration: none;">Go back to home</a>
    </div>
</body>
</html>"""
        
        self.wfile.write(bytes(response_html, "utf-8"))

def run_server(port=8080):
    """Run the HTTP server"""
    try:
        with socketserver.TCPServer(("", port), CustomHTTPRequestHandler) as httpd:
            print(f"Server running at http://localhost:{port}/")
            print("Press Ctrl+C to stop the server")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    except OSError as e:
        print(f"Error starting server: {e}")

if __name__ == "__main__":
    run_server()
