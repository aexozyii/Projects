
import sqlite3 as sql

def listExtension():
    con = sql.connect("Databases/tables.db")
    cur = con.cursor()
    data = cur.execute("SELECT * FROM users").fetchall()
    con.close()
    return data
