from blockchain import *
import timeit
import datetime
import os,sys
import json

def hackdatabase(dbname,index):

    hackbase = BlockChainStorage(dbname)

    blockrec = hackbase.getBlockByIndex(index)
    hackbase.close()
    blockobj = json.loads(blockrec["block"])
    block = CryptoBlock(**blockobj)

    #print(block)
    blocks = []
    for a in range(2000):
        block.content["price"] = block.content["price"]+1
        blocks.append(block)

    hackbase = BlockChainStorage(dbname)
    hackbase.addblocks(blocks)
    #print(block)

    if False:
        conn = sqlite3.connect('{}.db'.format(dbname))
        conn.row_factory = lambda c, r: dict([(col[0], r[idx]) for idx, col in enumerate(c.description)])
        c = conn.cursor();
        c.execute("INSERT OR REPLACE INTO blockchain values(:idx,:hash,:created,:block)", block.getRecord() )
        conn.commit()
        conn.close()

#hackdatabase("block01",2)

def standard():

    #os.remove("block01.db")

    #hackdatabase("block01",12000)

    myblockchain = BlockChain("block01")
    if myblockchain.getlastBlock() is None:
        myblockchain.addBlock(CryptoBlock())
    tic = timeit.default_timer()

    # MANY SMALL
    if False:
        newblock = myblockchain.getlastBlock()
        for x in range(50):
            newblock = nextBlock(newblock,genTestTransaction())
            myblockchain.addBlock(newblock)


    #LARGE BLOCK
    #newblock = nextLargeBlock(myblockchain.getlastBlock())
    #print(newblock)
    #myblockchain.addBlock(newblock)

    # BULK SUBMIT
    if False:
        blocks = []
        newblock=myblockchain.getlastBlock()
        for x in range(100):
            newblock = nextBlock(newblock,genTestTransaction())
            blocks.append(newblock)
        myblockchain.storage.addBlocks(blocks)

        #for block in blocks:
        #    print(blocks)
        #sys.exit()
    toc = timeit.default_timer()
    print("Time elapsed:",str(datetime.timedelta(seconds=toc-tic)))


    #lastblock = myblockchain.getBlock(50080)
    #print(lastblock)
    #lastlastblock = myblockchain.getBlock(hash=lastblock.previous)
    #print(lastlastblock)
    if False:
        tic = timeit.default_timer()
        print("Verifying blockchain")
        if myblockchain.checkAll() :
            print("1st CHECKS OUT OK !!")
        else:
            print("1st ERROR !!")
        toc = timeit.default_timer()
        print("Time elapsed:",str(datetime.timedelta(seconds=toc-tic)))

    block = myblockchain.getBlock(200013)
    print(block)

    #recblocks = myblockchain.storage.getByCriteria('%"seller": "x01"%')
    if False:
        tic = timeit.default_timer()
        #recblocks = myblockchain.storage.getByCriteria('%"volume": 4200%')
        recblocks = myblockchain.storage.getByCriteria('%"x04"%')
        #recblocks = myblockchain.storage.getBlockRange(230230200,10)
        if recblocks is None:
            print("Empty")
        else:
            q = 0
            for recblock in recblocks:
                block = CryptoBlock(**json.loads(recblock["block"]))
                seller = block.content.get("seller")
                if seller is None:
                    print(block)
                    print(block.content)
                    break
                else:
                    if seller == "x04": q -=block.content["volume"]*block.content["price"]
                buyer = block.content.get("buyer")
                if seller is None:
                    print(block)
                    print(block.content)
                    break
                else:
                    if buyer == "x04": q +=block.content["volume"]*block.content["price"]
                #print(block)
            print("Client x04 net value:",q)
        print("Total of {} observations".format(len(recblocks)))
        toc = timeit.default_timer()
        print("Time elapsed:",str(datetime.timedelta(seconds=toc-tic)))

    if False:
        blockrecs = myblockchain.storage.getNumberOfBlocks(1000)
        for blockrec in blockrecs:
            print(blockrec)
            blockdef = blockrec["block"]
            print(blockdef)
            block = CryptoBlock(**json.loads(blockdef))
            print(block)

            print("================")


    #sellerCode = hashIt("user03")
    assetCode = hashIt("ISIN1")
    #blocks = myblockchain.getBlocks(criteria='%"seller" = "x01"%')
    #blocks = myblockchain.getBlocks(criteria='%"seller": "{}"%'.format(sellerCode))


    #assetCode = "ae96f7d70a379a1a64feb65f30feb5209bd7089d4c568ca8fb86510284c205bd"
    blocks = myblockchain.getBlocks(criteria='%"ISIN": "{}"%'.format(assetCode))
    print(blocks[0])

    #print(myblockchain.getBlock(100))
    #blocks = myblockchain.getBlocks(200,10)
