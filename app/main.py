import socket

# HTTP Respond Messages
NOTFOUND = b'HTTP/1.1 404 Not Found\r\n\r\n'

def main():
    port = 4221
    with socket.create_server(('localhost', port), reuse_port=True) as server:
        print(f"Afif's HTTP server started at {port}")
        while True:
            conn, addr = server.accept()
            with conn:
                print(f'connected by {addr[0]} from port {addr[1]}')
                while True:
                    bytes_data = conn.recv(1024)
                    data = str(bytes_data, 'utf-8')
                    if not data:
                        break
                    lines = data.splitlines()
                    method, path, version = lines[0].split(' ')
                    host, user_agent = lines[3].split(' ')
                    handle_request(conn, path, user_agent)

def build_response(body, status, content_type):
    body_bytes = body.encode()
    resp = [
        f'HTTP/1.1 {status}',
    ]
    
    if status.startswith('200'):
        if body:
            resp.extend([f'Content-Type: {content_type}', f'Content-Length: {len(body_bytes)}', ''])
    
    return '\r\n'.join(resp).encode() + b'\r\n' + body_bytes

def handle_request(conn, path, user_agent):
    p = path.split('/') 
    if p[1] == '':
        print(build_response('', '200 OK', ''))
        conn.sendall(build_response('', '200 OK', ''))
    elif p[1] == 'echo' and len(p) > 2:
        print(build_response(p[2], '200 OK', 'text/plain'))
        conn.sendall(build_response(p[2], '200 OK', 'text/plain'))
    elif p[1] == 'user-agent':
        conn.sendall(build_response(user_agent, '200 OK', 'text/plain'))
    else:
        conn.sendall(NOTFOUND)
        
if __name__ == '__main__':
    main()
