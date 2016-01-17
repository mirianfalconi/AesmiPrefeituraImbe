from werkzeug.security import generate_password_hash,  check_password_hash


class User(object):

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

    def seta_password(self, password):
        return generate_password_hash(password)

    def verifica_password(self, hash, password):
        return check_password_hash(hash, password)
