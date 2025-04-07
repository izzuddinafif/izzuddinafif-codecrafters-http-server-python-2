import socket


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
                    splitted_data = data.split(' ')
                    path = splitted_data[1]
                    handlePath(conn, path)

def handlePath(conn, path):
    if path != '/':
        conn.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")
    else:
        conn.sendall(b"HTTP/1.1 200 OK\r\n\r\n")            
        
        
if __name__ == "__main__":
    main()
