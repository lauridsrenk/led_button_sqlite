import sqlite3

con = sqlite3.connect("ledstate.db")
cur = con.cursor()
cur.execute("""
    create table ledstate(
        ledstate_id     INTEGER PRIMARY KEY AUTOINCREMENT,
        is_on           INT NOT NULL,
        time_changed    REAL NOT NULL
    );
    """)
con.commit()
con.close()
