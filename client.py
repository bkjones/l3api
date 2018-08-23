import json
from requests import Request, Session, get, put, post
from time import sleep

s = Session()

def get_todo_by_id(id):
    return get('http://localhost:5000/todos/todo3')

def get_todo_status_by_id(id):
    return get('http://localhost:5000/todos/todo3/status')

def perform_op(todo, opname):
    todo = todo.json()
    try:
        op_config = todo['operations'][opname]
    except KeyError:
        print("The operation '%s' does not exist" % opname)
        return

    req = Request(op_config['method'], op_config['url'], data=op_config['data-fixed']).prepare()
    resp = s.send(req)
    return resp





if __name__ == '__main__':
    while True:
       todo = get_todo_by_id('todo3')
       print("GET TODO: %s" % todo.json())
       existing_status = get_todo_status_by_id('todo3')
       print("Existing Status: %s" % existing_status.json())
       status_update_response = perform_op(todo, 'complete-todo')
       print("Updated Status: %s" % status_update_response.json())
       sleep(5)

