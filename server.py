#This is standalone server that can be used anywhere that is running a litecoin node to stream from LTC or NCZ (Must have -txindex enabled in ltc config)
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import httpx
import base64
import json
import uvicorn
import webbrowser
import asyncio

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Default RPC server details
DEFAULT_RPC_USER = "nanocheeze"
DEFAULT_RPC_PASSWORD = "ncz"
DEFAULT_RPC_URL = "http://127.0.0.1:12782"

DEFAULT_LITE_RPC_URL = "http://127.0.0.1:9332"  # Adjusted port for Litecoin

# Variables to hold custom or default values
RPC_USER = DEFAULT_RPC_USER
RPC_PASSWORD = DEFAULT_RPC_PASSWORD
RPC_URL = DEFAULT_RPC_URL

LITE_RPC_URL = DEFAULT_LITE_RPC_URL
HOST = "127.0.0.1"
USE_SSL = False

# Create a global HTTPX client with connection pooling
client = httpx.AsyncClient()

# Embedded HTML content
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Streaming Music from Blockchain</title>
    <style>
        textarea {
            width: 100%;
            height: 200px;
            font-family: monospace;
            margin-top: 10px;
        }

        body {
            background-color: #000000;
            color: #ffffff;
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            text-align: center;
        }

        h1, label, textarea, input, button, a {
            color: #ffffff;
        }

        textarea, input, button {
            background-color: #333333;
            border: 1px solid #555555;
            color: #ffffff;
        }

        textarea {
            resize: none;
        }

        button {
            cursor: pointer;
            padding: 10px 20px;
            margin-top: 10px;
        }

        button:hover {
            background-color: #444444;
        }

        a {
            color: #00ff00;
            text-decoration: none;
            margin-top: 20px;
            display: inline-block;
        }

        a:hover {
            text-decoration: underline;
        }

        img {
            max-width: 100%;
            height: auto;
        }

        .media-player-container {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: 20px;
            flex-direction: column;
        }

        ul.hash-list {
            list-style-type: none;
            padding: 0;
            margin: 20px 0 0;
        }

        ul.hash-list li {
            cursor: pointer;
            color: #00ff00;
            margin-bottom: 5px;
        }

        ul.hash-list li:hover {
            text-decoration: underline;
        }
    </style>
    <style>
    /* Default styles for larger screens */
    body {
        font-size: 16px;
        line-height: 1.5;
    }

    h1, label, textarea, input, button, a {
        font-size: 1em;
    }

    textarea {
        width: 100%;
        height: 200px;
    }

    .media-player-container, .hash-list, .media-player-container a, button {
        font-size: 1em;
    }

    .media-player-container {
        width: 100%; /* Ensures media player uses full width of the container */
        //background-color: #333; /* Dark theme background */
        color: #fff; /* Light color for text */
        padding: 10px; /* Adds padding around the media player for better spacing */
        border-radius: 5px; /* Optional: adds rounded corners */
    }

    .media-player-container img {
        max-width: 100%; /* Ensures images within the media player scale down */
        height: auto; /* Maintains aspect ratio */
    }

    audio {
        width: 100%; /* Audio controls stretch to container width */
        //background-color: #222; /* Dark theme for audio controls */
        color: #fff; /* Ensures control icons are visible */
    }

    audio::-webkit-media-controls-panel {
        background-color: #222; /* Dark background for controls */
        color: #fff; /* Light color for icons and text */
    }

    audio::-webkit-media-controls-play-button,
    audio::-webkit-media-controls-timeline,
        audio::-webkit-media-controls-volume-slider {
    filter: invert(1); /* Invert colors to make them white on dark background */
}
        
    /* Styles for screens smaller than 800px */
    @media (max-width: 800px) {
        body {
            font-size: 12px; /* Smaller font size */
            line-height: 1.2;
        }

        h1 {
            font-size: 1.5em;
        }

        label, textarea, input, button, a {
            font-size: 0.8em; /* Make fonts smaller */
        }

        textarea {
            width: 100%;
            height: 150px; /* Reduce height */
        }

        .media-player-container, .hash-list, .media-player-container a, button {
            font-size: 0.8em; /* Adjust font size */
        }

        .media-player-container img {
            max-width: 80%; /* Reduce image size */
        }

        /* Adjust the margins and padding for smaller screens */
        body {
            padding: 10px;
        }

        .media-player-container, .hash-list {
            margin-top: 10px;
        }

        button {
            padding: 5px 10px; /* Smaller button padding */
        }

        /* Additional adjustments for smaller screens */
        input, textarea, button {
            border-width: 1px; /* Thinner borders */
        }

        .hash-list li {
            margin-bottom: 3px; /* Less spacing between list items */
        }
    }
</style>

<script>

