import tkinter as tk
from tkinter import ttk
import sqlite3
from random import choice

conn = sqlite3.connect("study.sqlite")
cur = conn.cursor()
cur.execute("""
                    SELECT  N.id, N.topic, N.sub_topic, N.study_point, T.module
                    FROM NOTES N LEFT JOIN TOPICS T 
                    ON N.topic = T.topic AND N.sub_topic = T.sub_topic;
                    """)
list_notes = list(cur.fetchall())
conn.close()

nums_list = list(map(lambda x: x[0], list_notes))
init_num = choice(nums_list)
init_record = list(filter(lambda x : x[0]==init_num, list_notes))
modules = sorted(list(set(map(lambda x: x[4], list_notes))))


def pick_item():
    global nums_list
    if moduleselectcheckvar.get() == "0":
        select_num = choice(nums_list)
        select_record = list(filter(lambda x : x[0]==select_num, list_notes))
    else:
        nums_list_bymod = list(map(lambda x: x[0], filter(lambda x: x[4]==modulevar.get(), list_notes)))
        select_num = choice(nums_list_bymod)
        select_record = list(filter(lambda x : x[0]==select_num, list_notes))
    module.set(select_record[0][4])
    topic.set(select_record[0][1])
    sub_topic.set(select_record[0][2])
    study_point.set(select_record[0][3])

window = tk.Tk()
window.title("EDUBE Modules 1-5: STUDY GUIDE")
window.geometry("908x730")
window.resizable(width=False, height=False)
window.configure(bg="cornflower blue")

topic = tk.StringVar()
topic.set(init_record[0][1])

sub_topic = tk.StringVar()
sub_topic.set(init_record[0][2])

study_point = tk.StringVar()
study_point.set(init_record[0][3])

frame_upper = tk.Frame(window,
                       padx=5, pady=5,
                       borderwidth=5, relief="ridge")
frame_upper.grid(row=0, column=0, columnspan=3)

frame_middle = tk.Frame(window,
                        borderwidth=5,
                        padx=5, pady=5,
                        relief="ridge")
frame_middle.grid(row=1, column=0, columnspan=3)

modulevar = tk.StringVar()
module = ttk.Combobox(frame_upper, textvariable=modulevar, width=10,
                      font=("Arial", "12", "bold"))
module['values'] = modules
module.set(modules[0])
module.state(["readonly"])
module.grid(row=0, column=0)

moduleselectcheckvar = tk.StringVar()
moduleselectcheckvar.set("0")
module_select = ttk.Checkbutton(frame_upper, text="Select By Module",
                                    variable=moduleselectcheckvar)
module_select.grid(row=0, column=1)

label_topic = tk.Label(frame_upper, textvariable=topic,
                       width=55, height=2,
                       font=("Arial", "22", "underline"))
label_topic.grid(row=1, column=0)

label_sub_topic = tk.Label(frame_upper, textvariable=sub_topic,
                           width=75, height=1,
                           font=("Arial", "16", "italic"))
label_sub_topic.grid(row=2, column=0)

label_study_point = tk.Label(frame_middle, textvariable=study_point,
                             font=("Arial", "28"), relief=tk.RAISED, justify=tk.LEFT,
                             width=55, height=14,
                             foreground="blue4",
                             wraplength=860)
label_study_point.grid(row=0, column=0, columnspan=3)

button_next = tk.Button(window, text="Next Note", padx=4, pady=4,
                        font=("Arial", "12", "bold"), relief=tk.RAISED,
                        command=pick_item)
button_next.grid(row=2, column=1)

button_quit = tk.Button(window, text="Quit", padx=4, pady=4,
                        font=("Arial", "12", "bold"), relief=tk.RAISED,
                        command=window.destroy)
button_quit.grid(row=2, column=2)

window.mainloop()
