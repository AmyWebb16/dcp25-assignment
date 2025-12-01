# Starter code for Data Centric Programming Assignment 2025
#Amy Webb C24423456
# os is a module that lets us access the file system

import os 
import mysql.connector
import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
import re 

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
        O TEXT,
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
        """INSERT INTO tunes1 (book_number, X, T, R, O,M, L, Q, K) VALUES (%s, %s, %s,%s, %s, %s, %s, %s, %s)""",
        (
            book_number,
            tune.get("X", ""),
            tune.get("T", ""),
            tune.get("R", ""),
            tune.get("O", ""),
            tune.get("M", ""),
            tune.get("L",""),
            tune.get("Q",""),
            tune.get("K","")
        )
    )

    conn.commit()
    cursor.close()
    conn.close()

abc_encoding_LOOKUP ={
    #grave
    '\\`A': 'À', '\\`a': 'à', '\\`E': 'È', '\\`e': 'è', 
    '\\`I': 'Ì', '\\`i': 'ì', '\\`O': 'Ò', '\\`o': 'ò',
    '\\`U': 'Ù', '\\`u': 'ù',

    #acute
    "\\'A": 'Á', "\\'a": 'á', "\\'E": 'É', "\\'e": 'é',
    "\\'I": 'Í', "\\'i": 'í', "\\'O": 'Ó', "\\'o": 'ó',
    "\\'U": 'Ú', "\\'u": 'ú', "\\'Y": 'Ý', "\\'y": 'ý',

    #circumflex
    '\\^A': 'Â', '\\^a': 'â', '\\^E': 'Ê', '\\^e': 'ê',
    '\\^I': 'Î', '\\^i': 'î', '\\^O': 'Ô', '\\^o': 'ô',
    '\\^U': 'Û', '\\^u': 'û',

    #tilde
    '\\~A': 'Ã', '\\~a': 'ã', '\\~N': 'Ñ', '\\~n': 'ñ',
    '\\~O': 'Õ', '\\~o': 'õ',

    #umlauts
    '\\"A': 'Ä', '\\"a': 'ä', '\\"E': 'Ë', '\\"e': 'ë',
    '\\"I': 'Ï', '\\"i': 'ï', '\\"O': 'Ö', '\\"o': 'ö',
    '\\"U': 'Ü', '\\"u': 'ü', '\\"Y': 'Ÿ', '\\"y': 'ÿ',

    #cedilla
    '\\cC': 'Ç', '\\cc': 'ç',

    #ring
    '\\AA': 'Å', '\\aa': 'å',

    #slash
    '\\/O': 'Ø', '\\/o': 'ø',

    #breve
    '\\uA': 'Ă', '\\ua': 'ă', '\\uE': 'Ĕ', '\\ue': 'ĕ',

    #caron
    '\\vS': 'Š', '\\vs': 'š', '\\vZ': 'Ž', '\\vz': 'ž',
    '\\vC': 'Č', '\\vc': 'č',

    #double acute
    '\\HO': 'Ő', '\\Ho': 'ő', '\\HU': 'Ű', '\\Hu': 'ű',

    #ligatures
    '\\ss': 'ß', '\\AE': 'Æ', '\\ae': 'æ', '\\oe': 'œ', '\\OE': 'Œ',
}
def decode(text):
    """Decode ABC notation special character to Unicode using LOOKUP table"""
    if not text:
        return text
    
    decoded_text=text

    sorted_keys =sorted(abc_encoding_LOOKUP.keys(), key=len, reverse=True)

    for encoding in sorted_keys:
        if encoding in decoded_text:
            decoded_text=decoded_text.replace(encoding,abc_encoding_LOOKUP[encoding])

    return decoded_text

def process_file(file,book_number):
    """Modifeied to decode abc encodings using LOOKUP table"""

    with open(file, 'r', encoding='utf-8') as f:
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
            decoded_value= decode(value.strip())
            current_tune[key.strip()] = decoded_value
    if current_tune:
        tunes.append(current_tune)
    
    for tune in tunes:
        insert_data(book_number, tune)
        pass

#create a ui for search bar functions later on
def create_UI():
    root = tk.Tk()
    root.geometry("400x300")
    root.title("Treeview Table")

    search_frame = tk.Frame(root)
    search_frame.pack(pady=5)

    table_frame = tk.Frame(root)
    table_frame.pack(fill="both", expand=True)

    columns = ('book_number', 'X', 'T', 'R','O', 'M', 'L', 'Q', 'K')
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

#search a tune by the title (partial)
def search_tune_title():
    conn = connect_db()
    root, search_frame, tree =create_UI()

    label = tk.Label(search_frame, text="Search by Title:")
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
            query1 = "SELECT * from tunes1 where T Like %s;"
            df = pd.read_sql(query1,conn,params=[f"%{search}%"])

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
    root, search_frame, tree = create_UI()

    root.title("All Tunes")
    root.geometry("400x300")

    search_frame.pack_forget()

    title_label = tk.Label(
        root,
        text="All Tunes from Table"
    )
    title_label.pack(side="top",pady=10)

    info_frame = tk.Frame(root)
    info_frame.pack(side="top",pady=5)
    

    record_label = tk.Label(
        info_frame,
        text="loading"
    )
    record_label.pack()

    try:
        query = "SELECT * from  tunes1"
        df = pd.read_sql(query,conn)

        for idx, row in df.iterrows():
            tree.insert("", tk.END, values=list(row))
            record_label.config(text=f"Total records {len(df)}")

    except Exception as e:
        messagebox.showerror("Error")
        record_label.config(text="error")

    btn_close = tk.Button(
        root,
        text="Close",
        command=lambda:[conn.close(), root.destroy()],
        width=20,
        height=5,
        bg="#38A5FF",
        fg="#000000",
        bd=5
    )
    btn_close.pack(pady=10)

    def on_closing():
        conn.close()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

    

