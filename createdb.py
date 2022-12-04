import sqlite3

def connect_to_db():
    conn = sqlite3.connect('database.db')
    return conn

def create_db_table():
    try:
        conn = connect_to_db()
        conn.execute('''DROP TABLE todotask''')
        conn.execute('''
            CREATE TABLE todotask (
                task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                taskname TEXT NOT NULL,
                person TEXT NOT NULL,
                iscompleted INTEGER NOT NULL,
                duedate TEXT NOT NULL
            );
        ''')
        conn.commit()
        print("Todotask table created successfully")
    except:
        print("Todotask table creation failed - Maybe table")
    finally:
        conn.close()

def insert_task(task):
    inserted_task = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO todotask (taskname, person, iscompleted, duedate) VALUES (?, ?, ?, ?)", (task['taskname'], task['person'], task['iscompleted'], task['duedate']) )
        conn.commit()
        inserted_task = get_task_by_id(cur.lastrowid)
    except:
        conn().rollback()

    finally:
        conn.close()

    return inserted_task

def get_task_by_id(task_id):
    task = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM todotask WHERE task_id = ?", (task_id,))
        row = cur.fetchone()

        # convert row object to dictionary
        task["task_id"] = row["task_id"]
        task["taskname"] = row["taskname"]
        task["person"] = row["person"]
        task["iscompleted"] = row["iscompleted"]
        task["duedate"] = row["duedate"]

    except:
        task = {}

    return task

tasks = []
task1 = {
        "taskname": "First task",
        "person": "elena.sim@sap.com",
        "iscompleted": 0,
        "duedate": "2022-12-08",
    }

task2 = {
        "taskname": "Second task",
        "person": "elena.sim@sap.com",
        "iscompleted": 0,
        "duedate": "2022-12-09",
    }

task3 = {
        "taskname": "Third task",
        "person": "elena.sim@sap.com",
        "iscompleted": 0,
        "duedate": "2022-12-10",
    }

task4 = {
        "taskname": "Fourth task",
        "person": "tommy.park@sap.com",
        "iscompleted": 0,
        "duedate": "2022-12-11",
    }

tasks.append(task1)
tasks.append(task2)
tasks.append(task3)
tasks.append(task4)

if __name__ == "__main__": 
    create_db_table()
    for task in tasks:
        insert_task(task)