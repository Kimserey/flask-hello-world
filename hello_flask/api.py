from . import app
from flask import Flask, jsonify,request
from marshmallow import Schema, fields, ValidationError, post_load

class Todo:
    def __init__(self, name, task):
        self.name = name
        self.task = task

todos = {}

### SCHEMAS ###

def must_not_be_blank(data):
    if not data:
        raise ValidationError('Data not provided.')

class TodoSchema(Schema):
    name = fields.Str(validate=must_not_be_blank)
    task = fields.Str(validate=must_not_be_blank)

    @post_load
    def make_todo(self, data):
        return Todo(data['name'], data['task'])

todo_schema = TodoSchema()

### API ###

@app.route("/")
def home():
  return "Hello, Flask!"

@app.route('/todos/<string:todo_id>')
def get_todo(todo_id):
    if todo_id not in todos:
        return jsonify({'message': '{} not found.'.format(todo_id)}), 404
    todo_result = todo_schema.dump(todos[todo_id])
    return jsonify(todo_result)

@app.route('/todos/', methods=['POST'])
def post_todo():
    json_data = request.get_json()
    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400
    try:
        data = todo_schema.load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    todos[data.name] = data
    return '', 200