#search a tune by the book number
def search_tune_book():
    conn = connect_db()
    root, search_frame, tree = create_UI()

    label = tk.Label(search_frame, text="Search by Book Number:")
    label.pack(side="left", padx=5)

    entry = tk.Entry(search_frame, width=30)
    entry.pack(side="left", padx=5)

    def on_click():
        tree.delete(*tree.get_children())  
        search = entry.get().strip()

        if not search:
            messagebox.showwarning("Input Required", "Please enter a book number") 
            return

        try:
            book_numer = int(search)
            query = "SELECT * FROM tunes1 WHERE book_number = %s;"
            df = pd.read_sql(query, conn, params=[search])

            if df.empty:
                messagebox.showinfo("No Results", f"No records found for '{search}'")
                return

            for _, row in df.iterrows():
                tree.insert("", tk.END, values=list(row))

        except Exception as e:
            messagebox.showerror("Error", f"Database error: {str(e)}")

    button = tk.Button(search_frame, text="Search", command=on_click)
    button.pack(side="left", padx=5)
    entry.bind('<Return>', lambda e: on_click())

    def on_closing():
        conn.close()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


    pass

def piechart_tune_type():
    conn = connect_db()
    query2 = "SELECT R from tunes1;"
    df = pd.read_sql(query2,conn,)
    
    type_counts = df['R'].value_counts().head(15)

    plt.figure(figsize=(10,6))
    plt.pie(type_counts.values, labels=type_counts.index, autopct='%1.2f%%')
    plt.title('Pie Chart of Top 15 Tune Types')
    plt.show()

    conn.close()
    pass

#creates a bar chart of the top 10 origins anf the count of tunes for each
def barchart_top10_origins():
    conn = connect_db()
    try:
        
        cursor = conn.cursor()
        cursor.execute("SELECT O FROM tunes1;")
        rows = cursor.fetchall()
        df = pd.DataFrame(rows, columns=["O"])

        origin_counts = df["O"].value_counts().head(11)
        origin_counts=origin_counts.iloc[1:11]
        print(origin_counts)

        colours=["#FF0000","#FE5D00", "#FFFF00","#0CF200","#2C8503","#00BBFF","#001AFF","#B700FF","#FF00EE","#F96AC0"]

        plt.figure(figsize=(10, 6))
        origin_counts.sort_values().plot(kind='barh', color=colours, edgecolor='black')

        plt.title("Top 10 Country Origins", fontsize=14, fontweight='bold')
        plt.xlabel("Number of Tunes", fontsize=12)
        plt.ylabel("Origin", fontsize=12)
        plt.grid(axis='x', linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.savefig("grid1.png")
        plt.show()
        
    finally:
        conn.close()

def create_menu():
    menu_window = tk.Tk()
    menu_window.title("Tunes Database")
    menu_window.geometry("500x500")
    menu_window.configure(bg='#ffffff')

    title_label = tk.Label(
        menu_window,
        text="Tunes Database",
        bg='#ffffff',
        fg='#000000'
    )
    title_label.pack(pady=20)

    button_frame = tk.Frame(menu_window, bg='#ffffff')
    button_frame.pack(pady=10)

    button_style = {
        'width':30,
        'height':2,
        'font': ("Arial", 10),
        'bg': "#8aedff",
        'fg': "#000000",
        'bd': 3
    }
    btn_all_tunes= tk.Button(
        button_frame,
        text="Show all Tunes",
        command=get_all_books,
        **button_style
    )
    btn_all_tunes.pack(pady=5)


    btn_search_title =tk.Button(
        button_frame,
        text="Search Tunes by Title",
        command= search_tune_title,
        **button_style
    )
    btn_search_title.pack(pady=5)

    btn_search_book=tk.Button(
        button_frame,
        text="Search Tunes by book number",
        command=search_tune_book,
        **button_style
    )
    btn_search_book.pack(pady=5)

    btn_barchart = tk.Button(
        button_frame,
        text="Top 10 Origins Chart",
        command=barchart_top10_origins,
        **button_style
    )
    btn_barchart.pack(pady=5)

    btn_piechart=tk.Button(
        button_frame,
        text="Piechart of 15 top types of Tune",
        command=piechart_tune_type,
        **button_style
    )
    btn_piechart.pack(pady=5)

    btn_exit= tk.Button(
        button_frame,
        text="Exit",
        command=menu_window.quit,
        width=30,
        height=5,
        font=("Arial",10),
        bg="#67e2f8",
        fg='black',
        bd=3
    )
    btn_exit.pack(pady=15)
    menu_window.mainloop()


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



#search_tune_title()
#barchart_top10_origins()
#search_tune_book()
#piechart_tune_type() NEED TO DO
create_menu()

