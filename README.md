### Mini Distributed Ledger Midleware

This is a very initial attempt to create a simple DLT middleware software for managing af simple permissioned distributed ledger based on BlockChain

The program is still very much under development as I am trying to establish the different parts

* A protocol (currently missing)
* A Server/Client: Chainnode.py which establishes a listening/requesting node. Currently only receives a signal and sends to other nodes in the network.
* A blockchain : blockchain.py (supported by blockchain.db)
* An Interface : CLI.py for communicating with the nodes.
* A smart contract interface (currently missing)
* A Concensus mechanism (currently missing - see below)

I have a few proof-of-concept files for the following attributes:

* Crypto.py which demonstrates how to use ECSDA module for signing messages
* SSLclient.py and SSLserver.py which demonstrates an encrypted communication based on certificates

The two proof-of-concepts above will in concert support that Nodes can communicate encrypted and that nodes can sign their communication so recipient nodes can verify it's origin.

#### Quick start - DLT Nodes

You can start the nodes by running

`python3.6 chainnode.py <config file> <node number>`

I have prepared a very simple configuration file to test a simple 3 node network. So you would need to start up three consoles where for each you would do:

`python3.6 chainnode.py chainnodeconfig.yml 0` (for node 0)

`python3.6 chainnode.py chainnodeconfig.yml 1` (for node 1)

`python3.6 chainnode.py chainnodeconfig.yml 2` (for node 2)

Then you have to start a fourth console

`python3.6 cli.py`

In the CLI you can send commands. The CLI will as a starting point send any command to localhost port 3301 which Node 0 listens to. When a Node receives an input from the CLI it will re-send the message to the other nodes on the network. Each Node recieving from a member node will just output a message.

If you want to send a message to Node 1 you have to write to another port. This is done by writing

`>>Command:<portnumber>,<message>`

Node 1 listens to port 3411 and Node 2 listens to 3421 (refer to chainnodeconfig.yml file to see all port configurations). After having send to a new port CLI remembers this as new port for all communication and will use this until you switch to a new port - by inserting new port number before the message separated by comma.

You can close down a port via the "stop" command

`>>Command:3401,stop`

will close down node0. It may take a few seconds to time-out all running threads - before the node fully closes down.

#### Quick start - Blockchain

The second part which is currently being developed is the blockchain. Data is stored in an SQLITE3 DB - unencrypted in the current version - but all data is hashed in order to achieve integrity of data. You run the blockchaintest example like this:

`python3.6 blockchaintest.py`

This program is rather messy at the current stage and actually only runs a few steps in __standard__. You should get the following output

```
Blocks Loaded 101 from DB block01 (max index=100)
Time elapsed: 0:00:00.000001
None
{
    "hash": "9be962968890a4773df0fa7bc8fa8b3ea29b1b311a84d88262483563997cd342",
    "block": {
        "idx": 100,
        "nounce": 0,
        "created": "2018-01-28 14:58:16.027429",
        "previous": "adb7534768a9777f116d8e3bcbbc6f44ace43f0118effb1bd84d566eb52f60e5",
        "content": {
            "price": 23,
            "volume": 3200,
            "ISIN": "e267d8127b4728602033da32e7dd566fbe3154085d95c4dd9b81aa0a41349089",
            "seller": "d0ae0ca6997450993de4a64a2a6b9b1f486c30ac5071830a6bb5beabdf5f7051",
            "buyer": "f9503391d6cd2b8c24574c1751423f1ae9d19fefff4c0ea621bee4a85e8fed16"
        }
    }
}
```

Which basically informs you that blockchain is loaded (101 blocks in memory cache). The chain totals 101 blocks and the last block is printed for inspection. In the content is created a dummy transactions - with a trade of 3200 units at the price of 23 - between a seller and buyer - based on a security which is identified by it's hashed ISIN-code. Seller, buyer and ISIN are all SHA256 hashed.

You can do a number of things on the blockchain object as is - but I will not document it here. For those who are interested you can look into the code and try some of the other code in theres which is currently excluded under __if FALSE__ clauses.

#### Concensus mechanism

This mini DLT is supposed to be a permissioned DLT - that is users will be authenticated and thereby trusted. Specific roles will be assigned to Nodes so some nodes will act as endorsers, while others will have a special role of define exact order of new blocks. This follows the Hyperledger Fabrics architecture where the network is composed of PEERS (endorsers) and ORDERER (which finanlize the order of new blocks)

I am also considering the following concensus mechanism:

1) A new transaction is send to network
2) Recipient Node - sends the transaction to all other nodes.
3) All nodes verifies the transaction
4) If the transaction checks out - the Node informs all other nodes on this
5) All nodes collect acceptance for all nodes
6) When a node has recieved acceptence from all nodes it sends a message to all nodes that it has received full verification
7) All nodes receives full verification from other nodes

At this stage then

a) all nodes has verified the transaction. (own verification)
b) all nodes knows that all other nodes has accepted the transaction (full agreement on transaction)
c) all nodes know that all other nodes knows that all nodes has accepted the transaction (full concent)

Therefore all can attach the block to it's blockchain

I am not sure if this works - obviously this protocol/concensus is rather strict. If a single signal miss out - the transaction is dumped.
