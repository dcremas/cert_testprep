import sqlite3
from wordcloud import WordCloud, STOPWORDS

location = "/Users/dustincremascoli/Documents/prof_cert/testprep/"

conn = sqlite3.connect(location + "study.sqlite")
cur = conn.cursor()
cur.execute("""
            SELECT  N.id, N.topic, N.sub_topic, N.study_point, T.module
            FROM NOTES N LEFT JOIN TOPICS T
            ON N.topic = T.topic AND N.sub_topic = T.sub_topic;
            """)
notes_list = cur.fetchall()
conn.close()

fields_dict = {"modules": 4, "topics": 1, "subtopics": 2}

for key, val in fields_dict.items():
    for item in set(map(lambda x: x[val], notes_list)):
        text = " ".join(list(map(lambda x: x[3].replace("\n", "").lower(),
                                 filter(lambda x: x[val] == item, notes_list))))
        wordcloud = WordCloud(stopwords=STOPWORDS,
                              width=800, height=400,
                              background_color="white",
                              collocations=True).generate(text)
        wordcloud.to_file(location + "wordclouds/" + key + "/" + item + ".pdf")

text_all = " ".join(list(map(lambda x: x[3].replace("\n", "").lower(), notes_list)))
wordcloud_all = WordCloud(stopwords=STOPWORDS,
                          width=800, height=400,
                          background_color="white",
                          collocations=True).generate(text_all)
wordcloud_all.to_file(location + "wordclouds/total.pdf")
