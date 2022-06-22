import pymysql
from pymysql.converters import escape_string

from lib.models.connector import Connector
from lib.models.word_letter import Word_Letter
from lib.models.letter import Letter

class Word():
    last_row = None
    query = Connector.query
    database = Connector.database
    table = "word"
    create_table_query = """
    CREATE TABLE word(
id INT NOT NULL AUTO_INCREMENT,
word varchar(20),
translation varchar(100),
alternative_translations varchar(1000),
definition varchar(1000),
aramaic_definition varchar(1000),
alternative_spellings varchar(1000),
kjv_translation varchar(1000),
strongs_hebrew varchar(100),
strongs_aramaic varchar(100),
aramaic_spelling varchar(20),
relation_to_root varchar(1000),
edenics varchar(1000),
parent_id INT,
PRIMARY KEY (id),
FOREIGN KEY (parent_id) 
    REFERENCES word_root(id)
    ON DELETE CASCADE
                );"""

    # Initializes the parent root from some set of properties
    def __init__(self):
        pass

    # Returns a card object for the (eventual?) site.
    def card(self):
        pass

    # Returns a glyph set for the root based on the characters.
    def glyphs(self):
        pass

    # Saves the root to a database
    def save(cls, json):
        pass

    # Loads the root 
    def load(cls, properties):
        pass

    # For creating a root from a JSON
    def from_dict(cls, dict):
        pass

    ## For interacting with the views

    def create(cls):
        pass

    @classmethod
    def read(cls, id):
#         id INT NOT NULL AUTO_INCREMENT,
# word varchar(20),
# translation varchar(100),
# alternative_translations varchar(1000),
# definition varchar(1000),
# aramaic_definition varchar(1000),
# alternative_spellings varchar(1000),
# kjv_translation varchar(1000),
# strongs_hebrew varchar(100),
# strongs_aramaic varchar(100),
# aramaic_spelling varchar(20),
# relation_to_root varchar(1000),
# edenics varchar(1000),
# parent_id INT,
        query = """SELECT 
                word_letter.word_id, word.word, word.translation, 
                word.alternative_translations, word.definition, 
                word.aramaic_definition, word.alternative_spellings, 
                word.kjv_translation, word.strongs_hebrew, word.strongs_aramaic, 
                word.relation_to_root, word.edenics, word_root.word_root_name,        
            GROUP_CONCAT(letter.glyph                  
                ORDER BY word_letter.letter_index SEPARATOR '')                  
                AS glyph from letter              
            JOIN  word_letter                  
                ON word_letter.letter_id = letter.id               
            JOIN word                  
                ON word.id = word_letter.word_id              
            LEFT JOIN word_root
                ON word.parent_id = word_root.id 
            GROUP BY word_letter.word_id
            """

        Connector.query(query)
        results = Connector.fetchall()
        word = {r["word_id"]: r for r in results}[id]
        
        for k, v in word.items():
            padding = " " * (40 - len(k))
            if v != "":
                print(f"{k}:{padding}{v}")

        return word
    
    @classmethod
    def update(cls, updated, id):
        query = "UPDATE word SET "
        query += ", ".join([f"{k} = '{escape_string(v)}'" for k, v in updated.items()])
        query += f" WHERE id = {id}"

        print(query)
        Connector.query(query)

    @classmethod
    def delete(cls, id):
        query = f"DELETE FROM word WHERE word.id = {id};"
        Connector.query(query)

    @classmethod
    def show(cls, start, end):
        query = """SELECT word_letter.word_id, word.word, 
            GROUP_CONCAT(letter.glyph 
                ORDER BY word_letter.letter_index SEPARATOR '') 
                AS glyph from letter 
            JOIN  word_letter 
                ON word_letter.letter_id = letter.id  
            JOIN word 
                ON word.id = word_letter.word_id 
            GROUP BY word_letter.word_id;"""

        Connector.query(query)
        words = Connector.fetchall()[start:end]

        print("ID\tWORD\tGLYPH")
        for word in words:
            word = [str(w) for w in word.values()]
            print("\t".join(word))

    # Debugging
    @classmethod
    def show_all(cls):
        query = f"SELECT * FROM {cls.table}"
        Connector.debug(query)

    @classmethod
    def insert_query(cls, dict):
        dict["aramaic_definition"] = dict.pop("aramaic definition", "")
        dict["relation_to_root"] = dict.pop("relationship to root", "")
        dict["alternative_translations"] = dict.pop("alternate translations", "")
        dict["alternative_spellings"] = dict.pop("aramaic spelling", dict.pop("alternative spellings", dict.pop("alternate spellings", "")))
        dict["kjv_translation"] = dict.pop("kjv translations", dict.pop("kjv translation", ""))
        dict["strongs_hebrew"] = dict.pop("strong's hebrew #", dict.pop("strongs_hebrew", ""))
        dict["strongs_aramaic"] = dict.pop("strong's aramaic #", dict.pop("strongs_aramaic", ""))
        keys = ', '.join(dict.keys())
        values = ', '.join([f"'{escape_string(v)}'" for v in dict.values()])
        query = f"INSERT INTO {cls.table} ({keys}) VALUES ({values});"
        print(query)
        return query

    @classmethod
    def insert(cls, dict):

        # print(dict)
        cls.last_row = Connector.query(cls.insert_query(dict))

        name = dict["word"]
        # Word.show_all()
        Connector.commit()
        for index, letter in enumerate(name):
            Word_Letter.insert({
                "word_id": cls.last_row,
                "letter_id": Letter.get_id(letter),
                "letter_index": index
            })
        
        return cls.last_row

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

