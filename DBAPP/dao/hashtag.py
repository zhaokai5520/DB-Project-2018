from config.dbconfig import pg_config
import psycopg2
class HashtagDAO:

    def __init__(self):

        connection_url = "dbname={} user={} host={} password={}".format(
            pg_config['dbname'],
            pg_config['user'],
            pg_config['host'],
            pg_config['password']
        )

        self.conn = psycopg2._connect(connection_url)

        #########Data from phase 1#######
        #                               #
        # H1 = [101, 'Hello', 1]        #
        # H2 = [102, 'NewYear', 2]      #
        # H3 = [103, 'DoingGood', 1]    #
        # H4 = [104, 'LetsParty', 1]    #
        # H5 = [105, 'YOLO', 2]         #
        # self.data = []                #
        # self.data.append(H1)          #
        # self.data.append(H2)          #
        # self.data.append(H3)          #
        # self.data.append(H4)          #
        # self.data.append(H5)          #
        #################################
    
    def getAllHashtags(self):
        cursor = self.conn.cursor()
        query = "select * from hashtag;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getHashtagByID(self, hid):
        cursor = self.conn.cursor()
        query = "select * from hashtag " \
                "where hid = {};".format(hid)
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getHashtagByText(self, text):
        cursor = self.conn.cursor()
        query = "select * from hashtag " \
                "where htext = '#{}';".format(text)
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTop10Hashtags(self):
        cursor = self.conn.cursor()
        query = "select * from hashtag " \
                "order by hcount desc " \
                "limit 10;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result