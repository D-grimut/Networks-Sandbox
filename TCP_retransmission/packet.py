import struct
import enum

class PacketType(enum.IntEnum):
    DATA = ord('D')
    ACK = ord('A')
    SYN = ord('S')

class Packet:
    _PACK_FORMAT = '!BI'
    _HEADER_SIZE = struct.calcsize(_PACK_FORMAT)
    MAX_DATA_SIZE = 1400

    def __init__(self, type, seq_num, data: str):
        self.type = type
        self.seq_num = seq_num
        self.data = data

    def to_bytes(self):
        header = struct.pack(Packet._PACK_FORMAT, self.type.value, self.seq_num)
        return header + self.data.encode()

    @classmethod
    def from_bytes(cls, raw):
        header = struct.unpack(Packet._PACK_FORMAT, raw[:Packet._HEADER_SIZE])
        type = PacketType(header[0])
        seq_num = header[1]
        data = raw[Packet._HEADER_SIZE:]
        return cls(type, seq_num, data)