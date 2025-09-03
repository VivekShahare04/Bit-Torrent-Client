import struct

#..........message ids.........
CHOKE = 0
UNCHOKE = 1
INTERESTED = 2
NOT_INTERESTED = 3
HAVE = 4
BITFIELD = 5
REQUEST = 6
PIECE = 7
CANCEL = 8
PORT = 9


#.......function for this messae......
def build_interest():
    return struct.pack(">IB", 1, INTERESTED)

def build_uninterest():
    return struct.pack(">IB", 1, NOT_INTERESTED)

def build_choke():
    return struct.pack(">IB", 1, CHOKE)

def build_unchoke():
    return struct.pack(">IB", 1, UNCHOKE)

def build_have(piece_index):
    return struct.pack(">IBI", 5, HAVE, piece_index)

def build_request(piece_index, begin, length):
    return struct.pack(">IBIII", 13, REQUEST, piece_index, begin, length)   

def build_piece(piece_index, begin, block):
    block_length = len(block)
    return struct.pack(">IBII", 9 + block_length, PIECE, piece_index, begin) + block

def build_cancel(piece_index, begin, length):
    return struct.pack(">IBIII", 13, CANCEL, piece_index, begin, length)

def build_port(port):
    return struct.pack(">IBH", 3, PORT, port)

# --- Message Parser ---
def parse_message(data):
    """
    Parse a raw message from peer
    Returns: (id, payload)
    """
    if len(data) < 4:
        return None, None

    length = struct.unpack(">I", data[:4])[0]
    if length == 0:
        return "keep-alive", None

    msg_id = data[4]
    payload = data[5:4+length]

    return msg_id, payload

def send_interested(sock):
    """Send 'interested' message to the peer"""
    try:
        # length prefix (4 bytes) + message ID (1 byte)
        msg = struct.pack(">IB", 1, 2)  # 1 = length, 2 = interested
        sock.send(msg)
        print("📩 Sent 'interested' message to peer")
    except Exception as e:
        print(f"❌ Failed to send interested message: {e}")