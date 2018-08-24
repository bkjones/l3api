The API and How To Use It
===========================

The 'todo' API is designed to make it as easy as possible for client developers to create applications that are not subject 
to disruption with every step made to evolve the API into the future. 

As such, the API is designed to enable client applications to focus on implementing *generic operations* rather than 
hard-coding hyper-specific URLs, methods, and data that tightly couple your applications to the current state of the API.

So, for example, a normal API would document the updating of a todo's status something like this: 

    URL: /todos/{todo_id}/status 
    Method: PUT
    Data: "{'status': 'complete'}"
    
If you implemented that in your code, it would typically look something like this (in Python): 

    def complete_todo(todo_id):
        url = '/todos/{todo_id}/status'.format(todo_id)
        method = 'PUT'
        data = json.dumps({'status': 'complete'})
        resp = requests.put(url, method, data)
        return resp
        
Simple enough. However, the API provider has decided to change this operation such that it becomes a POST instead of a PUT, 
and the request isn't sent to the `status` endpoint, but rather to the `/todos/{todo_id}` resource directly. You disagree 
with the design choice because it's dumb, and you're probably right, but you don't own the API, so you have to make the 
change to keep your application working. You go back to the documentation to get updated information on how to change your code: 

    URL: /todos/{todo_id}
    Method: POST
    Data: "{'status': 'complete'}"
    
So you change your code to look like this: 

    def complete_todo(todo_id):
        url = '/todos/{todo_id}'.format(todo_id)
        method = 'POST'
        data = json.dumps({'status': 'complete'})
        resp = requests.post(url, method, data)
        return resp
    
Not a big change, but after making a change like this once a month, it gets a little old. 

Stop The Madness
===================
Instead of exposing the implementation details of the API in the form of documentation that essentially gets cut-n-pasted 
into your code in the form of hard-coded URLs and methods, etc., our API will provide data dynamically to enable your 
application to implement *generic operations* instead of hard-coding. 

First, make a request for a resource map. This tells your code how to find resources in the API: 

    $ curl 'http://localhost:5000/'
    {
        "todos": "http://localhost:5000/todos"
    }

So, to find the url to get at the todos, your code needs to know it's looking for 'todos'. Yes, this is a hard-coded piece of 
data, but:
* if we stop supporting 'todos', we're out of business, and 
* it still affords you the ability to not have to care if we change the location of 'todos', which we could do if we someday 
enable users to assign todos to specific projects, for example. For all you care, that endpoint could be called 'a4cdz16f1003043358', 
because your code just looks it up in the resource map & knows where to go to get at and manipulate 'todos'. 

From there, your code needs to know what it can do with todos, and how to do it. If your code requests a todo, though (or
performs any other operation on it), it'll have all of the data it needs to perform any available operation on the resource: 

    {
        "task": "profit!",
        "status": "backlog",
        "operations": {
            "complete-todo": {
                "url": "http://localhost:5000/todos/todo3/status",
                "method": "PUT",
                "data-fixed": {
                    "status": "complete"
                }
            },
            "work-todo": {
                "url": "http://localhost:5000/todos/todo3/status",
                "method": "PUT",
                "data-fixed": {
                    "status": "working"
                }
            },
            "delete-todo": {
                "url": "http://localhost:5000/todos/todo3",
                "method": "DELETE"
            },
            "change-task": {
                "url": "http://localhost:5000/todos/todo3",
                "method": "PUT",
                "data-template": {
                    "task": "<str:task>"
                }
            }
        }
    }


This response contains data about the todo, like the 'task' and 'status', and then another section called 'operations'. 
Inside 'operations' is data in a format easily understood and manipulated by a computer program (or a human). 

So, the process of updating the status of a todo is as simple as looking up the operation, assembling the operation's method, 
url, and data into a request, and sending it! We can create a generic function to take in an operation name, make the request, 
and return the response. We'll call it 'perform_op': 

```python
from requests import Request, Session, get
s = Session()
def perform_op(todo, opname, **kwargs):
    """Assembles a requests.Request object using templated data we got from a response body

    """
    # pulls out the part of the response body 'operations' pertaining only to the operation we want to perform
    op_dict = {op:opconfig for (op, opconfig) in todo['operations'].items() if op == opname}
    
    # data payload for this operation is fixed data that came from the server. Convenient!
    body_data = op_dict[opname]['data-fixed']
    
    # assemble a Request object
    req = Request(op_dict[opname]['method'], op_dict[opname]['url'], json=body_data)
    
    # send the request!
    resp = s.send(req.prepare())
    return resp
```

This code is slightly simplified -- it doesn't support data payloads that are templated & require filling in by the client
(but we will get to that). Right now, this code only supports operations with a 'data-fixed' attribute. This covers all
of the status updates. So, to change the status of 'todo3' to 'complete', here's the code you would just add to the bottom 
of the above example: 
    
```python
def get_todo_by_id(todo_id):
    return get('{url}/{id}'.format(url=TODO_BASE_URL, id=todo_id))

if __name__ == '__main__':
    resource_map = get('http://localhost:5000/').json()
    TODO_BASE_URL = resource_map['todos']

    todo = get_todo_by_id('todo3').json()
    status_update_response = perform_op(todo, 'complete-todo')
```

Now, because most of what your code is doing consists of *generic operations*, like looking up data in a data structure, 
if the location of the todo endpoint changed, you don't have to care. If we changed the endpoint to perform status updates, 
you don't have to care. If we changed the HTTP method, no worries. If we changed the data you had to provide, but it was still 
fixed data, the change is transparent. As much of what your code needs as possible is formatted as data navigable by your code, 
so that when changes are made, your code can respond to them in real time, without having to make code updates. 

