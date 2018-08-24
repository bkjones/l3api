from requests import Request, Session, get

s = Session()

def get_todo_by_id(id):
    return get('http://localhost:5000/todos/{}'.format(id))

def get_todo_status_by_id(id):
    return get('http://localhost:5000/todos/{}/status'.format(id))

def update_data_template(template, **kwargs):
    """Some operations have a 'data-template' field whose value is a json block of attributes, at least one of which
    has some value set off by '< >' to indicate that it's expected to be replaced by the client side.

    """
    for field, val in template.items():
        if val.startswith('<') and val.endswith('>'):
            template[field] = kwargs[field]
    return template


def perform_op(todo, opname, **kwargs):
    """Assembles a requests.Request object using templated data we got from a response body

    """
    todo = todo.json()

    # pulls out the part of the response body 'operations' pertaining only to the operation we want to perform
    op_dict = {op:opconfig for (op, opconfig) in todo['operations'].items() if op == opname}

    # start assembling the requests.Request object with data we know now.
    req = Request(op_dict[opname]['method'], op_dict[opname]['url'])

    # the request body payload may require manipulation if it's 'data-template'. If 'data-fixed' we just plop it in.
    try:
        op_dict[opname]['data-template'] = update_data_template(op_dict[opname]['data-template'], **kwargs)
        req.json = op_dict[opname]['data-template']
    except KeyError:
        op_dict = op_dict[opname]['data-fixed']
        req.json = op_dict

    resp = s.send(req.prepare())
    return resp


if __name__ == '__main__':
   todo = get_todo_by_id('todo3')
   print("GET TODO: %s" % todo.json())

   existing_status = get_todo_status_by_id('todo3')
   print("GET Existing Status: %s" % existing_status.json())

   status_update_response = perform_op(todo, 'complete-todo')
   print("Update status result: %s" % status_update_response.json())

   task_update_response = perform_op(todo, 'change-task', task='Task name updated!')
   print ("Update task result: %s" % task_update_response.json())

