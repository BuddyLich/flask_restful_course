import sqlite3


class UserModel:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    # def find_by_username(self, username):
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username, ))
        # the second argument inside execute() must be tuple
        row = result.fetchone()
        if row:
            # user = User(row[0], row[1], row[2])
            user = UserModel(*row)
        else:
            user = None

        connection.close()
        return user

    @classmethod
    # def find_by_username(self, username):
    def find_by_id(cls, id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (id,))
        # the second argument inside execute() must be tuple
        row = result.fetchone()
        if row:
            # user = User(row[0], row[1], row[2])
            user = UserModel(*row)
        else:
            user = None

        connection.close()
        return user