document.addEventListener("DOMContentLoaded", function() {
    // Check if the page is being viewed in a frame
    if (window.self !== window.top) {
        // This means the page is in a frame
        document.body.style.backgroundColor = "rgba(0, 0, 0, 0.0)"; // more transparent
    } else {
        // This means the page is not in a frame
        document.body.style.backgroundColor = "rgba(0, 0, 0, 0.95)"; // less transparent
    }
});


    
let mediaSource;
let sourceBuffer;
let queue = [];
let fileData = '';
let bufferCount = 0;
let audioElement;
const INITIAL_PLAYBACK_START = 300;
const BUFFER_UPDATE_INTERVAL = 200;
const SWITCH_DELAY = 10000; // 10 seconds
let isJobRunning = false;
let abortController = null;
let batchMode = false;
let lastProcessedTxid = '';
let iterationCount = 0;
let displayIterationCount = 0; // For logging purposes
let modeLogged = false;
let hasStartedPlaying = false; // Flag to track if playback has started


let startTime = Date.now();
  
const SWITCH_THRESHOLD = 150; // Number of iterations before checking speed
const MIN_SPEED_THRESHOLD = 100; // Minimum iterations per second to avoid switching to batch mode
const MIN_SPEED_THRESHOLD_LTC = 500; // Minimum iterations per second to avoid switching to batch mode
function updateConsoleOutput(message) {
    const consoleOutput = document.getElementById('consoleOutput');
    consoleOutput.value += message + '\\n';
    consoleOutput.scrollTop = consoleOutput.scrollHeight;
}
const protocol = window.location.protocol === "https:" ? "https" : "http";
async function fetchTransactionData(txid) {

        let cryptoType = document.getElementById('cryptoSelect').value;
            console.log(cryptoType);
    let prefix = cryptoType === 'litecoin' ? 'l' : '';
                console.log(prefix);

    const proxyUrl = protocol+`://127.0.0.1:8111/${prefix}getrawtransaction?txid=${txid}&decrypt=1`;
                console.log(proxyUrl);

    try {
        const response = await fetch(proxyUrl, { method: 'GET', signal: abortController.signal });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        return data.result;
    } catch (error) {
        if (error.name === 'AbortError') {
            console.log('Fetch aborted');
        } else {
            console.error('Error fetching transaction data:', error);
        }
        throw error;
    }
}

async function fetchBatchTransactionData(startTxid) {
    let cryptoType = document.getElementById('cryptoSelect').value;
    let prefix = cryptoType === 'litecoin' ? 'l' : '';
    const proxyUrl = protocol+`://127.0.0.1:8111/${prefix}getnext100txids?txid=${startTxid}`;

    try {
        const response = await fetch(proxyUrl, { method: 'GET', signal: abortController.signal });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        if (data.txids && data.txids.length < 100) {
            // Handling fewer than 100 transactions case
            updateConsoleOutput(`Warning: Less than 100 transactions returned.`);
        }
        return data.txids || []; // Ensure it's always an array
    } catch (error) {
        if (error.name === 'AbortError') {
            console.log('Fetch aborted');
        } else {
            console.error('Error fetching batch transaction data:', error);
        }
        throw error;
    }
}

