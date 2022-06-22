# Model for Hebrew parent root words
import json
from collections.abc import Mapping
import pymysql
from pymysql.converters import escape_string

from lib.models.connector import Connector
from lib.models.word import Word
from lib.models.root_letter import Root_Letter
from lib.models.letter import Letter

import MySQLdb

class Root():
    query = Connector.query
    database = Connector.database
    table = "word_root"
    create_table_query = """
    CREATE TABLE word_root(
                id INT NOT NULL AUTO_INCREMENT,
                word_root_name varchar(20),
                parent_id INT,
                object varchar(100),
                action varchar(100),
                abstract varchar(100),
                definition varchar(1000),
                relationships varchar(1000),
                ancient_hebrew varchar(1000),
                edenics varchar(1000),
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

    # Returns a glyph set for the root based on the letters.
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

    def read(cls):
        pass

    def update(cls):
        pass

    def delete(cls):
        pass

    @classmethod
    def insert(cls, dict):
        Connector.query(cls.insert_query(dict))
        result = Connector.cursor.lastrowid

        name = dict["word_root_name"]
        exceptions = ["Adopted Roots", "4 letter words", "Affixes"]
        if name in exceptions:
            return result

        for index, letter in enumerate(name):
            Root_Letter.insert({
                "root_id": result,
                "letter_id": Letter.get_id(letter),
                "letter_index": index
            })
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

    @classmethod
    def insert_query(cls, dict):
        dict["relationships"] = dict.pop("relationship to parent", None)
        dict["ancient_hebrew"] = dict.pop("ancient hebrew", None)
        dict["word_root_name"] = dict.pop("root", dict.get("word_root_name"))

        dict = {k: v for k, v in dict.items() if v is not None}
        print(dict)
        keys = ', '.join([k for k, v in dict.items() if not isinstance(v, Mapping)])
        values = ', '.join(["'" + escape_string(str(v)) + "'" for k, v in dict.items() if not isinstance(v, Mapping)])
        query = f"INSERT INTO {cls.table} ({keys}) VALUES ({values});"
        print(query)

        return query
