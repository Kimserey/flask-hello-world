from flask import Flask, jsonify, request, g
from marshmallow import Schema, ValidationError, fields, post_load

from . import app
from . import storage

### SCHEMAS ###

def must_not_be_blank(data):
    if not data:
        raise ValidationError('Data not provided.')

class Todo:
    def __init__(self, name, task):
        self.name = name
        self.task = task

class TodoSchema(Schema):
    name = fields.Str(validate=must_not_be_blank)
    task = fields.Str(validate=must_not_be_blank)

    @post_load
    def make_todo(self, data):
        return Todo(data['name'], data['task'])

todo_schema = TodoSchema()

### API ###

@app.before_request
def before_request():
    g.db = storage.db
    g.db.connect()

@app.after_request
def after_request(response):
    g.db.close()
    return response

@app.route("/")
def home():
    return "Hello, Flask!"

@app.route('/todos/<string:name>')
def get_todo(name):
    todo = storage.Todo.get_by_id(name)
    result = todo_schema.dump(todo)
    return jsonify(result)

@app.route('/todos/', methods=['POST'])
def post_todo():
    json_data = request.get_json()
    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400
    try:
        data = todo_schema.load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    try:
        storage.Todo.get_by_id(data.name)
        return jsonify({'errors': 'Task already exists.'}), 400
    except storage.Todo.DoesNotExist:
        storage.Todo.create(
            name = data.name,
            task = data.task
        )

    return '', 200
