import socket
import logging
import threading
import argparse
import pathlib

BADREQ = '400 Bad Request'
NOTFOUND = '404 Not Found'
OK = '200 OK'
CREATED = '201 Created'
enc_flag = False

parser = argparse.ArgumentParser(description="Afif's simple HTTP server.")
parser.add_argument('--directory', type=str, help="Path where the HTTP server operates.", default="/tmp")
dir_path = pathlib.Path(parser.parse_args().directory)
if not dir_path.exists():
    print("The directory doesn't exist")
    raise SystemExit(1)

def main():
    format = "%(asctime)s %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    port = 4221
    with socket.create_server(('localhost', port), reuse_port=True) as server:
        logging.info(f"Afif's simple HTTP server started at port: {port}, and at directory: {dir_path}")
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
            print(lines)
            
            user_agent_lines = [ua for ua in lines if ua.startswith("User-Agent:")]
            user_agent = user_agent_lines[0].split(' ', 1)[1] if user_agent_lines else "Unknown"
            
            encoding = [ae for ae in lines if ae.startswith("Accept-Encoding:")]
            enc_list = encoding[0].removeprefix("Accept-Encoding: ").split(', ') if encoding else None
            print(enc_list)
            enc = 'gzip' if enc_list and 'gzip' in enc_list else None
            
            global enc_flag
            if enc == 'gzip':
                enc_flag = True
            else:
                enc_flag = False
                
            request_body = lines[-1] if lines[-2] == '' else ''
            handle_request(conn, path, user_agent, method, request_body)

def build_response(body, status, content_type):
    body_bytes = body.encode()
    resp = [
        f'HTTP/1.1 {status}',
    ]
    
    if status.startswith(OK):
        if body:
            resp.extend([f'Content-Type: {content_type}', f'Content-Length: {len(body_bytes)}'])
    if enc_flag:
        resp.append('Content-Encoding: gzip')
    resp.append('')
    
    # add CRLF before response body to terminate the headers section
    return '\r\n'.join(resp).encode() + b'\r\n' + body_bytes

def handle_request(conn, path, user_agent, method, req_body):
    p = path.split('/') 
    if method == 'GET':
        if p[1] == '':
            resp = build_response('', OK, '')
            logging.info(resp)
            conn.sendall(resp)
        elif p[1] == 'echo' and len(p) > 2:
            resp = build_response(p[2],  OK, 'text/plain')
            logging.info(resp)
            conn.sendall(resp)
        elif p[1] == 'user-agent':
            resp = build_response(user_agent, OK, 'text/plain')
            logging.info(resp)
            conn.sendall(resp)
        elif p[1] == 'files' and len(p) > 2:
            file_path = dir_path.joinpath(p[2])
            if file_path.exists():
                with open(file_path, "r") as f:
                    content = f.read().rstrip('\n')
                resp = build_response(content, OK, 'application/octet-stream')
                logging.info(resp)
                conn.sendall(resp)
            else:                
                resp = build_response('', NOTFOUND, '')
                logging.info(resp)
                conn.sendall(resp)
        else:
            resp = build_response('', NOTFOUND, '')
            logging.info(resp)
            conn.sendall(resp)
    elif method == 'POST':
        if p[1] == 'files' and len(p) > 2 and req_body:
            file_path = dir_path.joinpath(p[2])
            with open(file_path, "w") as f:
                f.write(req_body)
                f.close()
            resp = build_response('', CREATED, '') 
            logging.info(resp)
            conn.sendall(resp)
        else:
            resp = build_response('', BADREQ, '')
            logging.info(resp)
            conn.sendall(resp)
                        
        
if __name__ == '__main__':
    main()
