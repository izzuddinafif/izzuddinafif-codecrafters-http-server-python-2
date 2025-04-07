import socket

def main():
    port = 4221
    with socket.create_server(("localhost", port), reuse_port=True) as server:
        print(f"Afif's HTTP server started at {port}")
        while True:
            conn, addr = server.accept()
            with conn:
                print(f"connected by {addr[0]} from port {addr[1]}")
                conn.sendall(b"HTTP/1.1 200 OK\r\n\r\n")

            
if __name__ == "__main__":
    main()
