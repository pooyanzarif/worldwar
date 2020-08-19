import MySQLdb
import MySQLdb.cursors

class tdb:
    host = ""
    username = ""
    password = ""
    database = ""
    cursor = 0
    db = 0

    def __init__(self, config):
        self.host= config['host']
        self.username = config['username']
        self.password = config['password']
        self.database = config['database']
        self.connect()

    def connect(self):
        self.db = MySQLdb.connect(self.host, self.username, self.password, self.database,cursorclass=MySQLdb.cursors.DictCursor)
        self.db.ping(True)
        self.db.autocommit(True)

    def execute(self,sql):
        if not self.db.open:
            self.connect()
        self.cursor = self.db.cursor()
        return self.cursor.execute(sql)

    def fetchall(self):
        # if not self.db.open:
        #     self.connect()
        result = self.cursor.fetchall()
        return result

    def fetchone(self):
        # if not self.db.open:
        #     self.connect()
        result = self.cursor.fetchone()
        return result

    def close(self):
        if self.db.open:
            return self.db.close()

    def commit(self):
        return self.db.commit()

    def rollback(self):
        return self.db.rollback()

    def lastrowid(self):
        return self.cursor.lastroid

    def callproc(self,procname, args=()):
        if not self.db.open:
            self.connect()
        return self.cursor.callproc(procname,args)
        self.cursor.callproc()
