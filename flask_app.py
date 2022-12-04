import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS
#from waitress import serve

def connect_to_db():
    conn = sqlite3.connect('database.db')
    return conn

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

def get_tasks():
    tasks = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM todotask")
        rows = cur.fetchall()

        # convert row objects to dictionary
        for i in rows:
            task = {}
            task["task_id"] = i["task_id"]
            task["taskname"] = i["taskname"]
            task["person"] = i["person"]
            task["iscompleted"] = i["iscompleted"]
            task["duedate"] = i["duedate"]
            tasks.append(task)

    except:
        tasks = []

    return tasks


def update_task(task):
    updated_task = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("UPDATE todotask SET taskname = ?, person = ?, iscompleted = ?, duedate = ? WHERE task_id =?", (task['taskname'], task['person'], task['iscompleted'], task['duedate'],task['task_id']) )
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
        conn.execute("DELETE from todotask WHERE task_id = ?", (task_id,))
        conn.commit()
        message["status"] = "Task deleted successfully"
    except:
        conn.rollback()
        message["status"] = "Cannot delete task"
    finally:
        conn.close()

    return message

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/')
def home():
    return 'Todo task rest api'

@app.route('/api/tasks', methods=['GET'])
def api_get_tasks():
    return jsonify(get_tasks())

@app.route('/api/tasks/<task_id>', methods=['GET'])
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

@app.route('/api/tasks/delete/<task_id>',  methods = ['DELETE'])
def api_delete_task(task_id):
    return jsonify(delete_task(task_id))


if __name__ == "__main__":
    app.run()
    #serve(app, host="0.0.0.0", port=8080)