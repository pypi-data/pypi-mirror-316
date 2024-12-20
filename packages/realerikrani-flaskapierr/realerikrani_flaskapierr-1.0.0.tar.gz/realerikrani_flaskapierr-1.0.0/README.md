# flaskapierr

Register the error handler

```py
from flask import Flask
from realerikrani.flaskapierr import handle_error

# ...

def create() -> Flask:
    app = Flask("api")
    app.register_blueprint(todo_blueprint, url_prefix="/todos")
    app.register_error_handler(Exception, handle_error)
    return app
```

... and use the error classes for raising errors from Flask blueprints.

```py
from realerikrani.flaskapierr import Error, ErrorGroup

# ...

@todo_blueprint.route("", methods=["POST"])
def create_todo():
    try:
        todo = repo.create_todo(dict(request.json))
    except TodoAlreadyExistsError as ve:
        raise ErrorGroup("409", [Error(ve.message, ve.code)]) from None

    return {"todo": asdict(todo)}, 201
```