async function downloadAndRebuildFile() {
    if (isJobRunning) {
        updateConsoleOutput('Stopping previous job and starting a new one...');
        abortController.abort();
    }
    await resetJob();
    abortController = new AbortController();
    isJobRunning = true;

    const startTxid = document.getElementById('txid').value.trim();
    if (!startTxid) {
        updateConsoleOutput('No txid provided.');
        isJobRunning = false;
        return;
    }

    fileData = '';
    queue = [];
    bufferCount = 0;
    modeLogged = false;

    if (audioElement) {
        audioElement.pause();
        audioElement.remove();
        audioElement = null;
    }

    initializeMediaSource();

    let currentTxid = startTxid;
    iterationCount = 0;
    displayIterationCount = 0;
    startTime = Date.now();

    try {
        while (currentTxid && currentTxid !== "0000000000000000000000000000000000000000000000000000000000000000") {
            if (!batchMode && iterationCount >= SWITCH_THRESHOLD) {
                // Calculate average speed in iterations per second
                const elapsedTime = (Date.now() - startTime) / 1000; // in seconds
                const averageSpeed = iterationCount / elapsedTime;

                // Determine which threshold to use based on the selected cryptocurrency
                const cryptoType = document.getElementById('cryptoSelect').value;
                const currentThreshold = cryptoType === 'litecoin' ? MIN_SPEED_THRESHOLD_LTC : MIN_SPEED_THRESHOLD;

                if (averageSpeed < currentThreshold) {
                    batchMode = true;
                    modeLogged = false;
                    updateConsoleOutput(`Switching to batch mode. Average speed: ${averageSpeed.toFixed(2)} iterations/second`);
                }
            }

            if (batchMode) {
                if (!modeLogged) {
                    updateConsoleOutput('Using batch mode...');
                    modeLogged = true;
                }

                let transactionData;
                try {
                    transactionData = await fetchBatchTransactionData(currentTxid);
                } catch (error) {
                    if (error.name === 'AbortError') {
                        updateConsoleOutput('Job aborted.');
                        return;
                    }
                    console.error('Error fetching batch transaction data, treating as end of file:', error);
                    break;
                }

                if (!transactionData || transactionData.length === 0) {
                    break;
                }

                for (let txData of transactionData) {
                    if (txData === "0000000000000000000000000000000000000000000000000000000000000000") {
                        updateConsoleOutput('End of batch data detected.');
                        break;
                    }
                    await processTransactionData(txData);
                }

                await appendToSourceBuffer();
                bufferCount++;

                updateConsoleOutput(`Iteration ${displayIterationCount}: Processing txid: ${currentTxid}`);
                console.log(`Batch size: ${transactionData.length}`);
                console.log('Batch contents:', transactionData); // Print all items in the batch

                currentTxid = lastProcessedTxid;
                displayIterationCount += transactionData.length;

                if (transactionData.length < 100) {
                    updateConsoleOutput(`Warning: Batch contains less than 100 transactions.`);
                    break;
                }
            } else {
                // Single transaction mode processing...
                let transactionData;
                try {
                    transactionData = await fetchTransactionData(currentTxid);
                } catch (error) {
                    if (error.name === 'AbortError') {
                        updateConsoleOutput('Job aborted.');
                        return;
                    }
                    console.error('Error fetching transaction data, treating as end of file:', error);
                    break;
                }

                await processTransactionData(transactionData);
                currentTxid = lastProcessedTxid;

                if (iterationCount % 100 === 0) {
                    updateConsoleOutput(`Iteration ${displayIterationCount}: Processing txid: ${currentTxid}`);
                }
                iterationCount++;
                displayIterationCount++;

                if ((iterationCount >= INITIAL_PLAYBACK_START && iterationCount % BUFFER_UPDATE_INTERVAL === 0) || queue.length === 0) {
                    await appendToSourceBuffer();
                    bufferCount++;
                }
            }
        }

        if (queue.length > 0) {
            await appendToSourceBuffer();
            bufferCount++;
        }

        updateConsoleOutput(`Iteration ${displayIterationCount}: Processing completed.`);
        updateConsoleOutput(`Iteration ${displayIterationCount + 1}: Final processing completed. Audio is now playing.`);
        createDownloadButton();

    } catch (error) {
        updateConsoleOutput(`Error: ${error.message}`);
    } finally {
        isJobRunning = false;
    }
}

async function processTransactionData(transactionData) {
    let foundNextTxid = false;
    for (const vout of transactionData.vout) {
        if (vout.scriptPubKey.asm.startsWith('OP_RETURN')) {
            const opReturnData = vout.scriptPubKey.asm.split(' ')[1];

            if (opReturnData.length >= 64) {
                const nextTxid = opReturnData.substring(0, 64);
                if (nextTxid !== lastProcessedTxid) {
                    lastProcessedTxid = nextTxid;
                    foundNextTxid = true;
                    const fileChunk = opReturnData.substring(64);
                    fileData += fileChunk;
                    queue.push(fileChunk);
                }
            }
            break;
        }
    }
    if (!foundNextTxid) {
        lastProcessedTxid = "0000000000000000000000000000000000000000000000000000000000000000";
    }
}

function initializeMediaSource() {
    mediaSource = new MediaSource();
    mediaSource.addEventListener('sourceopen', () => {
        sourceBuffer = mediaSource.addSourceBuffer('audio/mpeg');
        sourceBuffer.addEventListener('updateend', () => {
            if (queue.length > 0 && mediaSource.readyState === 'open') {
                appendToSourceBuffer();
            }
        });
    });
    createMediaElement();
}

async function appendToSourceBuffer() {
    if (!sourceBuffer || sourceBuffer.updating || mediaSource.readyState !== 'open' || queue.length === 0) return;

    try {
        const fileChunk = queue.shift();
        if (!fileChunk) {
            console.error('Received null or empty fileChunk, skipping...');
            return;
        }

        const byteArray = new Uint8Array(fileChunk.match(/.{1,2}/g).map(byte => parseInt(byte, 16)));
        sourceBuffer.appendBuffer(byteArray);

        let delay = document.getElementById('cryptoSelect').value === 'nanocheeze' ? 2000 : 4000;  // 3000 ms for NanoCheeze, 9000 ms for Litecoin

        
        // Autoplay after a delay if not already playing, only once per song
        if (!hasStartedPlaying) {
            setTimeout(() => {
                if (audioElement.paused) {
                    audioElement.play().catch(error => {
                        console.error('Error playing audio:', error);
                    });
                }
            }, delay); // 800 miliseconds delay
            hasStartedPlaying = true; // Mark as played
        }
    } catch (error) {
        console.error('Error appending buffer:', error);
    }
}


