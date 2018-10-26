import hashlib as hasher
import datetime as date
import json
import random
from blockchaindb import *

"""
# SIMPLE BLOCKCHAIN EXAMPLE

 Set BlockSize or timeout before nextblock is submitted

 Simple change here from WS

"""

PoW = 0

def hashIt(text):
    sha = hasher.sha256()
    sha.update(text.encode("utf-8"))
    return sha.hexdigest()

def recordToBlock(blockrec,prev=None):
    if blockrec is None:
        return None
    blockdata = json.loads(blockrec["block"])
    newblock = CryptoBlock(**blockdata)
    if blockrec["hash"]!=newblock.hash:
        print("ERROR - failed hash integrity - Block with index {} and hash {}".format(blockrec["idx"],blockrec["hash"]))
        return None
    if  prev is not None:
        if prev.hash != newblock.previous:
            print(prev)
            print(newblock)
            print("ERROR - failed chain integrity - Block with index {} and hash {}".format(blockrec["idx"],blockrec["hash"]))
            return None
    return newblock


class CryptoBlock:

    def __init__(self,idx=0,nounce=0,created=date.datetime.now(),previous=0,content=eval("{'name':'genesis'}")):
        self.index = idx
        self.content = content
        self.nounce = nounce
        self.created= created
        self.previous = previous
        self.hash = self._internalHash()

    def getBlock(self):
        return {"idx":self.index,"nounce":self.nounce,"created":self.created,"previous":self.previous,"content":self.content}


    def __str__(self):
        return json.dumps({"hash":self.hash,"block":self.getBlock()},default=str,sort_keys=False,indent=4)

    def _internalHash(self):
        sha = hasher.sha256()
        sha.update(self.cleanString())
        return sha.hexdigest()

    def cleanString(self):
        return (str(self.nounce)+str(self.index)+str(self.created)+str(self.previous)+str(self.content)).encode('utf-8')

    def setnounce(self,nounce):
        self.nounce = nounce
        self.hash = self._internalHash()

    def checkIntegrity(self):
        return self.hash == self._internalHash()

    def compare(self,anotherBlock):
        if not anotherBlock.checkIntegrity(): return False
        if not self.checkIntegrity(): return False
        if self.hash != anotherBlock.hash: return False
        return True

    def getRecord(self):
        #return {"idx":1,"hash":"hjh","created":000,"block":"jkjk"}
        return {"idx":self.index,"hash":self.hash,"created":self.created,"block":json.dumps(self.getBlock(),default=str)}

    def getRecordClean(self):
        #return {"idx":1,"hash":"hjh","created":000,"block":"jkjk"}
        return {"idx":self.index,"hash":self.hash,"created":self.created,"block":self.getBlock()}


class BlockChain:

    def __init__(self,db="blockchain"):
        self.blocks = []
        self.storage = BlockChainStorage(db)
        self.basename = db
        self.blocks = []
        self.getLastBlocks(1000)

    def __str__(self):
        return self.toJSON()

    def getLastBlocks(self,numberOfBlocks):
        blockrecs = self.storage.getNumberOfBlocks(numberOfBlocks)
        if len(blockrecs)>0:
            #print(blockrecs)
            prev = None
            for blockrec in blockrecs:
                block = recordToBlock(blockrec)
                if block is None:
                    self.blocks = []
                    return False
                self.blocks.append(block)
            print("Blocks Loaded {} from DB {} (max index={})".format(len(self.blocks), self.basename,self.getlastBlock().index))
            return True
        else:
            print("Blocks Loaded 0 - Genesis Block needs to be added")
            return False
            #genesis = CryptoBlock()
            #self.blocks = [genesis]
            #self.storage.addBlock(genesis)
            #else:

    def toJSON(self):
        return json.dumps(self.blocks,default=lambda a: eval(str(a)),indent=4,ensure_ascii=False)


    def checkIntegrityRange(self,start,steps,block=None):
        blockrecs = self.storage.getBlockRange(start,steps)
        #print("Doing from {} and {} steps".format(start,steps))
        for blockrec in blockrecs:
                block = recordToBlock(blockrec,block)
                if block is None: return False,None
        if len(blockrecs)< steps:
            return True,None
        return True,block


    def checkAll(self):
        idx = 0
        step = 100000
        flag,prev = self.checkIntegrityRange(idx,step)
        idx += step
        while flag and prev is not None:
            flag,prev = self.checkIntegrityRange(idx,step,prev)
            idx += step
        return flag

    def checkIntegrity(self):
        prev = self.blocks[0]
        for block in self.blocks[1:]:
            #check that hashes are ok
            if prev.hash != block.previous:
                #print(prev)
                #print(block)
                return False
            if not block.checkIntegrity():
                print("Stored Hash    :",block.hash)
                print("Calculated Hash:",block._internalHash())
                return False
            prev = block
        return True

    def compare(self,anotherBlock):
        #checking external
        if not anotherBlock.checkIntegrity():
            print("Other chains integrity breached")
            return False
        blockLength = len(anotherBlock.blocks)
        if blockLength == len(self.blocks):
            for x in range(blockLength):
                if not self.blocks[x].compare(anotherBlock.blocks[x]):
                    print ("Block {} does not match".format(x))
                    return False
            return True
        else:
            print("blocks not of same length")
            return False

    def getlastBlock(self):
        #lastkey = sorted(self.blocks.keys())[-1]
        #return self.blocks[lastkey]
        if len(self.blocks) == 0:
            return None
        else:
            return self.blocks[-1]

    def addBlock(self,newblock):
        # Assumed that business logic in data is check beforehand
        if newblock is None:
            print("new block was None and not added")
            return False
        else:
            if len(self.blocks) > 0:
                lastblock = self.getlastBlock()
                if newblock.previous == lastblock.hash and newblock.checkIntegrity():
                    #self.blocks[newblock.index] = newblock
                    self.blocks.append(newblock)
                    self.storage.addBlock(newblock)
                    return True
                else:
                    print("Newblock was refused")
                    print("NEWBLOCK:",newblock)
                    print("PREVIOUS:",lastblock)
                    return False
            else:
                # adding genesis block
                if (0 == newblock.index and newblock.checkIntegrity()):
                    #self.blocks[newblock.index] = newblock
                    self.blocks = [newblock]
                    self.storage.addBlock(newblock)
                    print("Genesis block was added")
                    return True
                return False

    def getBlock(self, index=-1,hash=""):
        blockrec = None
        if index>=0:
            blockrec = self.storage.getBlockByIndex(index)
        if hash!="":
            blockrec = self.storage.getBlockByHash(hash)
        return recordToBlock(blockrec)

    def getBlocks(self,offset=-1,count=-1,criteria=""):
        blocks = []
        if offset!=-1 and count !=-1:
            blockrecs = self.storage.getBlockRange(offset,count)
        elif criteria != "":
            blockrecs = self.storage.getByCriteria(criteria)
        if blockrecs is None:
            return []
        else:
            prev = None
            for blockrec in blockrecs:
                block = recordToBlock(blockrec,prev)
                blocks.append(block)
                if offset != -1: prev = block
            return blocks

