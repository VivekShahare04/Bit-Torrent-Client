from tracker_client import contact_tracker
from peer_client import Peer, handshake, after_handshake
from helpers import generate_peer_id
import os
import sys

#1.contact tracker and get list of peers
peers,info_hash, peer_id = contact_tracker(r"c:\Users\Vivek Shahare\Downloads\ubuntu-22.04.5-desktop-amd64.iso.torrent")
#2. pick first peer now
if peers:
    ip,port = peers[0]
    peer = Peer(ip,port,None)
    print(f"Attempting handshake with {ip}:{port}")
#3. handshake with peer
sock = handshake(peer,info_hash,peer_id)
#4. after handshake send interested message
if sock:
    after_handshake(sock)

