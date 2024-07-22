class Helper():

    # Mimicking TCP packet structure (skipping some stuff for simplicity)
    TCP_SRC_PORT = 16
    TCP_DEST_PORT = TCP_SRC_PORT + 16
    SEQ_NUM = TCP_DEST_PORT + 32
    ACK_NUM = SEQ_NUM + 32
    DATA = ACK_NUM

    MAX_PACKET_SIZE = 100000

    MISSING_SYN_MSG = "!MISSING_SYN"
    END = "!END"

    def __init__(self) -> None:
        pass

    def encode_data(data, max_length):
        encoded = str(data).encode()
        encoded += b' ' * (max_length - len(encoded))
        return encoded
    

    def prepare_packet(encrypted_packet, dest_port, source_port):
        recv_initial_seq = int(encrypted_packet[Helper.TCP_DEST_PORT: Helper.SEQ_NUM].decode())
        send_initial_seq = 5
        ack = recv_initial_seq + 1

        print(f'[RECIEVED from {dest_port}] initial seuqence num {recv_initial_seq}')

        encoded_source_port = Helper.encode_data(source_port, 16)
        encoded_dest_port = Helper.encode_data(dest_port, 16)

        encoded_seq_num = Helper.encode_data(send_initial_seq, 32)
        encoded_ack_num = Helper.encode_data(ack, 32)

        encoded_message = Helper.encode_data("Why are you looking at the data so early in the handshake?", Helper.MAX_PACKET_SIZE - 96)

        return encoded_source_port + encoded_dest_port + encoded_seq_num + encoded_ack_num + encoded_message
