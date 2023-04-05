# RUN PYTHON FILE TO START USER INTERFACE
import tkinter as tk
import text2dm
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import scrolledtext
from tkinter import ttk
from tkinter import *


def open_file():
    # function to open a text file with a textual description
    filepath = askopenfilename(filetypes=[("Text Files", "*.txt")])
    if not filepath:
        return
    txt_edit.delete("1.0", tk.END)
    with open(filepath, "r") as input_file:
        text = input_file.read()
        txt_edit.insert(tk.END, text)
    window.title(f"Text2DM - {filepath}")


def classify():
    # refresh fields
    txt2_edit.delete("1.0", "end")
    position = tk.END

    # get input text
    text = txt_edit.get("1.0", position)

    # get classification
    df_classified = text2dm.classification(text)

    # function to save classification table
    def save_classification():
        filepath = asksaveasfilename(defaultextension='.csv', filetypes=[("CSV Files", "*.csv")])
        if not filepath:
            return
        df_classified.to_csv(filepath, index=False, header=True)

    # initialize frame and widgets
    fr_classification_table = tk.Frame(window)
    fr_classification_table.grid(row=2, column=0, sticky="nsew")  # sticky = nsew to fit entire space
    fr_classification_table.rowconfigure(0, weight=1)
    fr_classification_table.columnconfigure(0, weight=1)
    btn_save_classification = tk.Button(fr_classification_table, text="Save", command=save_classification)
    btn_save_classification.grid(column=0, row=1)

    # convert df to tuples
    tuples = [tuple(x) for x in df_classified.to_numpy()]

    # create scrollbar
    tree_scroll = tk.Scrollbar(fr_classification_table)
    tree_scroll.grid(row=0, column=1, sticky='ns')

    # create treeview (table)
    my_tree = ttk.Treeview(fr_classification_table, yscrollcommand=tree_scroll.set, columns=(1, 2), show="headings", height=5)
    my_tree.grid(row=0, column=0, sticky='nsew')

    # configure scrollbar
    tree_scroll.config(command=my_tree.yview)

    # create headings
    my_tree.heading(1, text="Sentence", anchor=W)
    my_tree.heading(2, text="Prediction", anchor=W)
    my_tree.column(1, minwidth=0, width=400, stretch=True)
    my_tree.column(2, minwidth=0, width=82, stretch=False)

    # add data
    for i in range(0, len(tuples)):
        if tuples[i][1] == "irrelevant":
            my_tree.insert(parent='', index='end', iid=i, text="", values=(tuples[i]), tags="red")

        elif tuples[i][1] == "dependency":
            my_tree.insert(parent='', index='end', iid=i, text="", values=(tuples[i]), tags="blue")

        elif tuples[i][1] == "logic":
            my_tree.insert(parent='', index='end', iid=i, text="", values=(tuples[i]), tags="green")

        else:
            my_tree.insert(parent='', index='end', iid=i, text="", values=(tuples[i]))

    # color cells
    my_tree.tag_configure("red", foreground="red")
    my_tree.tag_configure("blue", foreground="blue")
    my_tree.tag_configure("green", foreground="green")

    # new text
    txt2_edit.tag_configure("red", foreground="red")
    txt2_edit.tag_configure("blue", foreground="blue")
    txt2_edit.tag_configure("green", foreground="green")

    # to not start with a space
    if tuples[0][1] == "irrelevant":
        txt2_edit.insert(tk.END, str(tuples[0][0]), "red")

    elif tuples[0][1] == "dependency":
        txt2_edit.insert(tk.END, str(tuples[0][0]), "blue")

    elif tuples[0][1] == "logic":
        txt2_edit.insert(tk.END, str(tuples[0][0]), "green")

    # for next sentences first a space
    for i in range(1, len(tuples)):
        if tuples[i][1] == "irrelevant":
            txt2_edit.insert(tk.END, " " + str(tuples[i][0]), "red")

        elif tuples[i][1] == "dependency":
            txt2_edit.insert(tk.END, " " + str(tuples[i][0]), "blue")

        elif tuples[i][1] == "logic":
            txt2_edit.insert(tk.END, " " + str(tuples[i][0]), "green")