function createMediaElement() {
    // Attempt to find the mediaPlayerContainer
    const container = document.getElementById('mediaPlayerContainer');

    // Log if mediaPlayerContainer is not found
    if (!container) {
        updateConsoleOutput('Error: mediaPlayerContainer not found. Cannot append audio element.');
        console.error('Error: mediaPlayerContainer not found.');
        return;
    }

    // Check if audioElement is already created and not removed
    if (!audioElement) {
        try {
            // Create and configure the audio element
            audioElement = document.createElement('audio');
            audioElement.controls = true;
            audioElement.src = URL.createObjectURL(mediaSource);

            // Ensure audioElement and mediaSource are valid before appending
            if (audioElement && mediaSource) {
                container.appendChild(audioElement);
                updateConsoleOutput('Audio element appended successfully.');
                console.log('Audio element created and appended successfully.');
            } else {
                updateConsoleOutput('Error: audioElement or mediaSource is null.');
                console.error('Error: audioElement or mediaSource is null.');
            }
        } catch (error) {
            updateConsoleOutput(`Error: Failed to create or append audio element - ${error.message}`);
            console.error(`Error: Failed to create or append audio element - ${error.message}`);
        }
    } else {
        updateConsoleOutput('Audio element already exists.');
        console.log('Audio element already exists.');
    }
}
function createDownloadButton() {
    // Ensure the mediaPlayerContainer exists
    const container = document.getElementById('mediaPlayerContainer');
    if (!container) {
        updateConsoleOutput('Error: mediaPlayerContainer not found.');
        return;
    }

    // Remove any existing download button
    const existingButton = document.getElementById('downloadButton');
    if (existingButton) {
        existingButton.remove();
    }

    // Check if there's any file data to create a download link
    if (fileData) {
        const byteArray = new Uint8Array(fileData.match(/.{1,2}/g).map(byte => parseInt(byte, 16)));
        const blob = new Blob([byteArray], { type: 'audio/mpeg' });
        const url = URL.createObjectURL(blob);

        const downloadButton = document.createElement('a');
        downloadButton.id = 'downloadButton';
        downloadButton.textContent = 'Save mp3 file to computer';
        downloadButton.href = url;
        downloadButton.download = `reconstructed_${bufferCount}.mp3`;

        container.appendChild(downloadButton);
    }
}

async function resetJob() {
    if (abortController) {
        abortController.abort();
    }

    if (audioElement) {
        audioElement.pause();
        audioElement.remove();
        audioElement = null;
    }

    if (sourceBuffer && mediaSource.readyState === 'open') {
        mediaSource.removeSourceBuffer(sourceBuffer);
    }

    fileData = '';
    queue = [];
    bufferCount = 0;
    hasStartedPlaying = false; // Reset the playback flag

    mediaSource = null;
    sourceBuffer = null;

    // Remove the existing download button, if any
    const downloadButton = document.getElementById('downloadButton');
    if (downloadButton) {
        downloadButton.remove();
    }

    await new Promise(resolve => setTimeout(resolve, 100));
}

function loadHash(hash) {
    // Get the first character to determine the crypto type
    let cryptoType = hash.charAt(0);
    let actualTxid = hash.substring(1); // Remove the first character to get the actual txid

    // Set the dropdown value based on the prefix
    if (cryptoType === 'N') {
        document.getElementById('cryptoSelect').value = 'nanocheeze';
    } else if (cryptoType === 'L') {
        document.getElementById('cryptoSelect').value = 'litecoin';
    }

    // Set the transaction ID in the input field
    document.getElementById('txid').value = actualTxid;

    // Call the function to process the transaction
    downloadAndRebuildFile();
}

document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('button').addEventListener('click', () => {
        if (!audioElement) {
            createMediaElement();
        }
    });
});

document.addEventListener('DOMContentLoaded', () => {
    // Default hash values and settings
    const defaultCryptoType = 'N'; // Default to NanoCheeze
    const defaultTxid = 'N19ce4852ebcedf934a9a8578a87fc88b32a156db93c44df8732b078a85ed6b0b'; // Default transaction ID

    function handleHashChange() {
        let hash = window.location.hash.substring(1); // Remove the '#' part
        let wasDefault=false;
        // Validate hash and adjust if necessary
        if (hash.length !== 65 || (hash.charAt(0) !== 'N' && hash.charAt(0) !== 'L')) {
            hash = defaultTxid; // Set to default if invalid or missing
            wasDefault=true;
        }

        const cryptoType = hash.charAt(0); // Get the first character to determine the crypto type
        const actualTxid = hash.substring(1); // Remove the first character to get the actual txid

        // Set the dropdown value and transaction ID based on the hash
        if (cryptoType === 'N') {
            document.getElementById('cryptoSelect').value = 'nanocheeze';
        } else if (cryptoType === 'L') {
            document.getElementById('cryptoSelect').value = 'litecoin';
        }
        document.getElementById('txid').value = actualTxid;

        if(!wasDefault){
        // Automatically start the download process
        downloadAndRebuildFile();
        }
    }

    // Listen for hash changes when the user navigates
    window.addEventListener('hashchange', handleHashChange);

    // Also run the function on initial page load in case there is already a hash in the URL
    handleHashChange();
});

