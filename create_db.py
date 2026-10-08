import sqlite3


def create_table():
    """
    The create_table function creates a non-existing table.
    """
    my_conn = sqlite3.connect("moneypal_db.db")
    my_cur = my_conn.cursor()

    # Create the Clients table
    my_cur.execute("""CREATE TABLE IF NOT EXISTS Clients (
        clientID INTEGER PRIMARY KEY AUTOINCREMENT,
        firstName VARCHAR(50) NOT NULL,
        lastName VARCHAR(50) NOT NULL,
        age INTEGER NULL,
        password VARCHAR(100) NOT NULL,
        incomes FLOAT NOT NULL DEFAULT 0,
        expenses FLOAT NOT NULL DEFAULT 0,
        assetsAmount FLOAT DEFAULT 0,
        debtsAmount FLOAT DEFAULT 0,
        balance FLOAT,
        accountType VARCHAR(50) NULL,
        notes TEXT NULL
    );""")

    # Begin the counting of clientIDs from 101
    my_cur.execute("""
        INSERT OR IGNORE INTO sqlite_sequence (name, seq)
        VALUES ('Clients', 100);
    """)

    my_conn.commit()
    my_conn.close()
