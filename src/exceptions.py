"""
Module housing custom exceptions required in the api TestSuite
"""


class APIException(Exception):
    """
    Exception class related to API request status'
    """
    message: str

    def __init__(self, message: str):
        self.message = message


class VerificationException(Exception):
    """
    Exception class relating to test verification condition resolving to a falsey value
    """
    message: str

    def __init__(self, message: str):
        self.message = message

