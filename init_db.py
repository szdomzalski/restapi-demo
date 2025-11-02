import sqlite3

import config


INITIAL_PEOPLE = [
    "1, 'Fairy', 'Tooth', '2022-10-08 09:15:10'",
    "2, 'Ruprecht', 'Knecht', '2022-10-08 09:15:13'",
    "3, 'Bunny', 'Easter', '2022-10-08 09:15:27'",
]


def init_database() -> None:
    conn = sqlite3.connect(config.basedir / 'people.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS person (
            id INTEGER PRIMARY KEY,
            lname TEXT NOT NULL,
            fname TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    for person in INITIAL_PEOPLE:
        cursor.execute(f'INSERT INTO person (id, lname, fname, timestamp) VALUES ({person})')
    conn.commit()
    cursor.close()


if __name__ == '__main__':
    init_database()