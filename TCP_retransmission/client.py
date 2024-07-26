import socket as sk
import threading
import numpy as np
from packet import Packet, PacketType
import time

class Client:

    DROPOUT_RATE = 0.3

    def __init__(self,server_ip = "192.168.2.74", server_port = 5050):

        self.server_addr = (server_ip, server_port)
        
        self.sock = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        self.info = self.sock.getsockname()

        self.buffer_slots = 5
        self.buffer = self.buffer_slots * [None]
        self.timer = None

        self.last_seq_sent = -1
        self.last_ack_recieved = 4

        self.semaphore = threading.Semaphore(self.buffer_slots)

        self.sock.connect(self.server_addr)

        syn_packet = Packet(PacketType.SYN, self.last_ack_recieved + 1, "")
        self.sock.send(syn_packet.to_bytes())

        self.last_seq_sent = self.last_ack_recieved

        self.thread = threading.Thread(target=self.recv_ack)
        self.thread.start()
 

    def encode_data(data: str) -> list:
        
        core_data = []
        for c in data:
            core_data.append(c)

        return core_data


    def timeout(self):

        re_transmit_seq_num = self.last_ack_recieved + 1
        slot = re_transmit_seq_num % self.buffer_slots

        if self.buffer[slot] and self.buffer[slot]['seq num'] == re_transmit_seq_num:
            print(f"[TIMEOUT] Re-transmitting last packet sent seq num: {re_transmit_seq_num}")
            self.send_packet(packet=self.buffer[slot]['packet'])
    

    def get_message(self):

        message = None

        print("Type message to send to da serwer:")
        message = input()

        core_data = Client.encode_data(message)

        for data in core_data:
            self.send_packet(data)


    def send_packet(self, data=None, packet=None):

        # if packet passed, use it, otherwise create it
        if not packet:
            self.semaphore.acquire()
            packet = Packet(PacketType.DATA, self.last_seq_sent + 1, data)
            self.last_seq_sent = self.last_seq_sent + 1

        slot = packet.seq_num % self.buffer_slots
        self.buffer[slot] = {"packet" : packet, "seq num" : packet.seq_num}
        print(f"[SENDING] Sending packet {packet.seq_num}")
        self.sock.send(packet.to_bytes())

        #start timout timer
        if self.timer is not None:
            self.timer.cancel()
        self.timer = threading.Timer(interval=3.0, function=self.timeout)
        self.timer.start()

        time.sleep(0.5)
        
    # we are recieving CUMULATIVE ACKs
    def recv_ack(self):
        while True:
        
            raw_data = self.sock.recv(4096)

            if raw_data is None:
                continue

            recv_packet = Packet.from_bytes(raw_data)

            if recv_packet.type != PacketType.ACK:
                continue

            ack_num = recv_packet.seq_num

            dropout = np.random.uniform(0, 1)
            if dropout <= Client.DROPOUT_RATE:
                print(f"[DROPPING] Dropped ACK {ack_num}")
                continue

            print(f"[RECIEVED] ACK for packet {ack_num}")

            self.last_ack_recieved = ack_num
            start, end  = self.last_seq_sent - self.buffer_slots + 1, ack_num + 1

            for seq_num in range(start, end):
                slot = seq_num % self.buffer_slots
                self.buffer[slot] = None
                self.semaphore.release()
                
            if self.last_seq_sent == ack_num:
                print(f"[RECIEVED] Last ACK - num: {ack_num} - stopping timer")
                self.timer.cancel()

client = Client()
client.get_message()