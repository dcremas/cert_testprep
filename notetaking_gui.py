import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
import csv
from datetime import datetime


insert_data_sql = """INSERT OR IGNORE INTO NOTES (topic, sub_topic, study_point)
                               VALUES (?, ?, ?);
                               """

headers = ["id", "topic", "sub_topic", "study_point"]


conn = sqlite3.connect("study.sqlite")
cur = conn.cursor()
cur.execute("""SELECT * FROM TOPICS;""")
topics_data = list(cur.fetchall())
conn.close()

modules = sorted(list(set(map(lambda x: x[1], topics_data))))
topics, subtopics = dict(), dict()
for module in modules:
    topics[module] = sorted(list(set(map(lambda x: x[2], filter(lambda x: x[1]==module, topics_data)))))
topics_list = list()
for strings in topics.values():
    for string in strings:
        topics_list.append(string)
for topic in topics_list:
    subtopics[topic] = sorted(list(set(map(lambda x: x[3], filter(lambda x: x[2]==topic, topics_data)))))


def module_bind(event=None):
    topic['values'] = topics[modulevar.get()]

def topic_bind(event=None):
    subtopic['values'] = subtopics[topicvar.get()]

def subtopic_bind(event=None):
    conn = sqlite3.connect("study.sqlite")
    cur = conn.cursor()
    cur.execute("""SELECT * FROM TOPICS;""")
    topics_data_updated = list(cur.fetchall())
    conn.close()
    subtopic_sel = subtopicvar.get()
    current_status = (list(filter(lambda x: x[3]==subtopic_sel, topics_data_updated)))[0][4]
    if current_status == '0':
        subtopicstatusvar.set("Incomplete")
    else:
        subtopicstatusvar.set("Complete")

def commit_status():
    if messagebox.askyesno("?", "Are your sure\n you would like to update\nthe status of this subtopic?"):
        commit_value = subtopiccheckvar.get()
        conn = sqlite3.connect("study.sqlite")
        cur = conn.cursor()
        cur.execute("""SELECT * FROM TOPICS;""")
        topics_data_current = list(cur.fetchall())
        subtopic_sel = subtopicvar.get()
        current_index = (list(filter(lambda x: x[3]==subtopic_sel, topics_data_current)))[0][0]
        update_sql = """UPDATE TOPICS SET status = ? WHERE id = ?;"""
        params = (commit_value, current_index)
        cur.execute(update_sql, params)
        conn.commit()
        conn.close()
        subtopic_bind()

def commit_record():
    if messagebox.askyesno("?", "Are your sure\n you would like to add\nthis record to the database?"):
        topic_var = topic.get()
        subtopic_var = subtopic.get()
        studypoint_var = text_study_point.get("1.0", tk.END)
        record = (topic_var, subtopic_var, studypoint_var)
        conn = sqlite3.connect("study.sqlite")
        cur = conn.cursor()
        cur.execute(insert_data_sql, record)
        conn.commit()
        conn.close()

def backup_csv():
    if messagebox.askyesno("?", "Are your sure\n you would like to backup\nthe data to a csv file?"):
        now = datetime.strftime(datetime.now(), format="%Y%m%d_%H%M") 
        conn = sqlite3.connect("study.sqlite")
        cur = conn.cursor()
        data_list = list(cur.execute("""SELECT * FROM NOTES;"""))
        with open("extract_files/notes_" + now + ".csv", "w") as file_write:
            writer = csv.writer(file_write)
            writer.writerow(headers)
            writer.writerows(data_list)
        conn.close()

def click_quit():
    if messagebox.askyesno("?", "Are you sure\nyou would like to quit?"):
        window.destroy()
    
window = tk.Tk()
window.title("EDUBE Modules 1-5: NOTES")
window.minsize(width=800, height=400)
window.resizable(width=False, height=False)

frame_1 = tk.Frame(window, padx=5, pady=5)
frame_1.pack()

modulevar = tk.StringVar()
module = ttk.Combobox(frame_1, textvariable=modulevar, width=10,
                      font=("Arial", "12", "bold"))
module['values'] = modules
module.set(modules[0])
module.bind("<<ComboboxSelected>>", module_bind)
module.state(["readonly"])
module.grid(row=0, column=0)

label_topic = tk.Label(frame_1, text="Topic:", padx=5, pady=5, width=10,
                       font=("Arial", "12", "bold"), anchor=tk.W)
label_topic.grid(row=1, column=0)

label_sub_topic = tk.Label(frame_1, text="Sub Topic:", padx=5, pady=5, width=10,
                           font=("Arial", "12", "bold"), anchor=tk.W)
label_sub_topic.grid(row=2, column=0)

label_study_point = tk.Label(frame_1, text="Study Point:", padx=5, pady=5, width=10,
                             font=("Arial", "12", "bold"), anchor=tk.NW)
label_study_point.grid(row=3, column=0)

topicvar = tk.StringVar()
topic = ttk.Combobox(frame_1, textvariable=topicvar, width=75,
                      font=("Arial", "12"))
topic['values'] = topics[modulevar.get()]
topic.set((topics[modules[0]])[0])
topic.bind("<<ComboboxSelected>>", topic_bind)
topic.state(["readonly"])
topic.grid(row=1, column=1)

subtopicvar = tk.StringVar()
subtopic = ttk.Combobox(frame_1, textvariable=subtopicvar, width=75,
                         font=("Arial", "12"))
subtopic['values'] = subtopics[topicvar.get()]
subtopic.set((subtopics[(topics[modules[0]])[0]])[0])
subtopic.bind("<<ComboboxSelected>>", subtopic_bind)
subtopic.state(["readonly"])
subtopic.grid(row=2, column=1)

text_study_point = tk.Text(frame_1, width=77, height=10, font=("Arial", "12"),
                           padx=5, pady=5)
text_study_point.grid(row=3, column=1, rowspan=4)

button_commit = tk.Button(frame_1, text="Commit Record", padx=4, pady=4,
                          font=("Arial", "12"), relief=tk.RAISED, command=commit_record)
button_commit.grid(row=3, column=2)

subtopic_status_label = tk.Label(frame_1, text="Notes Status:", padx=5, pady=5, width=10,
                           font=("Arial", "12", "bold"), anchor=tk.W)
subtopic_status_label.grid(row=7, column=0)

subtopicstatusvar = tk.StringVar(value="Unknown")
subtopic_status = tk.Label(frame_1, textvariable=subtopicstatusvar, padx=5, pady=5, width=10,
                           font=("Arial", "12", "italic"), anchor=tk.W)
subtopic_status.grid(row=8, column=0)

subtopiccheckvar = tk.StringVar()
subtopic_complete = ttk.Checkbutton(frame_1, text="Subtopic Status Change",
                                    variable=subtopiccheckvar)
subtopic_complete.grid(row=7, column=1)

status_commit = tk.Button(frame_1, text="Commit Status", padx=4, pady=4,
                          font=("Arial", "12"), relief=tk.RAISED, command=commit_status)
status_commit.grid(row=8, column=1)

button_backup_csv = tk.Button(frame_1, text="Backup To CSV", padx=4, pady=4,
                          font=("Arial", "12"), relief=tk.RAISED, command=backup_csv)
button_backup_csv.grid(row=9, column=2)

button_quit = tk.Button(frame_1, text="Quit Application", padx=4, pady=4,
                        font=("Arial", "12"), relief=tk.RAISED, command=click_quit)
button_quit.grid(row=10, column=1)

window.mainloop()
