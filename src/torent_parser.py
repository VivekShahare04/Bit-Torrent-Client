import bencodepy
import sys
import math

def parse_torrent(file_path):
    with open(file_path,'rb') as f:
        torrent_data = bencodepy.decode(f.read())

    info = torrent_data[b'info']
    announce = torrent_data[b'announce'].decode('utf-8')
    name = info[b'name'].decode('utf-8')
    length = info[b'length']
    pieces_length = info[b'piece length']
    pieces = info[b'pieces']
    num_pieces = math.ceil(length / pieces_length)  # Assuming piece length is 16KB

    print(f"Announce URL: {announce}")
    print(f"File Name: {name}")
    print(f"File Length: {length} bytes")
    print(f"Number of Pieces: {num_pieces}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python torent_parser.py <path_to_torrent_file>")
    
    else:
        parse_torrent(sys.argv[1])