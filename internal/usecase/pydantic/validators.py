from typing import Pattern

from internal.usecase.pydantic import errors


def validate_email(phone: str, regex: Pattern[str]) -> str:
    if not regex.match(phone):
        raise errors.EmailError(phone=phone)

    return phone


def validate_username(username: str, regex: Pattern[str]) -> str:
    if not regex.match(username):
        raise errors.UserNameError(username=username)

    return username
