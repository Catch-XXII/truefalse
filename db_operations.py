import sqlite3


def create_sqlite_database(filename):
    """create a database connection to an SQLite database"""
    try:
        with sqlite3.connect(
            filename, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
        ) as conn:
            return conn
    except sqlite3.Error as error:
        print(f"Sqlite DB Connection Error:{error}")


def create_table(conn):
    cursor = conn.cursor()
    print("Connected to SQLite")

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS player(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    age INTEGER NOT NULL,
    phone TEXT UNIQUE NOT NULL,
    score INTEGER NOT NULL ,
    duration REAL NOT NULL,
    date TIMESTAMP NOT NULL);"""
    )
    conn.commit()
    cursor.close()


def insert_into_table(conn, player, delta_time):
    cursor = conn.cursor()
    print("Connected to SQLite")

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS player(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    age INTEGER NOT NULL,
    phone TEXT UNIQUE NOT NULL,
    score INTEGER NOT NULL ,
    duration REAL NOT NULL,
    date TIMESTAMP NOT NULL);"""
    )

    cursor.execute(
        "INSERT INTO player (name, email, age, phone, score, duration, date) values(?, ?, ?, ?, ?, ?, ?)",
        (
            player.name,
            player.email,
            player.age,
            player.phone,
            player.score,
            delta_time,
            player.date,
        ),
    )
    conn.commit()
    cursor.close()


def fetch_score_board(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM player ORDER BY duration ASC")
    rows = cursor.fetchall()
    print(
        "{:-^4s}{:_^30s}{:@^30s}{:-^7s}{:#^12s}{:-^9s}{:*^12s}{:~^26s}".format(
            "No", "Name", "E-mail", "Age", "Number", "Score", "Duration", "Date"
        )
    )
    for row in rows:
        print(
            "{:^4d}{:<30s}{:<30s}{:^7d}{:<12s}{:^9d}{:^12.2f}{:^26s}".format(
                row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]
            )
        )

    conn.commit()
    cursor.close()
