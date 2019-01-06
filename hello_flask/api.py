from . import app
from flask import request
from flask_restful import Resource, Api

api = Api(app)

todos = {}

class Persons(Resource):
  def get(self):
    return [{ 'name': 'Kim' }, { 'name': 'Tom' }]

class TodoSimple(Resource):
    def get(self, todo_id):
        if todo_id in todos:
          return { todo_id: todos[todo_id]}
        else:
          return todo_id + ' not found.'

    def put(self, todo_id):
        todos[todo_id] = request.form['data']
        return { todo_id: todos[todo_id]}

api.add_resource(Persons, '/persons')
api.add_resource(TodoSimple, '/todos/<string:todo_id>')