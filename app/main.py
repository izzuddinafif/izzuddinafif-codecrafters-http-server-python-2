import socket

# HTTP Respond Messages
OK = b"HTTP/1.1 200 OK\r\n\r\n"
NOTFOUND = b"HTTP/1.1 404 Not Found\r\n\r\n"

def build_response(body, status="200 OK", content_type="text/plain"):
    body_bytes = body.encode()
    resp = [
        f"HTTP/1.1 {status}",
        f"Content-Type: {content_type}",
        f"Content-Length: {len(body_bytes)}",
        "",
        "",
    ]
    
    return "\r\n".join(resp).encode() + body_bytes

def main():
    port = 4221
    with socket.create_server(("localhost", port), reuse_port=True) as server:
        print(f"Afif's HTTP server started at {port}")
        while True:
            conn, addr = server.accept()
            with conn:
                print(f"connected by {addr[0]} from port {addr[1]}")
                while True:
                    bytes_data = conn.recv(1024)
                    data = str(bytes_data, 'utf-8')
                    if not data:
                        break
                    request_line = data.splitlines()[0]
                    method, path, version = request_line.split(' ')
                    handlePath(conn, path)

def handlePath(conn, path):
    p = path.split('/')
    if p[1] == '':
        conn.sendall(OK)
    if p[1] == 'echo' and len(p) > 2:
        conn.sendall(build_response(p[2], "200 OK", "text/plain"))
    else:
        conn.sendall(NOTFOUND)      
        
if __name__ == "__main__":
    main()