"""
    for block in blocks:
        print(block)
    print(len(assetCode))
    print(16**64)
    print(2**256)
    print(256**32)
    print(16**2)
    print(256/4)
    keyLength=2048
    print(2**keyLength)
    print(2**8)
    print(keyLength/8)
"""
standard()

#print(myblockchain)

#print(myblockchain)


def addMore():
    if len(myblockchain.blocks) == 0:
        myblock = CryptoBlock()
        myblockchain.addBlock(myblock)
        prevblock = myblock
    else:
        prevblock = myblockchain.getlastBlock()
    for x in range(2000):
        nxblock = nextBlock(prevblock,genTestTransaction())
        myblockchain.addBlock(nxblock)
        prevblock = nxblock

#myblockchain.saveBlocks()




def secondstage():
    otherblockchain = BlockChain("test2.json","blokc02")
    otherblockchain.loadJSON(str(myblockchain))
    manip = 0
    if manip>0:
        block = otherblockchain.blocks[manip]
        block.data = genTestTransaction()
        block.hash = block._internalHash()
        prevhash = block._internalHash()
        for block in otherblockchain.blocks[manip+1:]:
            block.previous = prevhash
            block.hash = block._internalHash()
            prevhash = block._internalHash()

    otherblockchain.saveBlocks()

    #print(otherblockchain)

    thirdblockchain = BlockChain("test2.json","blokc03")
    thirdblockchain.loadBlocks()
    #print(thirdblockchain)

    print(thirdblockchain.getBlock(20))

    #print(thirdblockchain.getLastBlocks(20))

    #block = thirdblockchain.blocks[2]
    #block.data = eval(json.dumps([{"price":random.randint(0,100),"ISIN":"001","seller":"x0{}".format(random.randint(0,9)),"buyer":"x0{}".format(random.randint(0,9))}]))
    #block.hash = block._internalHash()

    if myblockchain.checkIntegrity() :
        print("1st CHECKS OUT OK !!")
    else:
        print("1st ERROR !!")

    if otherblockchain.checkIntegrity() :
        print("2nd CHECKS OUT OK !!")
    else:
        print("2nd ERROR !!")
    if thirdblockchain.checkIntegrity() :
        print("3rd CHECKS OUT OK !!")
    else:
        print("3rd ERROR !!")

    if myblockchain.compare(thirdblockchain):
        print("1st and 3rd is the same")
    else:
        print("BREACH OF INTEGRITY: 1st and 3rd is not the same")


    print("MAIN")
"""
for block in myblockchain.blocks:
    print(block.previous)
    print(block.hash)
    print(block._internalHash())
    print(block.hash==block._internalHash())

print("MAIN")
print(myblockchain.blocks[1].hash)
print(myblockchain.blocks[1]._internalHash())

print("ALT")
print(otherblockchain.blocks[1].hash)
print(otherblockchain.blocks[1]._internalHash())

print("MAIN")
print(myblockchain.blocks[1].cleanString())

print("ALT")
print(otherblockchain.blocks[1].cleanString())
"""
#print(myblock)
#print(myblock.__dict__)
#print(json.dumps(myblock,default=lambda o:myblock.__dict__),sort_keys=True,indent=4)
#print(json.dumps(myblock.__dict__,default=str))
#print(myblock.toJSON())
#print(nxblock.toJSON())
#delta = BlockfromJSON(nxblock.toJSON())
#print(delta.toJSON())