def genTestTransaction():
    users = ["user01","user02","user03","user04","user05","user06","user07"]
    seller = random.choice(users)
    users.remove(seller)
    buyer = random.choice(users)


    sellerHex = hashIt(seller)
    buyerHex = hashIt(buyer)
    assetIds = ["ISIN"+str(x) for x in range(0,10)]
    assetId = random.choice(assetIds)
    #sha.update(assetId.encode("utf-8"))
    assetHex = hashIt(assetId)

    #return {"price":random.randint(0,100),"volume":random.randint(1,100)*100,"ISIN":"001","seller":"x0{}".format(random.randint(0,9)),"buyer":"x0{}".format(random.randint(0,9))}
    return {"price":random.randint(0,100),"volume":random.randint(1,100)*100,"ISIN":assetHex,"seller":sellerHex,"buyer":buyerHex}

def nextBlock(previousblock, data):
    #newblock = CryptoBlock(previousblock.index+1,date.datetime.now(),data,previousblock.hash)
    if previousblock is None:
        print("Error created next block. Previous block was not defined.")
        return None
    else:
        newblock = CryptoBlock(idx=previousblock.index+1,previous=previousblock.hash,content=data)
    return newblock


def nextLargeBlock(previousblock):
    #newblock = CryptoBlock(previousblock.index+1,date.datetime.now(),data,previousblock.hash)
    if previousblock is None:
        print("Error created next block. Previous block was not defined.")
        return None
    else:
        largeblock = []
        prevback = previousblock.hash
        idx = previousblock.index
        for a in range(200000):
            data = genTestTransaction()
            idx += 1
            previous = CryptoBlock(idx=idx,previous=previousblock.hash,content=data)
            largeblock.append(eval(json.dumps(previous.getRecordClean(),default=str)))
        idx += 1
        newblock = CryptoBlock(idx=idx,previous=prevback,content=largeblock)
        #while (newblock.hash[-PoW:]!='000000000'[-PoW:] and PoW >0):
        #    newblock.setnounce(newblock.nounce+1)
        #print(newblock)
    return newblock


"""
def demo():
    sometime = date.datetime.now()
    myblock = CryptoBlock(0,sometime,"(Root)","0")
    blockchain = []
    blockchain.append(myblock)
    prevblock = myblock
    for o in range(1,20):
        otherblock = nextBlock(prevblock,"(Transfer: A -> B : 80")
        prevblock = otherblock
        blockchain.append(otherblock)

    for block in blockchain:
        print(block)


    def loadJSON(self,JSONText):
        blockList = json.loads(JSONText)
        for block in blockList:
            newblock = CryptoBlock(block["index"],block["nounce"],block["previous"],block["data"],date.datetime.strptime(block["timestamp"],"%Y-%m-%d %H:%M:%S.%f"))
            self.addBlock(newblock)

    def loadBlocks(self):
        with open(self.filepath) as data_file:
            #self.loadJSON(data_file)
            blockList = json.load(data_file)
            for block in blockList:
                newblock = CryptoBlock(block["index"],block["nounce"],block["previous"],block["data"],date.datetime.strptime(block["timestamp"],"%Y-%m-%d %H:%M:%S.%f"))
                self.addBlock(newblock)
            print("Blocks Loaded {} from file".format(len(self.blocks)))

    def saveBlocks(self):
        with open(self.filepath,'w', encoding='utf-8') as f:
            f.write(str(self.toJSON()))
        #print("File {} saved!".format(self.filepath))
        print("Blocks saved {} to file {}".format(len(self.blocks),self.filepath))
"""

"""
    def checkIntegrityRange(self,start,end,prev=None):
        blockrecs = self.storage.getblockrange(start,end)
        for blockrec in blockrecs:
"""
