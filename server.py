import socket as sk
import threading
from packet_helper import Helper

class Server():

    PORT = 5050
    IP = sk.gethostbyname(sk.gethostname())
    ADDR = (IP, PORT)

    def __init__(self, is_udp):
        self.cleints = {}
        self.sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM) if is_udp else sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        self.sock.bind(Server.ADDR)

    def handle_client(conn: sk.socket, addr: int):

        dest_ip, dest_port = addr

        connetced = True 
        handshake = True

        print(f'user with ip {dest_ip} and port number {dest_port} has connected - starting three way handshake')

        while connetced:
            # rcv seq_num + send back syn and ack
            second_handshake = conn.recv(Helper.MAX_PACKET_SIZE)
            test = second_handshake[:96].decode().replace(" ", "")

            if(len(test) > 1):

                while handshake:
                    conn.send(Helper.prepare_packet(second_handshake, dest_port, Server.PORT))

                    # recieve ACK and begin communication
                    third_handshake = conn.recv(Helper.ACK_NUM)
                    syn_ack = int(third_handshake[Helper.SEQ_NUM: Helper.ACK_NUM].decode())

                    print("Three way handshale complete - Happy chatting!")
                    handshake = False
                
                msg = second_handshake.decode().strip()
                print(f'{dest_ip} says : {msg}')

                if msg == Helper.END:
                    connetced = False


        

    def start_server(self):
        
        self.sock.listen()
        print("Server Listening")
        while True:
            conn, addr = self.sock.accept()
            thread = threading.Thread(target=Server.handle_client, args=(conn, addr))
            thread.start()


server = Server(False)
server.start_server()