import MySQLdb

class MySQLdbHelper():
    def __init__(self):
        self.conn = MySQLdb.connect(
            host='mysql',
            user='root',
            password='root',
            db='concerts',
            charset='utf8'
        )
        self.cursor = self.conn.cursor()

    def _query(self):
        self.query = ''
        return self

    def save(self, data):
        query = ('INSERT INTO event (name,venue,date) VALUES (%s, %s, %s)')
        data = (data['band'], data['venue'], data['date'])
        self.cursor.execute(query, data)
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
