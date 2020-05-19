from flask import Flask, request, jsonify, abort, flash
import unicodedata as unicode

app = Flask(__name__)

# List As A Temp Storage
mytasks = []

# GET Whole List
@app.route('/api/tasks', methods=['GET'])
def get():
    return jsonify({'mytasks': mytasks})

# GET One Entry By ID
@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in mytasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'mytasks': task[0]})

# POST New Entry To MyTasks
@app.route('/api/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': request.json['id'],
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    mytasks.append(task)
    return jsonify({'task': task}), 201

# PUT Modified Entry
@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = [task for task in mytasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get(
        'description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})

# DELETE One Entry From MyTasks List
@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = [task for task in mytasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    mytasks.remove(task[0])
    return jsonify({'result': True, 'mytasks': task[0]})

if __name__ == '__main__':
    app.run(debug=True)
