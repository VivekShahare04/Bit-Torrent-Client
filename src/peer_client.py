import socket
import hashlib
import sys

from helpers import update_peer_status, generate_peer_id
from peer_protocol import build_interest,parse_message,send_interested

#-------peer clas -------------
class Peer:
    def __init__(self, ip, port, peer_id):
        self.ip = ip
        self.port = port
        self.peer_id = peer_id
        self.available_pieces = set()  # Pieces this peer has
        self.connected = False
        self.failed_attempts = 0

peers_list = []  # From tracker_client

peer_objects = []
for ip, port in peers_list:
    p = Peer(ip, port, None)  # peer_id unknown initially
    peer_objects.append(p)
    print(f"Peer: {ip}:{port}, Connected: {p.connected}, Failed Attempts: {p.failed_attempts}")

# --- Handshake function ---
def handshake(peer_obj, info_hash, peer_id):
    """Perform BitTorrent handshake with a peer"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3)  # 5 seconds timeout
        s.connect((peer_obj.ip, peer_obj.port))

        # Build handshake message
        pstr = b"BitTorrent protocol"
        msg = (
            bytes([len(pstr)]) +  # protocol length
            pstr +
            b'\x00' * 8 +         # reserved bytes
            info_hash +
            peer_id.encode()
        )

        s.send(msg)

        # Receive handshake response
        response = s.recv(68)
        if len(response) < 68:
            print(f"Handshake failed with {peer_obj.ip}:{peer_obj.port}")
            update_peer_status(peer_obj, False)
            s.close()
            return None
        elif response[28:48] == info_hash:
            peer_id_recv = response[48:68].decode(errors='ignore')
            print(f"✅ Handshake successful with {peer_obj.ip}:{peer_obj.port}")
            print(f"🤝 Peer ID: {peer_id_recv}")
            update_peer_status(peer_obj, True, response[48:68].decode(errors='ignore'))
            send_interested(s)

            while True:
                data = s.recv(4096)
                if not data:
                    break
                msg_id, payload = parse_message(data)
                print(f"Received message ID: {msg_id}, Payload Length: {len(payload) if payload else 0}")
            return True
            
        else:
            print(f"Info hash mismatch with {peer_obj.ip}:{peer_obj.port}")
            update_peer_status(peer_obj, False)
            return None

    except Exception as e:
        print(f"Connection failed with {peer_obj.ip}:{peer_obj.port} - {e}")
        update_peer_status(peer_obj, False)
        return None

def after_handshake(sock):
    """ mesage after handshake has been done """

    try:
        msg = build_interest()
        sock.send(msg)

        response = sock.recv(4096)
        if response:
            msg_id, payload = parse_message(response)
            print(f"Received message ID: {msg_id}, Payload Length: {len(payload) if payload else 0}")
        else:
            print("No response received after sending interest message.")
    except Exception as e:
        print(f"Error during post-handshake communication: {e}")
    finally:
        sock.close()
    
# --- Main testing ---
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python peer_client.py <peer_ip> <peer_port> <info_hash_hex>")
        sys.exit(1)

    ip = sys.argv[1]
    port = int(sys.argv[2])
    info_hash_hex = sys.argv[3]  # hex string from torrent_parser
    info_hash = bytes.fromhex(info_hash_hex)
    peer_id = generate_peer_id()

    peer_obj = Peer(ip, port,peer_id)
    handshake(peer_obj, info_hash, peer_id)