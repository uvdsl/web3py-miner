# Sleeping Miner (web3py) 

A little miner sleeping at work, written in python using the web3py Websocket or RPC interface for geth.

## Requirements
I used a conda environment with python 3.7:
```
pip install -r requirements.txt
```

## Usage
```
python miner.py [-h] [-e ENDPOINT] [-t THREADS]

optional arguments:
  -h, --help            show this help message and exit
  -e ENDPOINT, --endpoint ENDPOINT
                        Geth connection endpoint, default: ws://localhost:8546
  -t THREADS, --threads THREADS
                        Number of threads to mine with, default: 1
```
