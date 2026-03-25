import http.server
import socketserver
import json
import os

PORT = 8003
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class SorryHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Serve files from the same directory as this script
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_POST(self):
        if self.path == '/forgive':
            content_length = int(self.headers.get('Content-Length', 0))
            her_message = ""
            if content_length > 0:
                post_data = self.rfile.read(content_length)
                try:
                    data = json.loads(post_data.decode('utf-8'))
                    her_message = data.get('message', '')
                except Exception:
                    pass
                
            print("\n" + "="*50, flush=True)
            print("*** SHE SAID YES! FORGIVENESS SECURED! ***", flush=True)
            if her_message:
                print("\n*** SHE SENT YOU A MESSAGE: ***", flush=True)
                try:
                    print(f"   \"{her_message}\"", flush=True)
                except UnicodeEncodeError:
                    print("   [Message contains emojis - Check she_said_yes.txt!]", flush=True)
                print("\n" + "="*50 + "\n", flush=True)
            else:
                print("="*50 + "\n", flush=True)
            
            # Save the response to a text file
            with open(os.path.join(DIRECTORY, "she_said_yes.txt"), "w", encoding="utf-8") as f:
                f.write("She forgave you! 🎉\n")
                if her_message:
                    f.write(f"\nHer Message to you:\n\"{her_message}\"")
                f.flush()

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'success', 'message': 'Yay! Thank you for forgiving me!'}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), SorryHandler) as httpd:
        print(f"Server is running at http://localhost:{PORT}")
        print("Share this link with her and wait for the magic to happen...")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")
