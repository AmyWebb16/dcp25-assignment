# Starter code for Data Centric Programming Assignment 2025
#Amy Webb C24423456
# os is a module that lets us access the file system

import os 
import mysql.connector
import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# connect to mysql server
def connect_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",        
        password="",       
        database="tunes1"   
        
    )
    return conn



def do_databasse_stuff():

    conn = connect_db()
    cursor = conn.cursor()

    # Create table
    cursor.execute("DROP TABLE IF EXISTS tunes1")
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS tunes1 (
        book_number INT,
        X TEXT,
        T Text,
        R TEXT,
        M TEXT,
        L TEXT,
        Q TEXT,
        K TEXT
        )""")
    conn.commit()
    cursor.close()
    conn.close()

def insert_data(book_number, tune):
    conn = connect_db()
    cursor = conn.cursor()

    #insert data into table
    cursor.execute(
        """INSERT INTO tunes1 (book_number, X, T, R, M, L, Q, K) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
        (
            book_number,
            tune.get("X", ""),
            tune.get("T", ""),
            tune.get("R", ""),
            tune.get("M", ""),
            tune.get("L",""),
            tune.get("Q",""),
            tune.get("K","")
        )
    )

    conn.commit()
    cursor.close()
    conn.close()


def process_file(file,book_number):
    with open(file, 'r') as f:
        lines = f.readlines()
    # list comprehension to strip the \n's
    lines = [line.strip() for line in lines]

    tunes = []
    current_tune = {}

   #get files into a list 
    for line in lines:
        if line.startswith("X:"):
            if current_tune:
                tunes.append(current_tune)
                current_tune ={}
        if ":" in line:
            key, value = line.split(":",1)
            current_tune[key.strip()] = value.strip()
    if current_tune:
        tunes.append(current_tune)
    
    for tune in tunes:
        insert_data(book_number, tune)
        pass

def create_UI():
    root = tk.Tk()
    root.geometry("400x300")
    root.title("Treeview Table")

    search_frame = tk.Frame(root)
    search_frame.pack(pady=5)

    table_frame = tk.Frame(root)
    table_frame.pack(fill="both", expand=True)

    columns = ('book_number', 'X', 'T', 'R', 'M', 'L', 'Q', 'K')
    tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=8)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    tree.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")

    table_frame.grid_rowconfigure(0, weight=1)
    table_frame.grid_columnconfigure(0, weight=1)

    return root, search_frame, tree


def get_tunes_by_title():
    conn = connect_db()
    root, search_frame, tree =create_UI()

    label = tk.Label(search_frame, text="Search T:")
    label.pack(side="left", padx=5)

    entry = tk.Entry(search_frame,width=30)
    entry.pack(side="left",padx=5)
    

    def on_click():
        tree.delete(*tree.get_children())

        search = entry.get().strip()
        if not search:
            tk.messagebox.showwarning("Input Required", "Please enter a title")
            return
        
        try:
            query1 = "SELECT * from tunes1 where T  Like %s;"
            df = pd.read_sql(query1,conn,params=[search])

            if df.empty:
                tk.messagebox.showinfo("No Results", f"No records found for '{search}'")
                return
        
            for idx, row in df.iterrows():
                tree.insert("",tk.END,values=list(row))

        except Exception as e:
            tk.messagebox.showerror("Error", f"Database error: {str(e)}")
        

    button = tk.Button(root,text="Click Me", command=on_click)
    button.pack(side="left",padx=5)
    entry.bind('<Return>',lambda e: on_click())
    def on_closing():
        conn.close()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

    pass


def get_all_books():
    conn = connect_db()
    query = "SELECT * from  tunes1"
    df = pd.read_sql(query,conn)
    print(df.head())

def search_tune_book(search_term):
    conn = connect_db()
    query3 = "Select * from tunes1 where book_number = search_term;"
    df = pd.read_sql(query3,conn)
    print(df)
    
    pass

def get_tunes_by_type():
    conn = connect_db()
    query2 = "SELECT * from tunes1 where R = ; "
    df = pd.read_sql(query2,conn)
    print(df)
    pass


do_databasse_stuff()
books_dir = "abc_books"

# Iterate over directories in abc_books
for item in os.listdir(books_dir):
    # item is the dir name, this makes it into a path
    item_path = os.path.join(books_dir, item)
    
    # Check if it's a directory and has a numeric name
    if os.path.isdir(item_path) and item.isdigit():
        print(f"Found numbered directory: {item}")
        book_number = int(item)

        
        # Iterate over files in the numbered directory
        for file in os.listdir(item_path):
            # Check if file has .abc extension
            if file.endswith('.abc'):
                file_path = os.path.join(item_path, file)
                print(f"  Found abc file: {file}")
                process_file(file_path, book_number)



get_tunes_by_book()

