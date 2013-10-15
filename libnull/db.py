import sqlite3, time
from socket import inet_aton
from struct import pack

DAYS_30 = 60*60*60*24*30

STATE_DOWNLOADING = 0
STATE_SEEDING = 1

MAX_PEERS = 1000

class DB(object):
    def __init__(self, name):
        self.name = name

    def get_conn(self):
        return sqlite3.connect("%s.db" % self.name)

    def __enter__(self):
        return self.get_conn()

    def __exit__(self, *args): pass

    def create(self):
        with self as conn:
            c = conn.cursor()
            c.execute("""
                CREATE TABLE articles
                    (added BIGINT,
                        title TEXT,
                        magnet TEXT,
                        hash BLOB)""")
            c.execute("""
                CREATE TABLE peers
                    (hash BLOB,
                        id TEXT,
                        ip TEXT,
                        port INT,
                        state INT)
                """)
            conn.commit()

    def add_peer(self, hash, id, ip, port, state):
        if not state in [STATE_DOWNLOADING, STATE_SEEDING]:
            return False
        with self as conn:
            c = conn.cursor()
            c.execute("""INSERT INTO peers VALUES (?, ?, ?, ?, ?)""",
                (hash, id, ip, port, state))
            conn.commit()

    def add_article(self, text, magnet, hash):
        with self as conn:
            c = conn.cursor()
            c.execute("""INSERT INTO articles VALUES (?, ?, ?, ?)""",
                (time.now(), text, magnet, hash))
            conn.commit()
        return True

    def get_articles(self, max_age=DAYS_30): pass

    def get_num_articles(self):
        with self as conn:
            c = conn.cursor()
            c.execute("""SELECT * FROM articles""")
            return c.rowcount

    def get_num_peers(self):
        with self as conn:
            c = conn.cursor()
            c.execute("""SELECT * FROM peers""")
        return c.rowcount

    def get_peers(self, hash, count=500, compact=False):
        with self as conn:
            c = conn.cursor()
            if count > MAX_PEERS:
                count = MAX_PEERS
            results = []
            for row in c.execute("SELECT * FROM peers WHERE hash=?", (hash, )):
                results.append({
                    "peer_id": row[1],
                    "ip": row[2],
                    "port": row[3]
                })

            if compact:
                final = ""
                for res in results:
                    ip = inet_aton(res['ip'])
                    port = pack(">H", int(res['port']))
                    final += (ip+port)
                return final

            return results
