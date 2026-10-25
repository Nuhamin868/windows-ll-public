"""Serve inert test fixtures on a controlled TLS host; no trust settings changed."""
import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import socket
import ssl
import threading
import time

DATA = Path(__file__).resolve().parents[1] / 'test_data'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cert', required=True)
    parser.add_argument('--key', required=True)
    parser.add_argument('--bind', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=443)
    parser.add_argument('--request-log', required=True)
    args = parser.parse_args()
    lock = threading.Lock()
    log = Path(args.request_log)
    # A fresh log is required to avoid mixing separate validation sessions.
    with log.open('x'):
        pass

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_):
            pass

        def do_GET(self):
            with lock, log.open('a') as output:
                output.write(json.dumps({'time': time.time(), 'path': self.path}) + '\n')
            route = self.path
            status = {'/404': 404, '/500': 500, '/redirect': 302, '/redirect301': 301, '/redirect-other': 302}.get(route, 200)
            body = {
                '/valid': (DATA / 'artifact.bin').read_bytes(),
                '/bad-tag': (DATA / 'bad-tag.bin').read_bytes(),
                '/bad-schema': (DATA / 'bad-schema.bin').read_bytes(),
                '/truncated': (DATA / 'truncated-artifact.bin').read_bytes(),
                '/empty': b'',
            }.get(route, b'fixture')
            if route.startswith('/oversize'):
                body = b'A' * (1024 * 1024 + 1)
            if route == '/timeout':
                time.sleep(8)
            try:
                self.send_response(status)
                if route in ['/redirect', '/redirect301', '/redirect-other']:
                    target = 'https://example.invalid/redirect-target' if route == '/redirect-other' else '/redirect-target'
                    self.send_header('Location', target)
                if route not in ['/oversize-no-length', '/disconnect', '/slow-drip']:
                    self.send_header('Content-Length', str(len(body)))
                if route == '/disconnect':
                    self.send_header('Content-Length', '1000')
                self.send_header('Connection', 'close')
                self.end_headers()
                if route == '/disconnect':
                    self.wfile.write(b'WLL1')
                    self.wfile.flush()
                    self.connection.shutdown(socket.SHUT_RDWR)
                elif route == '/slow-drip':
                    for _ in range(40):
                        self.wfile.write(b'A')
                        self.wfile.flush()
                        time.sleep(1)
                else:
                    self.wfile.write(body)
            except (BrokenPipeError, ConnectionError, ssl.SSLError):
                pass  # Clients deliberately reject oversized/slow responses.

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(args.cert, args.key)
    server = ThreadingHTTPServer((args.bind, args.port), Handler)
    server.daemon_threads = True
    server.socket = context.wrap_socket(server.socket, server_side=True)
    print(f'TLS fixture server listening on {args.bind}:{args.port}', flush=True)
    server.serve_forever()


if __name__ == '__main__':
    main()
