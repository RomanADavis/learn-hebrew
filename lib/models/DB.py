import json

from lib.models.connector import Connector
from lib.models.letter import Letter
from lib.models.root import Root
from lib.models.root import Word
from lib.models.root_letter import Root_Letter
from lib.models.word_letter import Word_Letter

class DB():
    @classmethod
    def initialize(cls):
        # Eventually figure out how to drop all the tables and execute at the
        # top of initialize.

        Letter.initialize()
        
        Root.create_table()
        Word.create_table()
        Root_Letter.create_table()
        Word_Letter.create_table()

        Connector.debug("SHOW TABLES;")

        roots = json.load(open("roots.json"))
        exceptions = ["4 letter words", "Affixes"]
        for letter, values in roots.items():
            parent = Root.insert({"word_root_name": letter})
            for two_letter, values in values.items():
                if not isinstance(values, dict):
                    continue
                if parent == "4 letter words":
                    # Wait, are these just words?
                    root = two_letter
                    query = Word.insert({
                        "word": values.get("root", root),
                        "translation": values.get("translation", ""),
                        "definition": values.get("definition", ""),
                        "alternative_spellings": values.get("alternative spellings", ""),
                        "kjv_translation": values.get("kjv translation", ""),
                        "strongs_hebrew": values.get("strong's hebrew #", ""),
                        "strongs_aramaic": values.get("strong's aramaic #", ""),
                        "parent_id":  parent
                    })
                    continue
                else:
                    query = Root.insert({"word_root_name": two_letter, "parent_id": parent})
                for root, values in values.items():
                    if not isinstance(values, dict):
                        continue
                    if values.get("root", False):
                        Root.insert(values)
                    if values.get("word", False):
                        Word.insert(values)
                    # I think this is as deep as it goes?
                    for word, values in values.items():
                        if not isinstance(values, dict):
                            continue
                        if values.get("root", False):
                            Root.insert(values)
                        if values.get("word", False):
                            Word.insert(values)