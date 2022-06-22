# Model for Hebrew letters
import json

from lib.models.connector import Connector

class Letter():
    query = Connector.query
    database = Connector.database
    table = "letter"
    create_table_query = """
    CREATE TABLE letter(
                id int NOT NULL AUTO_INCREMENT, 
                letter_char char, 
                glyph char, 
                letter_name varchar(10), 
                meaning varchar(300), 
                rationale varchar(5000),
                PRIMARY KEY (id)
                );"""

    # Initializes the letter from some set of properties
    def __init__(self):
        pass

    # Returns a card object for the (eventual?) site.
    def card(self):
        pass

    # Returns a heiroglyphic based on the letter.
    def glyph(self):
        pass

    ## For parsing, loading and saving

    # Saves the Letter to a database
    def save(cls, json):
        pass

    # Loads the Letter 
    def load(cls, properties):
        pass

    # For creating a letter from a JSON
    def from_dict(cls, dict):
        pass

    ## For interacting with the views

    def create(cls):
        pass

    def read(cls):
        pass

    def update(cls):
        pass

    def delete(cls):
        pass

    # Debugging
    @classmethod
    def show_all(cls):
        query = f"SELECT * FROM {cls.table}"
        Connector.debug(query)
        
    @classmethod
    def get_id(cls, letter):
        # cls.show_all()
        query = f"SELECT id FROM letter WHERE letter_char = '{letter}';"
        cls.query(query)
        # print(query)
        result = Connector.cursor.fetchall()[0]['id']
        return result

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

    ## For getting the whole thing started
    @classmethod
    def initialize(cls):
        cls.create_table()
        print(Connector.query("SHOW TABLES;"))

        letters = json.load(open("mnemonic_hints.json"))
        [l.pop("sophit", None) for l in letters]
        insert = "INSERT INTO letter (letter_char, glyph, letter_name, meaning, rationale) VALUES"
        for letter in letters:
            values = "(" + ", ".join(["\""+v.replace('"', "'")+"\"" for v in letter.values()]) + ")"
            values = values
            # print(f"{insert} {values};")
            Connector.query(f"{insert} {values};")