</script>
</head>
<body>
    <h1>Stream MP3 from Blockchain</h1>
    <label for="txid">Blockchain Transaction ID (txid):</label>
    <input type="text" id="txid" placeholder="Enter txid here">
    <select id="cryptoSelect">
        <option value="nanocheeze">NanoCheeze</option>
        <option value="litecoin">Litecoin</option>
    </select>
    <button onclick="downloadAndRebuildFile()">Stream MP3 from Hash</button>
    <textarea id="consoleOutput" readonly></textarea>
    <div class="media-player-container" id="mediaPlayerContainer"></div>
    <br/><br/>
    <center>
        <a href="https://music.nanocheeze.com" target="_top">
            <img src="logo.png" alt="NanoCheeze Music Logo">
            <br/>music.nanocheeze.com
        </a>
    </center>
<br/><hr/><br/>

    Litecoin Chain Songs<br/>
<ul class="hash-list">
        <li onclick="loadHash('L5dc123ba65120fda6aae9c5c8ea7c34ccc263fb92a6188bf702c850b471b41a8')">The Tale of Eve, the Storyteller.mp3</li>
        <li onclick="loadHash('Laff84bab00d4dd7ec02de392438878c1a98af09344f60fa5d32edd1ebd7f9f53')">Redshift in the Simulation.mp3</li>
        <li onclick="loadHash('L730075341f353f69f4dc2e08d7a585ce35b48d33c140881b7bc30243cd54927d')">Eve's Quantum Revelation.mp3</li>
