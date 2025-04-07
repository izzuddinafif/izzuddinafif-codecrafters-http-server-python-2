import socket  # noqa: F401


def main():
    port = 4221
    with socket.create_server(("localhost", port), reuse_port=True) as server:
        print(f"Afif's HTTP server started at {port}")  
        while True:
            conn, addr = server.accept()
            if conn:
                print(f"connection from {addr}")    
            
            
if __name__ == "__main__":
    main()
