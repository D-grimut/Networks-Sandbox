import socket as sk
import threading
from packet import Packet
from packet import PacketType

class Server():

    PORT = 5050
    IP = sk.gethostbyname(sk.gethostname())
    ADDR = (IP, PORT)

    def __init__(self):
        self.cleints = {}
        self.sock = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        self.sock.bind(Server.ADDR)
    

    def handle_client(conn: sk.socket, addr: int):

        dest_ip, dest_port = addr
        connetced = True 

        buffer_slots = 5
        buffer = buffer_slots * [None]

        expected_seq_num = -1

        print(f'[CONNECTED] user with ip {dest_ip} and port number {dest_port} has connected')

        while connetced:
            raw_data = conn.recv(4096)
            
            packet = Packet.from_bytes(raw_data)
            seq_num = packet.seq_num

            if packet.type == PacketType.SYN:
                print(f"[RECIEVED] Syn recived, expecting seq num: {seq_num}")
                expected_seq_num = seq_num
                continue
            
            elif packet.type != PacketType.DATA: # this can be extended later to accomodate for two way data transfers
                continue

            slot = seq_num % buffer_slots
            buffer[slot] = {"packet" : packet, "seq num" : seq_num}

            if seq_num != expected_seq_num:
                print(f"[SENDING] Out of Order (recieved: {seq_num}) - sending last well recieved ACK {expected_seq_num - 1}")
                ack_pack = Packet(PacketType.ACK, expected_seq_num - 1, "ACK")
                conn.send(ack_pack.to_bytes())

            else:
                i = slot

                print("[RECIEVED] Printing all data freed by this packet")

                while buffer[i] != None:
                    
                    processing_seq = buffer[i]['seq num']
                    expected_seq_num = processing_seq + 1
                    print(buffer[i]['packet'].data.decode())
                    buffer[i] = None
                    i += 1

                    if i == len(buffer):
                        i = i % len(buffer)
                    
                    print(f"[SENDING] ACK for seq num {seq_num}")
                    ack_pack = Packet(PacketType.ACK, processing_seq, "ACK")
                    conn.send(ack_pack.to_bytes())
                
                print("[RECIEVED] Done ----")

    def start_server(self):
        
        self.sock.listen()
        print("Server Listening")
        while True:
            conn, addr = self.sock.accept()
            thread = threading.Thread(target=Server.handle_client, args=(conn, addr))
            thread.start()


server = Server()
server.start_server()