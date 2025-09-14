class DatabaseError(Exception):
    pass


class UserNotFoundError(DatabaseError):
    pass


class MessageNotFoundError(DatabaseError):
    pass