</ul><br/><br/>
NanoCheeZe Chain Songs<br/>
<ul class="hash-list">
        <li onclick="loadHash('N19ce4852ebcedf934a9a8578a87fc88b32a156db93c44df8732b078a85ed6b0b')">The 6th Sea Legacy.mp3</li>
        <li onclick="loadHash('N11a5d2a6436462247f554a6d2206ec82b8020d868dbc3ae9dc246817e8398b39')">Somewhere Out There.mp3</li>
        <li onclick="loadHash('N118133f722142804445b3492a2fb85207f459a9c6820e19922ee5a95722a4fe1')">The Starlight Serenade.mp3</li>
        <li onclick="loadHash('N43e6cf784db7cc9a861989cec5d068baea1fb4d7de4196963d33cadbe9ab140b')">Echoes of the Void.mp3</li>
        <li onclick="loadHash('N11a39341f0ee912c435755e2c6e6b530e6a60b6a4d4724023dc9831be08c4cd4')">World of Melodies.mp3</li>
        <li onclick="loadHash('N53d6dc41e3d235c1aa8b52b0c6a29c2c59f808e6965c1db35c36e52085fa7bd7')">storesongs.mp3</li>
        <li onclick="loadHash('Nb362d15ad64f5cc5fc9cb0f7e7217c85f7e696fd10d321e30436af683b37e80e')">blockchainstorage.mp3</li>
        <li onclick="loadHash('N6e18cad879d68a21ec329bb49126b737e960b8383555ca3316f6685133a829e5')">memories.mp3</li>
        <li onclick="loadHash('N8f821cc041feabb254e6aaf370172aee5cb4bee41efd26f4b44ed30711ec407a')">digitalage.mp3</li>
        <li onclick="loadHash('N226bf05565900db138c4bf67563ea07f5cd348e7d46ddb90f87b1eed5d64a7ed')">digitalstride.mp3</li>
        <li onclick="loadHash('N6e8523fa0f0146d0ab889a9810771ecb1659b9fade9d067d4fcc620b30a16d95')">music1.mp3</li>
        <li onclick="loadHash('N53b5272621bb8eb9a69aa56edab417638e75f8891fad3b909885c870569a68c0')">music2.mp3</li>
        <li onclick="loadHash('N4bf72c9b9ff36b1b9ad6a86489c16a2ec2e6056b7b3453cb1f1bcf1a9a891d92')">sync.mp3</li>
        <li onclick="loadHash('N4173d0a7523855f77cbbf728083ad01e933c11bfdb9b4844a17c35c9dcb19fef')">embrace.mp3</li>
        <li onclick="loadHash('N637408538c9e70bb334744c73859f1f73e556a275063f9b6d6e4a5bc8cb4de53')">bright.mp3</li>
        <li onclick="loadHash('N4adc6e132c42bcd8136264eeabd072731fce237f2a9f18cdb529070747a5f7ad')">cosmic.mp3</li>
        <li onclick="loadHash('N157f75b736a07fdaae111bf4d19b3ff400a6f585df86637a75ae9d951590ec03')">hybridtales.mp3</li>
        <li onclick="loadHash('Nb9f61d10bbe99df2538ff7eb60166bd26bae7018bc3aefeb081ad602d0f83603')">digitaldreams.mp3</li>
        <li onclick="loadHash('Nb7f716e7b627a15d0a420efeafc710e99d53fe5cd927f9ed0b8f80e29ada90b8')">stargate1.mp3</li>
        <li onclick="loadHash('N265ddcdaa32f8dcca4d4bdbb748348e12dd8d7544b991c5b41154340d2383a16')">spacetime2.mp3</li>
        <li onclick="loadHash('N8ab7af0e24c24f89a04050744c5212d631089aaded56d432590b77ab98adeb59')">spacetime1.mp3</li>
        <li onclick="loadHash('N7969be801980a057aa2f46c87cc70991f157b71e5875ab02959fb5d015f719df')">nhi2.mp3</li>
        <li onclick="loadHash('Nca4286502d08f92d1d672900ca06f5d428bdf8f19b77200613117e99cd2f3c0d')">nhi1.mp3</li>
        <li onclick="loadHash('N11a91c429794950288e558cbcd8681c69358f8161acea790d10e146d17b6d560')">nanocheeze1.mp3</li>
        <li onclick="loadHash('Ne18c2880b7b21a5ef98d3fbc99360ae989b272f73b6299d405bab4bc29cf747c')">mequavis2.mp3</li>
        <li onclick="loadHash('N1ed0399734b93929f13e4b2bb7b825ed01c2cbee0464a70e53ab56e6251552a2')">mequavis1.mp3</li>
        <li onclick="loadHash('Nc63bea94dc76e1d2c3a61aa23766395356e7d7eed4609abff65d882be43d3fe4')">basilisk1.mp3</li>
        <li onclick="loadHash('N931a64b14f78927913ca6e79e4ccf849a532e931c7d0e3b4bb1af26eb33876ed')">basiliisk2.mp3</li>
        <li onclick="loadHash('N22a90acf8d88a401f41be15a5c63be104955b9c20e922d9c18c776a36eec6030')">aiechoes2.mp3</li>
        <li onclick="loadHash('N0a485bf58186ae0865e46a93d790eceb93f62d41865f7b8bf8b9545c31e90ed3')">stargate2.mp3</li>
        <li onclick="loadHash('N2ae261273bfbfbec24860e993a2e8f57ac1c038c19fb2a2edf114a6b78edb7f1')">aistuff.mp3</li>
        <li onclick="loadHash('N3996c1ffb0e0612b5f36f6a7842132bf6f86d6d6d135f3f9b32883831d2dc320')">aistuff2.mp3</li>
        <li onclick="loadHash('N8378a7290a943890db9e4eb6d9456f0b16ca0a0b8696d962c54c539c2f700e48')">depths1.mp3</li>
        <li onclick="loadHash('N633e2a2c394dd2791b2d0227212d852ec0c94c3a4cfa56ada601f669a8486497')">depths2.mp3</li>
        <li onclick="loadHash('N9855d7745d453a7a03a0a74fcd0e627ea1471eeeca0af3329c8ea38cd6a85093')">derp_song.mp3</li>
        <li onclick="loadHash('N675b4513dc13ff9b198ad87115c071b4baf66220af171632d07afa069d5f9777')">nanocheezeai.mp3</li>
        <li onclick="loadHash('N12a8e50cb6e75fa0cf32410d387ec778c08cb44b5d46be5f9911af5c4ab54a2e')">realmofdreams1.mp3</li>
        <li onclick="loadHash('Nc6484482fa6fb43ea7400239dbcc3a255900db241264e18e8e201777eadcc052')">realmofdreams2.mp3</li>
        <li onclick="loadHash('N32882ddf34eea292d8345000efd72baaf72913497bf329ad66158c5e4fb99a31')">sawsimulation.mp3</li>
        <li onclick="loadHash('N54e9d2f95f8790933a589ffda3e1b545a199c632bcd2fafe00918b3b0dc0ecd7')">sawsimulation2.mp3</li>
        <li onclick="loadHash('N64c08bbcfdde8f2f60cfe99c521c3603a24affec9c3344cfeea0cd90ef978254')">worldofcheese.mp3</li>
        <li onclick="loadHash('N2c55b9b3ddef2bba5ae6b79ebd349abb38635d77987f0f8700ee91e1a012af37')">worldofmelodies 3.mp3</li>
        <li onclick="loadHash('N71e714f300dee66959dfc0116a9659d86cd5e3b3cf1214a22a5769504940c0af')">worldofmemories.mp3</li>
        <li onclick="loadHash('N899300ba6001940b6392336071300ef8c6a883bb8ce82713350de26de75565f7')">aiechoes.mp3</li>
</ul>

