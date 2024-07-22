import socket as sk
from packet_helper import Helper
import time

class Client:

    def __init__(self, has_TLS = False, server_ip = "192.168.2.74", server_port = 5050):
        self.has_TLS = has_TLS
        self.timeout = 5
        self.server_addr = (server_ip, server_port)
        
        self.sock = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        self.info = self.sock.getsockname()


    def establish_TCP(self):

        self.sock.connect(self.server_addr)
        initial_seq = 9

        # First handshake
        encoded_source_port = Helper.encode_data(self.info[1], 16)
        encoded_dest_port = Helper.encode_data(self.server_addr[1], 16)

        encoded_seq_num = Helper.encode_data(initial_seq, 32)
        encoded_ack_num = Helper.encode_data("", 32)

        encoded_message = Helper.encode_data("Why are you looking at the data so early in the handshake?", Helper.MAX_PACKET_SIZE - 96)
        self.sock.send(encoded_source_port + encoded_dest_port + encoded_seq_num + encoded_ack_num + encoded_message)

        # Third Handshake
        third_hanshake = self.sock.recv(Helper.MAX_PACKET_SIZE)
        self.sock.send(Helper.prepare_packet(third_hanshake, self.server_addr[1], self.info[1]))

        time.sleep(5)

        self.sock.send("bim boom".encode())
        time.sleep(1)

        self.sock.send("bam bim".encode())
        time.sleep(1)

        self.sock.send("my elden ring build is op".encode())
        self.sock.send(Helper.END.encode())


client = Client()
client.establish_TCP()