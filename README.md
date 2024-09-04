# NanoCheeze Blockchain Music Streaming Server

## Overview

This project is a Python-based FastAPI server that streams MP3 music stored on a blockchain via Litecoin or NanoCheeze transactions. The server acts as a proxy to interact with the blockchain’s RPC servers, fetch transaction data, and reconstruct files from it.

The server provides a web interface where users can input a transaction ID (txid) and stream or download the MP3 file reconstructed from blockchain data. This project supports both HTTP and HTTPS protocols, with the ability to dynamically adjust the protocol depending on your environment.

![image](https://github.com/user-attachments/assets/e1d159d7-8a8f-46cb-8d97-ea4eb04ba552)

## Features

- **Blockchain Streaming:** Stream MP3 files stored in blockchain transactions using Litecoin or NanoCheeze.
- **Dynamic Protocol Handling:** Supports both HTTP and HTTPS, ensuring secure connections where needed.
- **SSL Configuration (Interactive):** Users can configure SSL via prompts at runtime.
- **Lightweight Web Interface:** Users can interact via a simple web interface to fetch and stream music.
- **MP3 Reconstruction:** Rebuilds MP3 files from multiple blockchain transactions.
- **Base64 Embedded Assets:** Assets like logos are embedded directly in the code as Base64-encoded strings, reducing the need for external files.

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


## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Contribution

Feel free to fork the repository and submit pull requests. We are open to any contributions or suggestions!
