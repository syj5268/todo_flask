from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql

def connect_to_db():
    conn = pymysql.connect(host={hostname}, user={username}, password={password}, db={dbname}, charset='utf8')
    return conn

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

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return 'Todo task rest api'

@app.route('/api/tasks', methods=['GET'])
def api_get_tasks():
    return jsonify(get_tasks())

@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def api_get_task(task_id):
    return jsonify(get_task_by_id(task_id))

@app.route('/api/tasks/add',  methods = ['POST'])
def api_add_task():
    task = request.get_json()
    return jsonify(insert_task(task))

@app.route('/api/tasks/update',  methods = ['PUT'])
def api_update_task():
    task = request.get_json()
    return jsonify(update_task(task))

@app.route('/api/tasks/delete/<int:task_id>',  methods = ['DELETE'])
def api_delete_task(task_id):
    return jsonify(delete_task(task_id))