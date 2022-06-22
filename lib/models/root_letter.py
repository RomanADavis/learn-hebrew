from lib.models.connector import Connector

class Root_Letter():
    query = Connector.query
    database = Connector.database
    table = "root_letter"
    create_table_query = """
    CREATE TABLE root_letter(
                    id INT NOT NULL AUTO_INCREMENT,
                    root_id INT NOT NULL,
                    letter_id INT NOT NULL,
                    letter_index INT NOT NULL,
                    PRIMARY KEY (id),
                    FOREIGN KEY (root_id) 
                        REFERENCES word_root(id)
                        ON DELETE CASCADE,
                    FOREIGN KEY (letter_id) 
                        REFERENCES letter(id)
                        ON DELETE CASCADE
                    );"""
 
    @classmethod
    def insert_query(cls, dict):
        keys = ', '.join(dict.keys())
        values = ', '.join([f"'{v}'" for v in dict.values()])
        query = f"INSERT INTO {cls.table} ({keys}) VALUES ({values});"
        print(query)

        return query

    @classmethod
    def drop_table(cls):
        Connector.set_fk_check(0)
        query = f"DROP TABLE IF EXISTS {cls.table}"
        cls.query(query)
        Connector.set_fk_check(1)

    @classmethod
    def create_table(cls):
        cls.drop_table()
        cls.query(cls.create_table_query)

    @classmethod
    def insert(cls, dict):
        Connector.query(cls.insert_query(dict))
        result = Connector.cursor.lastrowid
        return result