import psycopg2
from constants import *

def create_db():
    conn = psycopg2.connect(host=DB_HOST,database=DB_NAME, user=DB_USER, password=DB_PASS)
    cur = conn.cursor()    
    # cur.execute(""" INSERT INTO users (username, pass) VALUES (%s,%s)""", ("anas", "anas"))
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
        id SERIAL PRIMARY KEY,
        username varchar(100) NOT NULL UNIQUE,
        email varchar(100),
        phone varchar(15),
        pass varchar NOT NULL
    );""")
    cur.execute("""CREATE TABLE IF NOT EXISTS inventory(
        id bigint NOT NULL PRIMARY KEY,
        pr_name varchar(250) NOT NULL,
        stocks INTEGER NOT NULL,
        cost_price DECIMAL NOT NULL,
        sell_price DECIMAL NOT NULL,
        c_gst DECIMAL,
        s_gst DECIMAL,
        ven_name varchar(100),
        ven_num varchar(100),
        ven_purchase_mode varchar(100)
    );""")
    cur.execute("""CREATE TABLE IF NOT EXISTS paymode(
        id SERIAL PRIMARY KEY,
        name varchar(100) NOT NULL,
        percentage DECIMAL NOT NULL
    );""")
    cur.execute("""CREATE TABLE IF NOT EXISTS customer(
        id SERIAL PRIMARY KEY,
        name varchar(100) NOT NULL,
        num varchar(12),
        address varchar(250)
    );""")
    cur.execute("""CREATE TABLE IF NOT EXISTS bill(
        id SERIAL PRIMARY KEY,
        cus_id INTEGER NOT NULL,
        pr_id bigint NOT NULL,
        paid boolean NOT NULL,
        date DATE NOT NULL,
        quantity INTEGER NOT NULL,
        pur_mode INTEGER,
        inv_id INTEGER,
        FOREIGN KEY (cus_id) REFERENCES customer(id),
        FOREIGN KEY (pr_id) REFERENCES inventory(id),
        FOREIGN KEY (pur_mode) REFERENCES paymode(id)
    );""")
    cur.execute("""CREATE TABLE IF NOT EXISTS billdetails(
        id SERIAL PRIMARY KEY,
        cus_id INTEGER NOT NULL,
        date DATE NOT NULL,
        total_amount DECIMAL NOT NULL,
        bill_file_name varchar(100) NOT NULL
    );""")
    conn.commit()
    cur.close()
    conn.close()

create_db()