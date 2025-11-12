# Starter code for Data Centric Programming Assignment 2025
#Amy Webb C24423456
# os is a module that lets us access the file system

import os 
import mysql.connector
from typing import List, Dict, Any
import pandas as pd

# sqlite for connecting to sqlite databases
def connect_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",        
        password="",       
        database="tunes1"   
    )
    return conn

# An example of how to create a table
def do_databasse_stuff():

    conn = connect_db()
    cursor = conn.cursor()

    # Create table
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS tunes1 (
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



def process_file(file):
    with open(file, 'r') as f:
        lines = f.readlines()
    # list comprehension to strip the \n's
    lines = [line.strip() for line in lines]

    # just print the files for now
    for line in lines:
        # print(line)0
        pass

#
#do_databasse_stuff()

# Iterate over directories in abc_books
for item in os.listdir(books_dir):
    # item is the dir name, this makes it into a path
    item_path = os.path.join(books_dir, item)
    
    # Check if it's a directory and has a numeric name
    if os.path.isdir(item_path) and item.isdigit():
        print(f"Found numbered directory: {item}")
        
        # Iterate over files in the numbered directory
        for file in os.listdir(item_path):
            # Check if file has .abc extension
            if file.endswith('.abc'):
                file_path = os.path.join(item_path, file)
                print(f"  Found abc file: {file}")
                process_file(file_path)


