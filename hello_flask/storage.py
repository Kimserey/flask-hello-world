from peewee import SqliteDatabase, CharField, Model

db = SqliteDatabase('./data/todo.db')

class Todo(Model):
  name = CharField(primary_key=True, max_length=10, unique=True)
  task = CharField(max_length=100)
  
  class Meta:
    database = db

def create_tables():
  db.connect()
  Todo.create_table(True)