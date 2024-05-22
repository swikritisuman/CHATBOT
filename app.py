# app.py
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import wikipedia

class ChatbotHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        message = json.loads(post_data.decode('utf-8'))['message']
        
        print(f"Received message: {message}")

        response_message = self.get_response(message)
        response = {'response': response_message}
        self._set_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def get_response(self, message):
        print(f"Processing message: {message}")
        
        # Check if it's a greeting
        if any(greeting in message.lower() for greeting in ['hello', 'hi', 'hey']):
            return "Hello! How can I assist you today?"
        
        # Check if it's a mathematical operation
        if any(op in message for op in ['+', '-', '*', '/']):
            try:
                result = eval(message)
                print(f"Result of calculation: {result}")
                return f"The result is {result}"
            except Exception as e:
                print(f"Error evaluating mathematical expression: {e}")
                return "There was an error processing the mathematical expression."

        # Check if it's a question
        if '?' in message:
            try:
                # Get the Wikipedia summary for the question
                query = message.replace('?', '')
                summary = wikipedia.summary(query, sentences=2)
                return summary
            except wikipedia.exceptions.DisambiguationError as e:
                return "Can you please clarify your question?"
            except wikipedia.exceptions.PageError as e:
                return "I couldn't find information on that topic. Please try again."
            except wikipedia.exceptions.WikipediaException as e:
                return "An error occurred while processing your request. Please try again later."

        return "I'm not sure how to respond to that."

def run(server_class=HTTPServer, handler_class=ChatbotHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
