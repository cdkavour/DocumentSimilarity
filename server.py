from http.server import HTTPServer, BaseHTTPRequestHandler
from doc_sim_score import calculate_similarity


PORT = 8008
WE_TYPE = 'context-counts'
WINDOW = 2

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def _set_response(self, code=200):
        self.send_response(code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_response()
        self.wfile.write('Hello! This is the document similarity comparison App.\n\n'.encode())

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length).decode('utf-8') # <--- Gets the data itself
        print("POST BODY:\n{}".format(post_data))

        # Expect documents to be newline seperated
        try:
            docstr_A, docstr_B = post_data.split('\n', 1)
        except Exception:
             self._set_response(code=400)
             self.wfile.write("Failed to process request, make sure payload string is newline seperated between documents \n\n".encode('utf-8'))

        similarity = calculate_similarity(docstr_A, docstr_B, word_embedding_type=WE_TYPE, window=WINDOW)
        self._set_response()
        self.wfile.write("Document 1:\n{}\n\nDocument 2:\n{}\n\nDocument Similarity:\n{}\n\n".format(docstr_A, docstr_B, similarity).encode('utf-8'))


def main():
    server = HTTPServer(('', PORT), SimpleHTTPRequestHandler)
    print("Server running on port {}.\n".format(PORT))
    server.serve_forever()

if __name__ == '__main__':
    main()