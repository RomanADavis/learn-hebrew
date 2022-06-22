from mysql.connector import connect

class Connector():
    host = "localhost"
    database = "hebrew"
    user = "roman"
    password = ""
    connection = connect(
        host=host, 
        database=database, 
        user=user,
        password=password)

    cursor = connection.cursor(buffered=True, dictionary=True)
    commit = connection.commit

    @classmethod
    def query(cls, query_string):
        result = cls.cursor.execute(query_string) 
        if result == None:
            return cls.cursor.lastrowid
        return  result
    
    @classmethod
    def fetchall(cls):
        return cls.cursor.fetchall()
    
    @classmethod
    def debug(cls, query_string):
        cls.query(query_string)
        results = cls.cursor.fetchall()
        
        for result in results:
            print(result)

    @classmethod
    def set_fk_check(cls, bit):
        query = f"SET FOREIGN_KEY_CHECKS = {bit};"
        cls.query(query)

    # @classmethod
    # def row_id(cls):
        

    
