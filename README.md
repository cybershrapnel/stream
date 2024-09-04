# NanoCheeze Blockchain Music Streaming Server

## Overview

This project is a Python-based FastAPI server that streams MP3 music stored on a blockchain via Litecoin or NanoCheeze transactions. The server acts as a proxy to interact with the blockchain’s RPC servers, fetch transaction data, and reconstruct files from it.

The server provides a web interface where users can input a transaction ID (txid) and stream or download the MP3 file reconstructed from blockchain data. This project supports both HTTP and HTTPS protocols, with the ability to dynamically adjust the protocol depending on your environment.

demo server (will lag if busy)
https://stream.nanocheeze.com

![image](https://github.com/user-attachments/assets/e1d159d7-8a8f-46cb-8d97-ea4eb04ba552)

## Features

- **Blockchain Streaming:** Stream MP3 files stored in blockchain transactions using Litecoin or NanoCheeze.
- **Dynamic Protocol Handling:** Supports both HTTP and HTTPS, ensuring secure connections where needed.
- **SSL Configuration (Interactive):** Users can configure SSL via prompts at runtime.
- **Lightweight Web Interface:** Users can interact via a simple web interface to fetch and stream music.
- **MP3 Reconstruction:** Rebuilds MP3 files from multiple blockchain transactions.
- **Base64 Embedded Assets:** Assets like logos are embedded directly in the code as Base64-encoded strings, reducing the need for external files.

---

### MEQUAVIS Upload and Download Protocol

The MEQUAVIS protocol is designed to enable efficient, decentralized file storage and retrieval across various blockchain networks, including NanoCheeze, Litecoin, and other cryptocurrencies. This protocol ensures secure, immutable storage and allows for the distribution of files directly on the blockchain, providing a unique approach to decentralized file management.

#### Key Features:

1. **Multi-Blockchain Support**: 
   - The protocol currently supports uploading and downloading files to and from NanoCheeze and Litecoin, with future support for Feathercoin, Dogecoin, Mooncoin, Dimecoin, Bitcoin, and more. 
   - By leveraging these networks, it ensures redundancy, security, and accessibility, while offering the ability to store data in distributed ledgers.

2. **File Chunking and Reconstruction**:
   - Files are broken into smaller chunks, which are uploaded as individual transactions onto the blockchain. Each transaction contains a portion of the file data, stored in the OP_RETURN field, ensuring immutability and verification.
   - The protocol automatically reconstructs these chunks during download, ensuring that the original file is restored with accuracy. This process guarantees that no intermediary or third-party storage is needed—everything is self-contained on the blockchain.

3. **Blockchain Agnostic**:
   - While initially built for NanoCheeze and Litecoin, the protocol is designed to be modular and adaptable to other blockchain networks. This future-proofing ensures the protocol's flexibility and scalability as more blockchain networks adopt decentralized storage solutions.

4. **Immutability and Decentralization**:
   - Each uploaded file, or file chunk, is stored in a permanent, immutable state on the blockchain, guaranteeing that files cannot be altered or tampered with post-upload.
   - This decentralized approach ensures there is no central point of failure, and files remain accessible as long as the blockchain network itself remains operational.

5. **Efficient Retrieval with Batch Processing**:
   - The download mechanism uses optimized batch processing techniques for faster retrieval. This feature speeds up the process of downloading large files by fetching multiple transactions at once and reducing wait times, compared to traditional sequential downloads.

6. **Use Case**:
   - While initially tailored for MP3 and audio file storage, the protocol can be extended to handle any file type. Current development efforts are focused on adding support for non-MP3 files, making it a universal tool for decentralized storage of digital assets and data.

#### Future Development:

- **Extended Support for More Blockchains**: Integration with additional blockchain networks is in the pipeline, broadening the scope of decentralized file storage options.
  
- **Non-MP3 Support**: Soon, the protocol will allow for the upload and retrieval of other file types, providing even more flexibility for users needing decentralized storage. The MEQUAVIS JAVA app already has this support.

### MEQUAVIS Protocol: The Unstoppable Force in Decentralized Storage

The MEQUAVIS upload and download protocol represents the next evolution of decentralized file sharing and storage. In its current state, it operates as a *literal unstoppable version of Napster*, built on blockchain technology, where files are permanently embedded into distributed, immutable ledgers across multiple blockchain networks. Once a file is uploaded, it cannot be altered, deleted, or removed. This makes it the embodiment of the unstoppable force and the immovable object in the truest digital sense.

#### Why It's Unstoppable:

1. **Immutability on the Blockchain**:
   - Every file uploaded via the MEQUAVIS protocol is split into chunks and stored as transactions on the blockchain. These transactions are recorded in the blockchain's history and become a permanent part of the distributed ledger. Once a file or its chunks are recorded on-chain, they cannot be erased, modified, or censored. This makes them virtually indestructible, as long as the blockchain itself exists.
  
2. **Decentralized by Nature**:
   - Unlike traditional file-sharing systems, there’s no central server or company hosting these files. The file chunks are stored across a global network of blockchain nodes. Even if individual nodes go down or are targeted, the files remain accessible as long as other nodes on the network are operational. The decentralized nature of blockchain means there is no single point of failure, and no one entity has control over the network.

3. **No Central Authority to Take Down**:
   - Since files are stored directly on the blockchain, there is no central authority that can be pressured or forced to take down content. There are no domain names, centralized hosting services, or databases that can be seized or shut down. The protocol operates independently of any organization or government, making it immune to takedown attempts or legal intervention.

4. **Peer-to-Peer, With Cryptographic Integrity**:
   - Similar to how Napster operated in a peer-to-peer fashion, the MEQUAVIS protocol allows anyone to retrieve files directly from the blockchain by reconstructing them from the transactions that hold the file data. This means users can share and download files with cryptographic guarantees that the file they receive is exactly the same as what was uploaded, ensuring integrity and trust in the data.
  
5. **Unstoppable Distribution**:
   - Once a file is uploaded to the blockchain, it is distributed across multiple nodes globally. These nodes don’t just store the file; they store cryptographically linked transactions that represent the file. It’s like having the blueprints for reconstructing the file baked into the blockchain itself. There is no "kill switch" or centralized choke point that can be exploited to stop the system.

6. **Beyond Censorship**:
   - With traditional platforms, files can be deleted, accounts can be banned, or websites can be taken down. In contrast, the MEQUAVIS protocol doesn’t allow for this kind of control. Files uploaded to the blockchain are embedded in an incorruptible digital archive. Since blockchains like NanoCheeze and Litecoin are decentralized and cryptographically secured, they are resistant to censorship, making MEQUAVIS an unyielding force for file storage.

#### The Immovable Object:

1. **Permanence**:
   - Once data is written onto the blockchain, it stays there forever. Unlike cloud storage services where data can be deleted, modified, or subjected to corporate policy changes, MEQUAVIS ensures that the files remain exactly as they were when first uploaded. It’s impossible to remove a file from the blockchain without destroying the entire network, a feat no single entity can achieve.

2. **Indestructibility of Data**:
   - Files stored through MEQUAVIS are etched into the blockchain’s digital stone. As long as the blockchain exists, the files exist. The blockchain's cryptographic structure ensures that once data is added, it can't be retroactively altered or deleted, making MEQUAVIS not only unstoppable but also immovable in terms of data permanence.

3. **Global Accessibility**:
   - The decentralized nature of blockchains ensures that the file is accessible globally, regardless of geographical restrictions. This means the protocol enables free access to files for anyone with an internet connection and a blockchain client, making MEQUAVIS a truly borderless and indomitable platform.

#### Current Status:

- MEQUAVIS already allows the uploading and downloading of any file type (with current primary focus on MP3 files) via the NanoCheeze and Litecoin blockchains. Its support will soon extend to Feathercoin, Dogecoin, Mooncoin, Dimecoin, and more.
- Though currently optimized for MP3 files, the web server will soon enable users to upload and retrieve **any file type**, making the protocol a universal tool for decentralized, unstoppable storage.
  
#### The Future of Unstoppable File Sharing:

The MEQUAVIS protocol doesn't just store files; it embeds them into the very fabric of the blockchain. There is no button to press, no server to shut down, and no regulatory framework that can stop it. Files stored through this protocol are destined to exist for as long as the blockchain operates, making MEQUAVIS the ultimate force for truly unstoppable, decentralized file sharing.

In short, MEQUAVIS is the evolution of Napster, but without any of the vulnerabilities. It is the future of file storage in a world where data can't be censored, removed, or destroyed—a permanent, decentralized network for digital immortality.

---

## Project Structure

```
.
├── server.py                 # The main FastAPI server script (self-contained)
├── certificate.pem           # Optional SSL certificate file (if needed)
├── private.key               # Optional SSL private key file (if needed)
└── README.md                 # This file
```
The old folder is just old junk code for reference, and the ico, png, and html file are for github pages to serve the main files of the public server bridged over to my version of the proxy server so people can demo.
These 3 files and directory are not needed, The only file you need is server.py or sever.exe from the releases page https://github.com/cybershrapnel/stream/releases/download/main/server.exe

## How It Works

1. **Blockchain Interaction:** The server communicates with the Litecoin and NanoCheeze blockchains using their respective RPC APIs.
2. **Data Reconstruction:** MP3 file chunks are stored in OP_RETURN outputs of transactions. The server fetches and reconstructs the file from these chunks.
3. **Web Interface:** A web interface is provided for users to input transaction IDs, stream the music, and download the reconstructed MP3 files.
4. **Embedded Resources:** All assets, including the logo, are base64 encoded and embedded directly within the code, eliminating the need for external files except for optional SSL certificates.
5. **Dynamic Protocol Selection:** The server determines whether to run over HTTP or HTTPS based on SSL configurations, adjusting the protocol accordingly for both server and client interactions.

## Installation

### Prerequisites

- Python 3.8+
- `uvicorn`, `fastapi`, and other required Python packages (installed via `requirements.txt`)
- A valid Litecoin or NanoCheeze node running locally or remotely

### Step-by-Step Guide

1. **Clone the Repository:** (note: you only need to download the server.py file)
   ```bash
   git clone https://github.com/yourusername/nanocheeze-music-streaming.git
   cd nanocheeze-music-streaming
   ```

2. **Install Dependencies:**
   Install the required Python packages:
   ```bash
   pip install fastapi uvicorn httpx
   ```

3. **Run the Server:**
   Run the server script directly. During execution, the server will prompt you to configure the following options:

   - **SSL (Yes/No)**: The server will ask if you want to use SSL. If you select "Yes," it will automatically configure HTTPS using `certificate.pem` and `private.key` files.
   - **Host (Local or Exposed)**: You will be asked if you want to run the server locally (on `127.0.0.1`) or exposed to the internet (`0.0.0.0`).
   - **Custom or Default Configuration**: The script will prompt whether to use default or custom configuration values for Litecoin and NanoCheeze RPC settings.

   Simply follow the prompts to set up the server.

   **Example**:
   ```bash
   python server.py
   ```

4. **Access the Web Interface:**
   After starting the server, you can access the web interface at:
   ```
   http://127.0.0.1:8111/music  (for HTTP)
   https://127.0.0.1:8111/music (for HTTPS, if enabled)
   ```

5. **Input a Transaction ID:**
   Use the web interface to input a Litecoin or NanoCheeze transaction ID. The server will fetch and reconstruct the MP3 file from the blockchain.

6. **Download and Stream Music:**
   Stream the MP3 file directly from the interface or download the file to your local system.

## Usage

### Running the Server

- **With Interactive SSL Configuration:**
  Run the server, and the script will ask whether or not to enable SSL. There is no need for manual configuration or additional command-line arguments.

  ```bash
  python server.py
  ```

- **Prompts You Will See:**
  1. Do you want to use custom values for RPC configuration? (Yes/No)
  2. Do you want to run locally or exposed to the internet? (Local/Exposed)
  3. Do you want to enable SSL? (Yes/No)
  
  If you select "Yes" for SSL, the script will look for `certificate.pem` and `private.key` files in the directory and enable HTTPS automatically.

### Streaming a Song

1. Open the web interface in your browser.
2. Select either "Litecoin" or "NanoCheeze" as your crypto option.
3. Enter the blockchain transaction ID (txid) that contains the song data.
4. Click "Stream MP3 from Hash" to start playing or downloading the song.

### SSL Configuration

If you want to run the server over HTTPS, during runtime you will be prompted with the option to enable SSL. If you choose "Yes," the server will require `certificate.pem` and `private.key` files to be present in the directory for SSL configuration.

## Configuration

**Note**: All configurations, including RPC credentials and proxy interactions, are hardcoded into the server script for simplicity and security. There is no need to modify configuration files directly.

- **Base64 Embedded Assets**: The logo and other assets are embedded directly into the server script as Base64-encoded strings, so no additional static files are needed.

## Known Issues

- Ensure your nodes are running and accessible. If the server cannot reach the Litecoin or NanoCheeze nodes, you will encounter connection errors.
- If the MP3 reconstruction fails, ensure the blockchain transaction contains the correct OP_RETURN data for the MP3 chunks.


---

## Using the MEQUAVIS Java App for File Uploads and Downloads

The **MEQUAVIS Java App** is a powerful tool that enables users to upload and download any type of file to and from multiple blockchain networks, including NanoCheeze and Litecoin. Although the current web server is limited to handling MP3 files, the MEQUAVIS Java app extends support to a broader range of cryptocurrencies and file types.

### Supported Cryptocurrencies

The MEQUAVIS Java app currently supports file upload and download to the following blockchains:

- NanoCheeze
- Litecoin
- Feathercoin
- Dogecoin
- Mooncoin
- Dimecoin
- Bitcoin
- **And several others...**

### File Types

The MEQUAVIS Java app can handle **any file type**. This means you can upload and download files of any format, not just MP3s, to and from the supported blockchains.

### How to Use the MEQUAVIS Java App

1. **Download the MEQUAVIS Java App**:
   - Obtain the Java application from the official NanoCheeze or MEQUAVIS GitHub repository.
   - There are several options for installing MEQUAVIS/NanoCheeZe. (The JAVA app is extremely experimental)
   - https://github.com/cybershrapnel/NanoCheeZe/releases/tag/3.1.2.9
   
2. **Configure Blockchain Node Access**:
   - Ensure that your local or remote blockchain nodes (Litecoin, NanoCheeze, etc.) are running and accessible to the MEQUAVIS Java app.
   
3. **Upload Files**:
   - Launch the MEQUAVIS app and select the blockchain where you'd like to store your file. The app allows you to split your file into chunks and store them within blockchain transactions using the OP_RETURN field.

4. **Download Files**:
   - Simply enter the transaction ID (txid) of the blockchain transaction where the file is stored. The MEQUAVIS app will fetch, reconstruct, and download the file for you.

### Upcoming Web Server Features

While the current web server is designed to handle MP3 files, support for **additional file types** is planned for future updates. The goal is to extend the server's capabilities to allow downloading **any type of file** uploaded through the MEQUAVIS Java app.

In addition, **support for more cryptocurrencies** (such as Feathercoin, Dogecoin, Mooncoin, Dimecoin, and others) is also on the development roadmap, which will expand the server's ability to interact with various blockchains.

---

This is a standalone exe that runs the python server.

Must be running Litecoin-qt node with txindex enabled

I will release a new version soon that includes the litecoin exe and a fast sync option to get up and running easy for those that have never ran a node.

put your key and pem file in the same directory as the exe for https support.
note that running https over localhost will always say your cert is invalid unless you created your cert local for the local loopback.

This is a very early barely functioning release.
access [https://127.0.0.1:8111/music](https://127.0.0.1:8111/music) if it doesn't load automatically.
or [http://127.0.0.1:8111/music](http://127.0.0.1:8111/music) if not running ssl

---

To build the server from the server.py file as an exe you will need PyInstaller for python to build the application.

I was not able to build the exe without explicitly including these imports and the hsts bin file. You will need to locate the hstspreload.bin in your actual python directory and change the path accordingly. Just in case anyone wants to build on their own.

python -m PyInstaller --onefile --icon=favicon.ico --hidden-import=httpx --hidden-import=httpx._exceptions --hidden-import=httpx._client --hidden-import=httpx.HTTPStatusError --hidden-import=httpx.RequestError --hidden-import=hstspreload --add-data "C:/Users/user/AppData/Roaming/Python/Python311/site-packages/hstspreload/hstspreload.bin;hstspreload" server.py

---


## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Contribution

Feel free to fork the repository and submit pull requests. We are open to any contributions or suggestions!
