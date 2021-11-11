import falcon
from users import UserResource

app = application = falcon.App()

users = UserResource()
app.add_route('/users',users)

