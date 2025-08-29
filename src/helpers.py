import socket
import struct
import random
import string
def parse_compact_peers(peers_binary):
    """
    peers_binary: b'...'  # from tracker response b'peers'
    Returns: list of (ip, port)
    """
    peers = []
    for i in range(0, len(peers_binary), 6):
        ip_bytes = peers_binary[i:i+4]
        port_bytes = peers_binary[i+4:i+6]

        ip = socket.inet_ntoa(ip_bytes)
        port = struct.unpack(">H", port_bytes)[0]
        peers.append((ip, port))
    return peers

def generate_peer_id():
    # Example peer_id format: -PC0001-<random 12 chars>
    return "-PC0001-" + ''.join(random.choices(string.ascii_letters + string.digits, k=12))


#updation after handshake has been done
def update_peer_status(peer_obj, success, peer_id=None):
    if success:
        peer_obj.connected = True
        if peer_id:
            peer_obj.peer_id = peer_id
    else:
        peer_obj.failed_attempts += 1
        if peer_obj.failed_attempts >= 3:
            peer_obj.connected = False  # drop peer after repeated failures
