import sqlite3


def dict_from_row(row):
    return dict(zip(row.keys(), row))





class BlockChainStorage:

    def __init__(self,basename="blockchain"):
        #self.conn = sqlite3.connect(':memory:')
        self.conn = sqlite3.connect('{}.db'.format(basename))
        self.basename = basename
        #self.conn.row_factory = sqlite3.Row
        self.conn.row_factory = lambda c, r: dict([(col[0], r[idx]) for idx, col in enumerate(c.description)])
        self.c = self.conn.cursor();
        #self.c.execute("""DROP TABLE blockchain""")
        self.c.execute("""
            CREATE  TABLE IF NOT EXISTS blockchain (
                idx integer primary key,
                hash char(64),
                created timestamp,
                block text
            )
            """)

    def getByCriteria(self,criteria):
        self.c.execute("SELECT idx,hash,created,block FROM blockchain WHERE block LIKE :criteria", {'criteria':criteria} )
        return self.c.fetchall()

    def getBlockRange(self,start,steps):
        self.c.execute("SELECT idx,hash,created,block FROM blockchain ORDER BY idx ASC LIMIT :steps OFFSET :start", {'start':start,'steps':steps} )
        return self.c.fetchall()

    def getNumberOfBlocks(self,numberOfBlocks):
        self.c.execute("SELECT * FROM (SELECT idx,hash,created,block FROM blockchain ORDER BY idx DESC LIMIT :bounds) ORDER BY idx ASC", {'bounds':numberOfBlocks} )
        return self.c.fetchall()

    def addBlock(self,block):
        with self.conn:
            self.c.execute("INSERT INTO blockchain values(:idx,:hash,:created,:block)", block.getRecord() )

    def addBlocks(self,blocks):
        self.c.execute("BEGIN TRANSACTION;" )
        for block in blocks:
            #print(block.index)
            self.c.execute("INSERT INTO blockchain values(:idx,:hash,:created,:block);", block.getRecord() )
        self.c.execute("COMMIT;" )


    def getBlockByIndex(self,index):
        self.c.execute("SELECT idx,hash,created,block FROM blockchain WHERE idx = :idx", {'idx': index})
        return self.c.fetchone()

    def getBlockByHash(self,qhash):
        self.c.execute("SELECT idx,hash,created,block FROM blockchain WHERE hash = :hash", {'hash': qhash})
        return self.c.fetchone()

    def removeBlock(self,qhash):
        with self.conn:
            self.c.execute("""DELETE from blockchain where hash = :hash """,{'hash':qhash})

    def close(self):
        self.conn.close()
