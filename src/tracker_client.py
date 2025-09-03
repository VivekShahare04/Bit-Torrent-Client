import bencodepy
import hashlib
import requests
import urllib.parse
import sys
from helpers import parse_compact_peers, generate_peer_id

def contact_tracker(torrent_file):
    # Parse torrent file or we can add logic if torrent file is starting with http that means its a url so download it then bencode the data
    with open(torrent_file, "rb") as f:
        torrent_bytes = f.read()
        torrent_data = bencodepy.decode(torrent_bytes)

    info = torrent_data[b'info']
    announce = torrent_data[b'announce'].decode("utf-8")
    length = info[b'length']

    # Info hash (raw 20-byte, not hex)
    info_bencoded = bencodepy.encode(info)
    info_hash = hashlib.sha1(info_bencoded).digest()

    # URL-encode info_hash
    info_hash_encoded = urllib.parse.quote_from_bytes(info_hash)
    print(f"Info Hash: {info_hash.hex()}")

    # Peer ID
    peer_id = generate_peer_id()

    # Build request URL
    params = {
        "info_hash": info_hash_encoded,
        "peer_id": peer_id,
        "port": 6881,
        "uploaded": 0,
        "downloaded": 0,
        "left": length,
        "compact": 1
    }
    url = announce + "?" + "&".join([f"{k}={v}" for k,v in params.items()])

    print("Tracker Request URL:")
    print(url)

    # Send request
    resp = requests.get(url)
    tracker_response = bencodepy.decode(resp.content)
    print("\nTracker Response:")
    print(tracker_response)

    # Extract compact peers
    peers_binary = tracker_response[b'peers']
    peers_list = parse_compact_peers(peers_binary)

    print("\nPeers List:")
    for ip, port in peers_list:
        print(f"{ip}:{port}")

    return peers_list, info_hash, peer_id


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python tracker_client.py <path_to_torrent_file>")

    else:
        contact_tracker(sys.argv[1])
