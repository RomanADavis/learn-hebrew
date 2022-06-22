from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as Soup
import json

mnemonic_hints = json.loads(open("mnemonic_hints.json").read())
letter_names = [h["name"] for h in mnemonic_hints]

    
mnemonic_hints += [
    {"name": "other roots", "letter": "Adopted Roots"},
    {"name": "4 letter words", "letter": "4 letter words"},
    {"name": "Prefixes, Suffixes and Infixes".lower(), "letter": "Affixes"}
]

name_letter = {hint["name"]: hint["letter"] for hint in mnemonic_hints}

image_tags = {'<img src="https://www.ancient-hebrew.org/hebrew/heb-anc-sm-' + name + '.jpg"/>': letter for name, letter in name_letter.items()}

# print(image_tags)

print(name_letter)

# Suck the good stuff out of the site
def marrow(url):
    request = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

    page = urlopen(request).read().decode("utf-8")

    soup = Soup(page, "lxml")
    page = str(soup)
    
    print(len(page))
    for tag, letter in image_tags.items():
        page = page.replace(tag, letter)
    print(len(page))

    soup = Soup(page, "lxml")
    body = soup.find("body")

    table = body.find_all("table", recursive=False)[-1]
    meat = table.find("tbody")
    meat = table.find("tr")
    meat = meat.find("td")

    return meat

def get_word(tag):
    text = tag.find("font").text
    # get Hebrew characters 
    return "".join([c for c in text if "\u0590" <= c <= "\u05EA"])

def parse(tag, node_type="root"):
    properties = { node_type: get_word(tag) }
    # print(properties)
    fields = tag.find_all('b', recursive=False)
    for field in fields:
        # print(field)
        property_field = field.text.strip()[:-1].lower()
        property_value = field.next_sibling
        try:
            property_value = property_value.text
        except:
            pass
        # print(property_value)
        property_value = property_value.strip()
        properties[property_field] = property_value
    return properties

roots = {}
url = "https://www.ancient-hebrew.org/ahlb/aleph.html"
meat = marrow(url)

open("text.txt", "w").write(str(meat))

links = ["https://www.ancient-hebrew.org/ahlb/" + a["href"] for a in meat.find("center").find_all("a")]

for link in links:
    meat = marrow(link)
    letter = meat.find_all("center")[1].find("font").find("b").text.split(" - ")[-1].lower()
    letter = name_letter[letter]
    print(letter)

    if letter == "Adopted Roots":
        roots[letter] = {letter: {}}
        parent_root = letter
        child_root = letter
    else:
        print(letter)
        roots[letter] = {}
        parent_root = letter  
        child_root = None
    if letter == "4 letter words" or letter == "Affixes":
        tables = meat.find_all("table", recursive=False)
        tags = [table.find("p") for table in tables]
        for tag in tags:
            roots[letter][get_word(tag)] = parse(tag)
    else:
        for tag in meat.children:
            if tag.name == "p":
                parent_root = get_word(tag)
                if parent_root == "אב":
                    print(tag)
                child_root = parent_root
                roots[letter][parent_root] = {parent_root: parse(tag)}
            elif tag.name == "table":
                children = list(tag.find("tr").children)
                indent = int(children[0]["width"])
                tag = children[1].find("p")
                if indent == 25:
                    #parse as child root
                    child_root = get_word(tag)
                    # print("child", child_root)
                    # print("child root tag", tag)
                    roots[letter][parent_root][child_root] = parse(tag)
                if indent == 50:
                    #parse as word
                    word = get_word(tag)
                    # print("word", word)
                    # print("word node", tag)
                    roots[letter][parent_root][child_root][word] = parse(tag, node_type="word")

json.dump(roots, open("roots.json", "w"), indent=4, ensure_ascii=False)
# open("text", "w").write(meat.prettify())