import csv
import sqlite3

try:

    # Import csv and extract data
    with open('student_info.csv', 'r') as fin:
        dr = csv.DictReader(fin)
        student_info = [(i['NAME'], i['AGE']) for i in dr]
        print(student_info)

    # Connect to SQLite
    sqliteConnection = sqlite3.connect('sql.db')
    cursor = sqliteConnection.cursor()

    # Create student table
    cursor.execute('create table student(name varchar2(10), age int);')

    # Insert data into table
    cursor.executemany(
        "insert into student (name, age) VALUES (?, ?);", student_info)

    # Show student table
    cursor.execute('select * from student;')

    # View result
    result = cursor.fetchall()
    print(result)

    # Commit work and close connection
    sqliteConnection.commit()
    cursor.close()

except sqlite3.Error as error:
    print('Error occurred - ', error)

finally:
    if sqliteConnection:
        sqliteConnection.close()
        print('SQLite Connection closed')