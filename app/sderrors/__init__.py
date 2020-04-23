class DictionaryNotExistError(Exception):
    pass


class DictionaryAlreadyExistError(Exception):
    pass


class WordNotExistError(Exception):
    pass


class UserAlreadyExistError(Exception):
    pass


class InvalidUsernameOrPasswordError(Exception):
    pass


class QuestionAlreadyAddedError(Exception):
    pass
