import pymysql

def connect_to_db():
    conn = pymysql.connect(host={hostname}, user={username}, password={password}, db={dbname}, charset='utf8')
    return conn

def create_db_table():
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute('''DROP TABLE todotask''')
        cur.execute('''
                CREATE TABLE todotask (
                task_id INT(4) PRIMARY KEY AUTO_INCREMENT,
                taskname VARCHAR(255) NOT NULL,
                person VARCHAR(255) NOT NULL,
                iscompleted BOOLEAN NOT NULL,
                duedate DATETIME NOT NULL
            );
        ''')
        conn.commit();
    except Exception as e:
        print('db error:', e)
    finally:
        conn.close()

def insert_task(task):
    inserted_task = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO todotask (taskname, person, iscompleted, duedate) VALUES (%s, %s, %s, %s)", (task['taskname'], task['person'], task['iscompleted'], task['duedate']) )
        conn.commit()
        inserted_task = get_task_by_id(cur.lastrowid)
    except Exception as e:
        print('insert error:', e)

    finally:
        conn.close()

    return inserted_task

def get_task_by_id(task_id):
    task = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM todotask WHERE task_id = %s", (task_id,))
        row = cur.fetchone()
        # convert row object to dictionary
        task["task_id"] = row[0]
        task["taskname"] = row[1]
        task["person"] = row[2]
        task["iscompleted"] = row[3]
        task["duedate"] = row[4]

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

def get_tasks():
    tasks = []
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM todotask")
        rows = cur.fetchall()

        # convert row objects to dictionary
        for i in rows:
            task = {}
            task["task_id"] = i[0]
            task["taskname"] = i[1]
            task["person"] = i[2]
            task["iscompleted"] = i[3]
            task["duedate"] = i[4]
            tasks.append(task)

    except:
        tasks = []

    return tasks

def update_task(task):
    updated_task = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("UPDATE todotask SET taskname = %s, person = %s, iscompleted = %s, duedate = %s WHERE task_id =%s", (task['taskname'], task['person'], task['iscompleted'], task['duedate'],task['task_id']) )
        conn.commit()
        #return the task
        updated_task = get_task_by_id(task["task_id"])

    except:
        conn.rollback()
        updated_task = {}
    finally:
        conn.close()

    return updated_task


def delete_task(task_id):
    message = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("DELETE from todotask WHERE task_id = %s", (task_id,))
        conn.commit()
        message["status"] = "Task deleted successfully"
    except:
        conn.rollback()
        message["status"] = "Cannot delete task"
    finally:
        conn.close()
    return message

if __name__ == "__main__":
    create_db_table()
    for task in tasks:
        print(insert_task(task))
    print(get_tasks())