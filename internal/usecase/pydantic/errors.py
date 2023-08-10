from pydantic.errors import PydanticValueError


class EmailError(PydanticValueError):

    code = 'email'
    msg_template = '"{email}"  is already in use'


class UserNameError(PydanticValueError):

    code = 'username'
    msg_template = '"{username}" the name is already taken'
