# BitTorrent Client

A lightweight BitTorrent client built from scratch in Python.  
This project focuses on understanding the **BitTorrent protocol**, peer-to-peer networking, and file distribution.  
The client will handle `.torrent` file parsing, peer communication, piece downloading, and file reconstruction.

---

## 🚀 Tech Stack
- **Python** – Core programming language  
- **Sockets** – For peer-to-peer communication  
- **Asyncio** – For handling concurrent connections with peers  
- **bencodepy** – For parsing and encoding `.torrent` metadata  

---

## 📅 Roadmap

### Week 1
- Set up project structure  
- Learn the BitTorrent protocol basics  
- Implement `.torrent` file parser (using `bencodepy`)  

### Week 2
- Establish connections with peers (handshake using sockets)  
- Implement peer wire protocol basics  
- Manage multiple peers with `asyncio`  

### Week 3
- Download file pieces from peers  
- Handle piece verification with SHA-1 hashing  
- Reconstruct the original file  

### Week 4
- Optimize piece selection strategy (rarest-first, sequential)  
- Add upload capability (seeding)  
- Documentation & cleanup  

---

## 📖 Status
Currently working on **Week 1: Torrent file parser**.
