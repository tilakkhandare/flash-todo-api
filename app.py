from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('todo.db')
    conn.row_factory = sqlite3.Row  # Allows dictionary-like access to rows
    return conn

# GET all todos
@app.route('/todos', methods=['GET'])
def get_todos():
    conn = get_db_connection()
    todos = conn.execute('SELECT * FROM todos').fetchall()
    conn.close()
    return jsonify([dict(todo) for todo in todos])

# POST a new todo
@app.route('/todos', methods=['POST'])
def add_todo():
    data = request.get_json()
    title = data.get('title')
    if not title:
        return jsonify({'error': 'Title is required'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO todos (title, completed) VALUES (?, ?)', (title, 0))
    conn.commit()
    todo_id = cursor.lastrowid
    conn.close()

    return jsonify({'id': todo_id, 'title': title, 'completed': 0}), 201

# PUT update an existing todo
@app.route('/todos/<int:id>', methods=['PUT'])
def update_todo(id):
    data = request.get_json()
    title = data.get('title')
    completed = data.get('completed')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE todos 
        SET title = COALESCE(?, title), completed = COALESCE(?, completed) 
        WHERE id = ?
    ''', (title, completed, id))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Todo updated successfully'})

# DELETE remove a todo
@app.route('/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM todos WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Todo deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)