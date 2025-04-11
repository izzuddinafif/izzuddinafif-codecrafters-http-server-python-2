import socket
import logging
import threading

NOTFOUND = b'HTTP/1.1 404 Not Found\r\n\r\n'

def main():
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    port = 4221
    with socket.create_server(('localhost', port), reuse_port=True) as server:
        logging.info(f"Afif's HTTP server started at {port}")
        while True:
            conn, addr = server.accept()
            t = threading.Thread(target=handle_client, args=(conn, addr))
            t.start()
            
def handle_client(conn, addr):
    with conn:
        logging.info(f'connected by {addr[0]} from port {addr[1]}')
        while True:
            bytes_data = conn.recv(1024)
            data = str(bytes_data, 'utf-8')
            if not data:
                break
            lines = data.splitlines()
            method, path, version = lines[0].split(' ')
            user_agent_lines = [ua for ua in lines if ua.startswith("User-Agent:")]
            user_agent = user_agent_lines[0].split(' ', 1)[1] if user_agent_lines else "Unknown"
            handle_request(conn, path, user_agent)

def build_response(body, status, content_type):
    body_bytes = body.encode()
    resp = [
        f'HTTP/1.1 {status}',
    ]
    
    if status.startswith('200'):
        if body:
            resp.extend([f'Content-Type: {content_type}', f'Content-Length: {len(body_bytes)}', ''])
        else:
            resp.append('')
    
    return '\r\n'.join(resp).encode() + b'\r\n' + body_bytes

def handle_request(conn, path, user_agent):
    p = path.split('/') 
    if p[1] == '':
        resp = build_response('', '200 OK', '')
        logging.info(resp)
        conn.sendall(resp)
    elif p[1] == 'echo' and len(p) > 2:
        resp = build_response(p[2], '200 OK', 'text/plain')
        logging.info(resp)
        conn.sendall(resp)
    elif p[1] == 'user-agent':
        resp = build_response(user_agent, '200 OK', 'text/plain')
        logging.info(resp)
        conn.sendall(resp)
    else:
        logging.info(NOTFOUND)
        conn.sendall(NOTFOUND)
        
if __name__ == '__main__':
    main()