def get_drd():
    # function to "Build DRD TUPLE"
    # start with empty text field when clicking on "build drd"
    user_intervention.delete("1.0", "end")
    drd.delete("1.0", "end")

    position = tk.END
    text = txt2_edit.get("1.0", position)
    drd_tuple, set_concepts, set_dependencies = text2dm.text2drd(text)

    # function to save list of concepts, dependency and drd tuple of the form (I, D, R)
    def save_drd():
        # function to save the output as a text file
        filepath = asksaveasfilename(defaultextension="txt", filetypes=[("Text Files", "*.txt")])
        if not filepath:
            return
        with open(filepath, "w") as output_file:
            text = "SET OF CONCEPTS = " + str(set_concepts) + "\n" + "\n" + "\n" + "SET OF INPUT ITEMS (I) = " + str(drd_tuple[0]) + "\n" + "\n" + "\n" + "SET OF DECISIONS (D) = " + \
                   str(drd_tuple[1]) + "\n" + "\n" + "\n" + "SET OF DEPENDENCY TUPLES (R) = " + str(set_dependencies) + "\n" + "\n" + "\n" + "DRD TUPLE (I, D, R) = " + str(drd_tuple)
            output_file.write(text)
        window.title(f"DRD Extractor - {filepath}")

    # make save button
    fr_buttons3 = tk.Frame(fr_drd_tuple, height=15)
    fr_buttons3.grid(row=1, column=0)
    btn_save_tuple = tk.Button(fr_buttons3, text="Save", command=save_drd)
    btn_save_tuple.grid(column=0, row=0)

    # insert text
    user_intervention.tag_configure("red", foreground="red")
    user_intervention.insert(tk.END, "USER INTERVENTION", "red")
    user_intervention.insert(tk.END, "\n" + "Are these the unique and correct concepts?" + "\n" + "If you notice incorrect concepts or duplicates in the form of synonyms or different notations " + "\n" + "=> adjust colored text and and build drd tuple again." + "\n")
    user_intervention.insert(tk.END, "\n"+ "\n")

    user_intervention.insert(tk.END, "LIST OF CONCEPTS" + "\n")
    for concept in set_concepts:
        user_intervention.insert(tk.END, str(concept) + "\n")
    user_intervention.insert(tk.END, "\n" + "\n")

    user_intervention.insert(tk.END, "Your dependencies can further help you to identify incorrect concepts." + "\n" + "\n")

    user_intervention.insert(tk.END, "LIST OF DEPENDENCY TUPLES" + "\n")
    for dep in set_dependencies:
        user_intervention.insert(tk.END, str(dep) + "\n")
    user_intervention.insert(tk.END, "\n" + "\n")

    drd.insert(tk.END, "DRD TUPLE" + "\n" + str(drd_tuple) + "\n")


def get_graph():
    # function that gives drd graph in pop up window + also saved under "drd's interface"
    position = tk.END
    text = txt2_edit.get("1.0", position)
    drd_tuple, set_concepts, set_dependencies = text2dm.text2drd(text)
    dot, final_decision_id = text2dm.drd_graph_construction.tuple2graph(drd_tuple)
    dot.format = 'pdf'

    dot.render("drd's interface/DRD_" + final_decision_id, view=True)


def get_logic():
    # get input
    position = tk.END
    text = txt2_edit.get("1.0", position)

    # get logic table
    df_logic = text2dm.extract_logic_table(text)

    # function to save classification table
    def save_logic():
        filepath = asksaveasfilename(defaultextension='.csv', filetypes=[("CSV Files", "*.csv")])
        if not filepath:
            return
        df_logic.to_csv(filepath, index=False, header=True)

    # function to "Get logic table"
    fr_logic_table = tk.Frame(window)
    fr_logic_table.grid(row=2, column=1, sticky="nsew")
    fr_logic_table.rowconfigure(0, weight=1)
    fr_logic_table.columnconfigure(0, weight=1)
    btn_save_logic = tk.Button(fr_logic_table, text="Save", command=save_logic)
    btn_save_logic.grid(column=0, row=1)

    # convert df to tuples
    tuples = [tuple(x) for x in df_logic.to_numpy()]

    # create scroll bar
    tree_scroll = tk.Scrollbar(fr_logic_table)
    tree_scroll.grid(row=0, column=1, sticky='ns')

    # create treeview object (table)
    my_tree = ttk.Treeview(fr_logic_table, yscrollcommand=tree_scroll.set, columns=(1, 2, 3, 4), show="headings",
                           height=5)
    my_tree.grid(row=0, column=0, sticky='nsew')
    my_tree.rowconfigure(0, weight=1)
    my_tree.columnconfigure(0, weight=1)

    # configure scrollbar
    tree_scroll.config(command=my_tree.yview)

    # create headings
    my_tree.heading(1, text="Conditional clause", anchor=W)
    my_tree.heading(2, text="Exception clause", anchor=W)
    my_tree.heading(3, text="Consequence clause", anchor=W)
    my_tree.heading(4, text="Else clause", anchor=W)

    my_tree.column(1, minwidth=0, width=100, stretch=True)
    my_tree.column(2, minwidth=0, width=100, stretch=True)
    my_tree.column(3, minwidth=0, width=100, stretch=True)
    my_tree.column(4, minwidth=0, width=100, stretch=True)

    # add data
    for i in range(0, len(tuples)):
        my_tree.insert(parent='', index='end', iid=i, text="", values=(tuples[i]))


