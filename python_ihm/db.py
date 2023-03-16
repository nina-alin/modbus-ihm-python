import sqlite3
from datetime import datetime

from flask import current_app, g


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


def save_input_register(connection, captor_version, captor_date, temperature):
    computer_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor = connection.cursor()
    cursor.execute('''
    INSERT INTO input_register (CAPTOR_VERSION, CAPTOR_DATE, COMPUTER_DATE, TEMPERATURE)
    VALUES (?, ?, ?, ?);
    ''', (captor_version, captor_date, computer_date, temperature))
    connection.commit()
    cursor.close()


def get_input_register(connection, limit=0, offset=0):
    cursor = connection.cursor()

    if limit != 0:
        cursor.execute(f'''
        SELECT * from input_register
        LIMIT ?
        OFFSET ?
        ;
        ''', (limit, offset))
    else:
        cursor.execute(f'''
        SELECT * from input_register;
        ''')

    data = cursor.fetchall()
    cursor.close()
    return data


def get_input_register_between_date(connection, date_begin, date_end):
    cursor = connection.cursor()
    cursor.execute(f'''
    SELECT * from input_register
    WHERE COMPUTER_DATE BETWEEN(?, ?);
    ''', (date_begin, date_end))
    data = cursor.fetchall()
    cursor.close()
    return data


def get_input_register_under_temperature(connection, temperature):
    cursor = connection.cursor()
    cursor.execute(f'''
    SELECT * from input_register
    WHERE TEMPERATURE < ?;
    ''', temperature)
    data = cursor.fetchall()
    cursor.close()
    return data


def get_input_register_between_temperature(connection, upper_temperature, lower_temperature):
    cursor = connection.cursor()
    cursor.execute(f'''
    SELECT * from input_register
    WHERE TEMPERATURE BETWEEN(?, ?);
    ''', (upper_temperature, lower_temperature))
    data = cursor.fetchall()
    cursor.close()
    return data


def get_input_register_by_captor_version(connection, version):
    cursor = connection.cursor()
    cursor.execute(f'''
    SELECT * from input_register
    WHERE CAPTOR_VERSION = ?;
    ''', version)
    data = cursor.fetchall()
    cursor.close()
    return data