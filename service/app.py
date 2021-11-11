import falcon
from service.users import UserResource

app = application = falcon.App()

users = UserResource()
app.add_route('/users', users)

def create():
    """For use in testing"""
    app = falcon.App()
    app.add_route('/users', users)
    return app