window = tk.Tk()
window.title('Playground for decision model extraction tasks')
window.geometry("1200x800")  # measurements window to start with

window.rowconfigure(0, minsize=100, pad=3, weight=1)
window.rowconfigure(1, minsize=100, pad=3, weight=1)
window.rowconfigure(2, minsize=150, pad=3, weight=1)
window.columnconfigure(0, minsize=300, weight=1)
window.columnconfigure(1, minsize=300, weight=1)

fr_txt_edit = tk.Frame(window)
fr_txt_edit.grid(row=0, column=0, sticky="nsew")
fr_txt_edit.rowconfigure(0, weight=1)  # stretchable
fr_txt_edit.columnconfigure(0, weight=1)  # stretchable
txt_edit = scrolledtext.ScrolledText(fr_txt_edit, wrap=tk.WORD, font=("Arial", 14))
txt_edit.grid(row=0, column=0, sticky="nsew")

fr_buttons1 = tk.Frame(fr_txt_edit, height=15)
fr_buttons1.grid(row=1, column=0)
btn_open = tk.Button(fr_buttons1, text="Open text file", command=open_file)
btn_classify = tk.Button(fr_buttons1, text="Classify text", command=classify)
btn_open.grid(row=0, column=0)
btn_classify.grid(row=0, column=1)

fr_txt_edit2 = tk.Frame(window)
fr_txt_edit2.grid(row=1, column=0, sticky="nsew")
fr_txt_edit2.rowconfigure(0, weight=1)
fr_txt_edit2.columnconfigure(0, weight=1)
txt2_edit = scrolledtext.ScrolledText(fr_txt_edit2, wrap=tk.WORD, font=("Arial", 14))
txt2_edit.grid(row=0, column=0, sticky="nsew")

fr_buttons2 = tk.Frame(fr_txt_edit2, height=15)
fr_buttons2.grid(row=1, column=0)
btn_build_drd = tk.Button(fr_buttons2, text="Build DRD tuple", command=get_drd)
btn_graph = tk.Button(fr_buttons2, text="Get DRD graph", command=get_graph)
btn_logic = tk.Button(fr_buttons2, text="Build logic table", command=get_logic)
btn_build_drd.grid(row=0, column=1, sticky="ew", padx=5)
btn_graph.grid(row=0, column=2, sticky='ew', padx=5)
btn_logic.grid(row=0, column=3, sticky="ew", padx=5)

fr_user_intervention = tk.Frame(window)
fr_user_intervention.grid(row=0, column=1, sticky="nsew")
fr_user_intervention.rowconfigure(0, weight=1)
fr_user_intervention.columnconfigure(0, weight=1)
user_intervention = scrolledtext.ScrolledText(fr_user_intervention, wrap=tk.WORD, font=("Arial", 14))
user_intervention.grid(row=0, column=0, sticky="nsew")

fr_drd_tuple = tk.Frame(window)
fr_drd_tuple.grid(row=1, column=1, sticky="nsew")
fr_drd_tuple.rowconfigure(0, weight=1)
fr_drd_tuple.columnconfigure(0, weight=1)
drd = scrolledtext.ScrolledText(fr_drd_tuple, wrap=tk.WORD, font=("Arial", 14))
drd.grid(column=0, row=0, sticky="nsew")

window.mainloop()
