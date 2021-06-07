#!/usr/bin/env python
"""This module contain functionality that is common to all the models in this
passage"""


def model_dict(obj: object, columns: tuple) -> dict:
    """This function is a used to convert all models in the system to a
    dictionary representation

    Arg(s)
    ~~~~~~
        obj -> an instance of the sqlalchemy object to change to a dictionary
        columns: tuple -> a tuple of columns on model to be present in the
            dictionary

    Return(s)
    ~~~~~~~
        tmp: dict -> dictionary representation of the sqlalchemy model instance
            passed to the function
    """
    tmp = {}
    for column in columns:

        value = getattr(obj, column)

        if hasattr(value, 'year') or hasattr(value, 'hour'):
            value = str(value)

        tmp[column] = value

    return tmp
