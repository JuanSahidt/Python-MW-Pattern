import socket
import os

IP = socket.gethostbyname(socket.gethostname())
PORT = 4456
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    while True:
        data = client.recv(SIZE).decode(FORMAT)
        cmd, msg = data.split("@")

        if cmd == "disconnected":
            print(f"[SERVER]: {msg}")
            break
        elif cmd == "OK":
            print(f"{msg}")

        data = input("> ")
        data = data.split(" ")
        cmd = data[0]

        if cmd == "help":
            client.send(cmd.encode(FORMAT))
        elif cmd == "exit":
            client.send(cmd.encode(FORMAT))
            break
        elif cmd == "list":
            client.send(cmd.encode(FORMAT))
        elif cmd == "remove":
            client.send(f"{cmd}@{data[1]}".encode(FORMAT))
        elif cmd == "upload":
            path = data[1]

            if os.path.isfile(path):
                with open(f"{path}", "rb") as f:
                    text = f.read()

                filename = path.split("/")[-1]
                send_data = f"{cmd}@{filename}@{text}"
                client.send(send_data.encode(FORMAT))

            else:
                send_data = f"{cmd}@notfound@notfound"
                client.send(send_data.encode(FORMAT))

    print("Disconnected from the server.")
    client.close()

if __name__ == "__main__":
    main()