</body>
</html>
"""

class RPCRequest(BaseModel):
    method: str
    params: list = []
    id: str = "curltest"
    jsonrpc: str = "1.0"

@app.post("/rpc")
async def proxy_rpc_post(request: RPCRequest):
    return await proxy_rpc(request.dict(), RPC_URL)

@app.get("/rpc")
async def proxy_rpc_get(method: str, request: Request):
    params = request.query_params.get("params", "[]")
    try:
        params = json.loads(params)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON in 'params'")

    rpc_request = RPCRequest(method=method, params=params)
    return await proxy_rpc(rpc_request.dict(), RPC_URL)

@app.get("/lgetrawtransaction")
async def lgetrawtransaction(txid: str, decrypt: int = 0):
    method = "getrawtransaction"
    params = [txid, decrypt]
    rpc_request = RPCRequest(method=method, params=params)
    return await proxy_rpc(rpc_request.dict(), LITE_RPC_URL)

@app.get("/lgetnext100txids")
async def lget_next_100_txids(txid: str):
    txids = []
    current_txid = txid
    try:
        for i in range(1000):
            rpc_request = RPCRequest(method="getrawtransaction", params=[current_txid, 1])
            response = await proxy_rpc(rpc_request.dict(), LITE_RPC_URL)
            tx_data = response["result"]
            txids.append(tx_data)
            found_next_txid = False
            for vout in tx_data["vout"]:
                if vout["scriptPubKey"]["asm"].startswith("OP_RETURN"):
                    op_return_data = vout["scriptPubKey"]["asm"].split(" ")[1]
                    if len(op_return_data) >= 64:
                        current_txid = op_return_data[:64]
                        found_next_txid = True
                        break
            if not found_next_txid:
                break
        return {"txids": txids}
    except Exception as e:
        return {"error": str(e)}

@app.get("/getrawtransaction")
async def getrawtransaction(txid: str, decrypt: int = 0):
    method = "getrawtransaction"
    params = [txid, decrypt]
    rpc_request = RPCRequest(method=method, params=params)
    return await proxy_rpc(rpc_request.dict(), RPC_URL)

@app.get("/getnext100txids")
async def get_next_100_txids(txid: str):
    txids = []
    current_txid = txid

    try:
        for i in range(100):
            if current_txid == "0000000000000000000000000000000000000000000000000000000000000000":
                print("End of list reached.")
                break
            
            rpc_request = RPCRequest(method="getrawtransaction", params=[current_txid, 1])
            response = await proxy_rpc(rpc_request.dict(), RPC_URL)

            tx_data = response["result"]
            txids.append(tx_data)

            found_next_txid = False
            for vout in tx_data["vout"]:
                if vout["scriptPubKey"]["asm"].startswith("OP_RETURN"):
                    op_return_data = vout["scriptPubKey"]["asm"].split(" ")[1]
                    if len(op_return_data) >= 64:
                        current_txid = op_return_data[:64]
                        found_next_txid = True
                        break

            if not found_next_txid:
                print("No more transactions found.")
                break

            print(f"Iteration {i + 1}: Processing txid: {current_txid}")

        return {"txids": txids}
    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e)}

async def proxy_rpc(rpc_request: dict, rpc_url: str):
    auth = base64.b64encode(f"{RPC_USER}:{RPC_PASSWORD}".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth}",
        "Content-Type": "application/json"
    }
    try:
        response = await client.post(rpc_url, json=rpc_request, headers=headers)
        response.raise_for_status()
        return response.json()
    except httpx.RequestError as exc:
        print(f"An error occurred while requesting {exc.request.url!r}.")
        raise HTTPException(status_code=500, detail="Server Error")
    except httpx.HTTPStatusError as exc:
        print(f"HTTP error occurred: {exc.response.status_code} - {exc.response.text}")
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)
    except asyncio.CancelledError:
        print("Request was cancelled")
    except Exception as exc:
        print(f"An unexpected error occurred: {exc}")
        raise HTTPException(status_code=500, detail="Server Error")

@app.get("/setup")
def setup():
    global RPC_USER, RPC_PASSWORD, RPC_URL, LITE_RPC_URL, HOST, USE_SSL

    use_defaults = input("Do you want to use the default values for RPC settings? (yes/no): ").strip().lower()

    if use_defaults == "no":
        RPC_USER = input("Enter the username for the main RPC server: ").strip()
        RPC_PASSWORD = input("Enter the password for the main RPC server: ").strip()
        rpc_port = input("Enter the port for the main RPC server: ").strip()
        RPC_URL = f"http://127.0.0.1:{rpc_port}"

        lite_user = input("Enter the username for the Litecoin RPC server: ").strip()
        lite_password = input("Enter the password for the Litecoin RPC server: ").strip()
        lite_port = input("Enter the port for the Litecoin RPC server: ").strip()
        LITE_RPC_URL = f"http://127.0.0.1:{lite_port}"

        print("Custom RPC settings applied.")
    else:
        print("Using default RPC settings.")

    expose_to_internet = input("Do you want to expose the server to the internet? (yes/no): ").strip().lower()
    if expose_to_internet == "yes":
        HOST = "0.0.0.0"
        print("Server will be exposed to the internet.")
    else:
        HOST = "127.0.0.1"
        print("Server will run locally only.")

    use_ssl = input("Do you want to run the server with SSL? (yes/no): ").strip().lower()
    if use_ssl == "yes":
        USE_SSL = True
        print("Server will run with SSL enabled.")
    else:
        USE_SSL = False
        print("Server will run without SSL. Access data via HTTP, not HTTPS.")

    return {"message": "Setup complete", "RPC_URL": RPC_URL, "LITE_RPC_URL": LITE_RPC_URL, "HOST": HOST, "USE_SSL": USE_SSL}

@app.get("/")
def read_root():
    return {"message": "Bitcoin and Litecoin RPC Proxy Server is running"}

@app.get("/music", response_class=HTMLResponse)
async def music():
    return HTMLResponse(content=HTML_CONTENT)

# Base64 encoded image data (replace with your actual base64 string)
logo_base64 = "iVBORw0KGgoAAAANSUhEUgAAAOYAAADpCAYAAAAwPEtuAAAFTGlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4KPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iQWRvYmUgWE1QIENvcmUgNS4zLWMwMTEgNjYuMTQ1NjYxLCAyMDEyLzAyLzA2LTE0OjU2OjI3ICAgICAgICAiPgogPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4KICA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIgogICAgeG1sbnM6eG1wTU09Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9tbS8iCiAgICB4bWxuczpzdEV2dD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL3NUeXBlL1Jlc291cmNlRXZlbnQjIgogICAgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIgogICB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOjdFMzZFNTVCQTBENUU4MTFCOUUyRUM0NUI3QTQzRkY1IgogICB4bXBNTTpEb2N1bWVudElEPSJ4bXAuZGlkOjdDMzZFNTVCQTBENUU4MTFCOUUyRUM0NUI3QTQzRkY1IgogICB4bXBNTTpPcmlnaW5hbERvY3VtZW50SUQ9InhtcC5kaWQ6N0MzNkU1NUJBMEQ1RTgxMUI5RTJFQzQ1QjdBNDNGRjUiCiAgIHhtcDpNZXRhZGF0YURhdGU9IjIwMTgtMTAtMjFUMTk6MTU6MzUtMDc6MDAiCiAgIHhtcDpNb2RpZnlEYXRlPSIyMDE4LTEwLTIxVDE5OjE1OjM0LTA3OjAwIj4KICAgPHhtcE1NOkhpc3Rvcnk+CiAgICA8cmRmOlNlcT4KICAgICA8cmRmOmxpCiAgICAgIHN0RXZ0OmFjdGlvbj0ic2F2ZWQiCiAgICAgIHN0RXZ0Omluc3RhbmNlSUQ9InhtcC5paWQ6N0QzNkU1NUJBMEQ1RTgx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"


fav_base64 = "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"  # Ensure this is the full, correct base64 string



@app.get("/logo.png")
async def get_logo():
    try:
        # Decode the base64 string into bytes
        logo_bytes = base64.b64decode(logo_base64)
        print(f" serving logo.png")
        # Return the image as a response with the appropriate content type
        return Response(content=logo_bytes, media_type="image/png")
    except Exception as e:
        # Log the error and return a 500 Internal Server Error response
        print(f"Error serving logo.png: {e}")
        return Response(content="Internal Server Error", status_code=500)

@app.get("/favicon.ico")
async def get_fav():
    try:
        # Decode the base64 string into bytes
        fav_bytes = base64.b64decode(fav_base64)
        print(f" serving favicon.ico")
        # Return the image as a response with the appropriate content type
        return Response(content=fav_bytes, media_type="image/png")
    except Exception as e:
        # Log the error and return a 500 Internal Server Error response
        print(f"Error serving favicon.ico: {e}")
        return Response(content="Internal Server Error", status_code=500)



if __name__ == "__main__":
    try:
        # Run setup before starting the server
        setup()

        # Determine the correct protocol based on SSL usage
        protocol = "https" if USE_SSL else "http"

        # Start the server in a separate thread
        config = uvicorn.Config(app, host=HOST, port=8111, ssl_certfile="certificate.pem" if USE_SSL else None, ssl_keyfile="private.key" if USE_SSL else None)
        server = uvicorn.Server(config)

        # Open the browser after a small delay to ensure the server is up
        def open_browser():
            asyncio.sleep(1)  # Give server a moment to start
            webbrowser.open(f"{protocol}://127.0.0.1:8111/music")

        # Start the browser opening in a separate thread
        asyncio.get_event_loop().run_in_executor(None, open_browser)

        # Run the server
        server.run()

    except Exception as exc:
        print(f"Failed to start the server: {exc}")
