import sqlite3


containers = ["module_1", "module_2", "module_3", "module_4", "module_5"]

module_1 = {"OOP Foundations": ["Classes, Instances, Attributes Methods -- introduction",
                                "Working with class and instance data - instance variables"],
            "OOP Advanced": ["Python core syntax",
                             "Inheritance and polymorphism -- Inheritance as a pillar of OOP",
                             "Extended fucntion argument syntax",
                             "Decorators",
                             "Different faces of Python methods",
                             "Abstract classes",
                             "Encapsulation",
                             "Composition vs inheritance - two ways to the same destination",
                             "Inheriting properties from built-in classes"],
            "Advanced Techniques of Creating and Serving Exceptions": [
                "Advanced Techniquest of Creating and Serving Exceptions"],
            "Object Persistence": ["Shallow and deep copy operatons",
                                   "Serialization of Python objects using the pickle module",
                                   "Making Python objects persistent using the shelve module"],
            "Metaprogramming": ["Metaprogramming"]
            }

module_2 = {"Introduction to PEPs": ["What is PEP?"],
            "PEP 20: The Zen of Python": ["PEP 20 - The Zen of Python"],
            "PEP 8: Style Guide for Python Code": ["PEP 8 - Best Practices and Conventions"],
            "PEP 257, PEP 484, Documentation standards and linters": [
                "PEP 257 - Docstring Conventions, documentation, type hinting, and linters"]
            }

module_3 = {"Tkinter Essentials": ["Python Professional Course Series: GUI Programming",
                                   "Let Tkinter speak!",
                                   "Settling widgets in the window's interior",
                                   "Coloring your widgets",
                                   "A simple GUI application",
                                   "Events and how to handle them",
                                   "Visiting widgets' properties",
                                   "Interacting with widget methods",
                                   "Looking at variables"],
            "Lexicon of Widgets and more Tkinter Essentials": [
                "A small lexicon of widgets - Part 1",
                "A small lexicon of widgets - Part 2",
                "A small lexicon of widgets - Part 3",
                "Shaping the main window and conversing with the user",
                "Working with the canvas"]
            }

module_4 = {"Working with RESTful APIs": ["Basic concepts of network programming",
                                          "How to use sockets in Python",
                                          "Introduction to JSON",
                                          "Using the json module in Python",
                                          "Introduction to XML -- Why do we prefer to use JSON?",
                                          "HTTP made simple -- the request module",
                                          "CRUD -- how to build a simple REST client?"]
            }

module_5 = {"FIle Processing": ["sqlite3 - interacting with SQLite databases",
                                "xml - creating and processing XML files",
                                "csv - CSV file reading and writing",
                                "logging - basics logging facility for Python",
                                "configparser - configuration file parser"]
            }

all_topics = list()

for module in containers:
    for topic, subtopics in eval(module+".items()"):
        for items in subtopics:
            all_topics.append((module, topic, items, False))

create_all_topics_sql = """CREATE TABLE IF NOT EXISTS TOPICS (
                                     id INTEGER PRIMARY KEY,
                                     module TEXT,
                                     topic TEXT,
                                     sub_topic TEXT,
                                     status TEXT);
                                     """

insert_all_topics_sql = """INSERT OR REPLACE INTO TOPICS
                                    (module, topic, sub_topic, status)
                                    VALUES (?, ?, ?, ?);
                                    """

conn = sqlite3.connect("study.sqlite")
cur = conn.cursor()
cur.execute(create_all_topics_sql)
conn.commit()

cur.executemany(insert_all_topics_sql, all_topics)
conn.commit()
conn.close()
