import sqlite3
from genepi.storage.base import BaseStorage


class SqliteStorage(BaseStorage):

    def __init__(self, filename):
        self.filename=filename
    
    def initialize(self):
        conn = sqlite3.connect(self.filename)
        try:
            c = conn.cursor()
            c.execute("DROP TABLE IF EXISTS POPULATION");
            query ='''CREATE TABLE POPULATION (hash integer, 
                generation integer, individual text, score real,
                PRIMARY KEY(hash, generation))'''
            c.execute(query)
        except:
            raise
        finally:
            conn.close()
    
    def write_individual(self, hash, generation, individual):
        conn = sqlite3.connect(self.filename)
        try:
            c = conn.cursor()
            c.execute("SELECT * FROM POPULATION WHERE hash=? AND generation=?", (hash, generation));
            record = c.fetchone()
            if record:
                query = '''UPDATE POPULATION SET individual=?, score=? WHERE  hash=? AND generation=?'''
                c.execute(query, (individual.to_json(), individual.score, hash, generation))
            else:
                query = '''INSERT INTO POPULATION (hash, generation, individual, score) VALUES(?,?,?,?)'''
                c.execute(query, (hash, generation, individual.to_json(), individual.score))            
            conn.commit()
        except:
            raise
        finally:
            conn.close()
        
    def write_population_stats(self, generation, stats):
        conn = sqlite3.connect(self.filename)
        try:
            c = conn.cursor()
            """
            c.execute("SELECT * FROM POPULATION WHERE hash=? AND generation=?", (hash, generation));
            record = c.fetchone()
            if record:
                query = '''UPDATE POPULATION SET individual=?, score=? WHERE  hash=? AND generation=?'''
                c.execute(query, (individual.to_json(), individual.score, hash, generation))
            else:
                query = '''INSERT INTO POPULATION (hash, generation, individual, score) VALUES(?,?,?,?)'''
                c.execute(query, (hash, generation, individual.to_json(), individual.score))            
            """
        except:
            raise
        finally:
            conn.close()