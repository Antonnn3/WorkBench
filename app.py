from flask import Flask, render_template, request, redirect, url_for
import webbrowser
import os
import json

app = Flask(__name__)

# File to store tasks
TASK_FILE = "tasks.json"

# Load tasks from file or initialize empty
def load_tasks():
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, 'r') as file:
            return json.load(file)
    return []

# Save tasks to file
def save_tasks(tasks):
    with open(TASK_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)

@app.route('/')
def index():
    tasks = load_tasks()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task_name = request.form['task_name']
    webpage_url = request.form['webpage_url']
    file_path = request.form['file_path']
    filenote_path = request.form['filenote_path']

    tasks = load_tasks()
    tasks.append({
        'name': task_name,
        'webpage_url': webpage_url,
        'file_path': file_path,
        'filenote_path': filenote_path
    })
    save_tasks(tasks)

    return redirect(url_for('index'))

@app.route('/launch/<int:task_id>')
def launch_task(task_id):
    tasks = load_tasks()
    task = tasks[task_id]

    # Open URL
    webbrowser.open(task['webpage_url'])

    # Open file path
    if os.path.exists(task['file_path']):
        os.startfile(task['file_path'])

    # Open filenote
    if os.path.exists(task['filenote_path']):
        os.startfile(task['filenote_path'])

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
