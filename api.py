#!/usr/bin/env python3
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

TODOS = {
    'todo1': {'task': 'build an API', 'status': 'complete'},
    'todo2': {'task': '?????', 'status': 'working'},
    'todo3': {'task': 'profit!', 'status': 'backlog'},
}


#   In this structure, items inside quotes surrounded by curly braces are items the *server* should replace before
# sending to the client. Items in angle brackets are delivered as-is to the client, and are items the client should
# provide before sending a new request to the server. In general, the server should provide complete URIs to the client,
# with distinct placeholders in the template denoting the data type & name of the value expected from the client.
#   'data-template' is a field which provides placeholders to be filled in by clients when making a new request to the
# 'url' in the same operation.
#   'data-fixed' can be dropped into the body of a future request, unaltered.
TODO_OPS = {
    'complete-todo': {
        'url': 'http://localhost:5000/todos/{todo_id}',
        'method': 'POST',
        'data-fixed': {'status': 'complete'}
    },
    'work-todo': {
        'url': 'http://localhost:5000/todos/{todo_id}',
        'method': 'POST',
        'data-fixed': {'status': 'working'}
    },
    'delete-todo': {
        'url': 'http://localhost:5000/todos/{todo_id}',
        'method': 'POST'
    },
    'change-task': {
        'url': 'http://localhost:5000/todos/{todo_id}',
        'method': 'POST',
        'data-template': {'task': '<str:task>'}
    }
}

def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))

parser = reqparse.RequestParser()
parser.add_argument('task')
parser.add_argument('status')


def prepare_todo_ops(todo_id, **kwargs):
    prepped_ops = TODO_OPS
    for op, config in TODO_OPS.items():
        for cfield, cval in config.items():
            try:
                prepped_val = cval.format(**kwargs, todo_id=todo_id)
            except AttributeError:
                print("skipped field %s with value %s" % (cfield, cval))
            else:
                prepped_ops[op][cfield] = prepped_val
    print("prepped_ops: %s" % prepped_ops)
    return prepped_ops


class TodoStatus(Resource):
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        status = TODOS[todo_id]['status']
        ops = prepare_todo_ops(todo_id)
        return {'todo_id': todo_id, 'status': status, 'operations': ops}


# Todo
# shows a single todo item and lets you delete a todo item
class Todo(Resource):
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        ops = prepare_todo_ops(todo_id)
        todo = TODOS[todo_id]
        todo['operations'] = ops
        return todo

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 204

    def put(self, todo_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[todo_id] = task
        return task, 201

    def post(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        todo = TODOS[todo_id]
        args = parser.parse_args()
        status = args['status']
        TODOS[todo_id]['status'] = status
        ops = prepare_todo_ops(todo_id, **args)
        todo["operations"] = ops
        return todo, 201



# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    def get(self):
        return TODOS

    def post(self):
        args = parser.parse_args()
        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        todo_id = 'todo%i' % todo_id
        TODOS[todo_id] = {'task': args['task']}
        return TODOS[todo_id], 201

##
## Actually setup the Api resource routing here
##
api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<todo_id>')
api.add_resource(TodoStatus, '/todos/<todo_id>/status')


if __name__ == '__main__':
    app.run(debug=True)
