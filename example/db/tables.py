from pypika import Table


class Users(Table):
    __table__ = "users"
    id: int
    username: str
    email: str
    password: str


users = Users()
