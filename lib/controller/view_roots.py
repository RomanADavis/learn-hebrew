from lib.models.connector import Connector
from lib.models.word import Word

class WordViews():
    start = 0
    end = 15

    @classmethod
    def run(cls):
        cls.scan()
        choice = input("")
        while(True):
            cls.tick(choice)
            choice = input("") + " "

    @staticmethod
    def noop():
        pass

    @classmethod
    def tick(cls, choice):
        controls = {"M": cls.more,
                    "R": cls.read,
                    "D": cls.delete,
                    "U": cls.update,
                    "C": cls.create,
                    "X": cls.exit,
                    " ": cls.noop, #NOOP
                    "S": Word.show_all
                    }

        function = controls.get(choice[0], controls[" "])

        if choice[0] in "RDU":
            number = input("Which one?")
            function(int(number))
        else:
            function()

    @classmethod
    def scan(cls):
        Word.show(cls.start, cls.end)
    
    @classmethod
    def more(cls):
        cls.start += 15
        cls.end += 15
        cls.scan()

    @staticmethod
    def read(id):
        return Word.read(id)

    @classmethod
    def delete(cls, id):
        Word.delete(id)
        print("<< DELETED >>")
        cls.scan()

    @classmethod
    def update(cls, id):
        updated = {}
        word = cls.read(id)
        print(word)
        print("TODO: check user input")


        for k, v in word.items():
            if k in ["word_id", "word", "parent_id", "word_root_name"] :
                continue
            if k == "glyph":
                continue

            padding = " " * (40 - len(k))
            # print(f"{k}:{padding}{v}")
            updated[k] = input(f"{k}:")

        Word.update(updated, id)
        cls.read(id)
    
    @staticmethod
    def random_word():
        query = "SELECT letter_char FROM letter ORDER BY RAND() LIMIT 3;"
        Connector.query(query)
        letters = Connector.fetchall()
        return "".join([l["letter_char"] for l in letters])
    
    @classmethod
    def create(cls):
        word = {
            "word": "",
            "translation": "",
            "alternative_translations": "",
            "definition": "",
            "aramaic definition": "",
            "alternative_spellings": "",
            "kjv_translation": "",
            "strongs_hebrew": "",
            "strongs_aramaic": "",
            "aramaic_spelling": "",
            "relation_to_root": "",
            "edenics": ""
        }

        print("TODO: check user input")

        for k, v in word.items():
            if k == "word":
                word[k] = cls.random_word()
                print(f"word:{word[k]}")
                continue

            padding = " " * (40 - len(k))
            word[k] = input(f"{k}:{padding}")

        Word.insert(word)
        cls.read(Word.last_row)

    @classmethod
    def exit(cls):
        Connector.commit()
        print("Have a nice day!")
        exit()
        

    