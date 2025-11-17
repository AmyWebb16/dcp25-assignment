# Starter code for Data Centric Programming Assignment 2025
#Amy Webb C24423456
# os is a module that lets us access the file system

import os 
import mysql.connector
import pandas as pd

# connect to mysql server
def connect_db():
    conn = mysql.connector.connect(
        host="10.154.12.37",
        user="root1",        
        password="",       
        database="tunepal"   
        
    )
    return conn

# An example of how to create a table

def do_databasse_stuff():

    conn = connect_db()

do_databasse_stuff()

def query_made():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("Select * from tuneindex")
 
    while True:
        


query_made()