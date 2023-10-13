import sqlite3


setup_data = [("OOP Foundations", "Classes, Instances, Attributes Methods -- introduction",
              "Class - an idea, blueprint, or recipe for an instance"),
              ("OOP Foundations", "Classes, Instances, Attributes Methods -- introduction",
               "Instance - an instantiation of the class; very often used interchangeably with the word 'object'"),
              ("OOP Foundations", "Classes, Instances, Attributes Methods -- introduction",
               "Object - Python's representation of data and methods, objects could be aggregates of instances"),
              ("OOP Foundations", "Classes, Instances, Attributes Methods -- introduction",
               "Attribute - any object or class trait; could be a variable or method"),
              ("OOP Foundations", "Classes, Instances, Attributes Methods -- introduction",
               "Method - A function built into a class or object; some say it's a callable atrribute"),
              ("OOP Foundations", "Classes, Instances, Attributes Methods -- introduction",
               "Type - refers to the class that was used to instantiate the object")
              ]

create_table_sql = """CREATE TABLE IF NOT EXISTS NOTES (
                              id INTEGER PRIMARY KEY,
                              topic TEXT,
                              sub_topic TEXT,
                              study_point TEXT);
                              """

insert_data_sql = """INSERT OR IGNORE INTO NOTES (topic, sub_topic, study_point)
                               VALUES (?, ?, ?);
                               """

conn = sqlite3.connect("study.sqlite")
cur = conn.cursor()

cur.execute(create_table_sql)
conn.commit()

cur.executemany(insert_data_sql, setup_data)
conn.commit()

conn.close()
