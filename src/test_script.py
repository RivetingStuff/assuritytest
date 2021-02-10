#!/usr/env/python3
"""
Test script
"""

# TODO make request to API
def api_request(api_address: str, request: dict) -> dict:
    """
    Make a GET request to the provided API endpoint given the parameters provided in request
    :param api_address: URL of the API endpoint being tested
    :param request: GET parameters for the request
    :return:
    """
    pass


# TODO verification function
def verify(conditional:bool, message:str) -> None:
    """
    If conditional is falsey, raise verification exception with the provided message.
    Else print the message
    :param conditional: Evaluated conditional statement
    :param message: log message explaining the intention of this verification
    :return: None
    """
    pass


class TestSuite:
    result_summary: dict

    def _setup(self):
        #TODO setup
        pass

    def _teardown(self):
        #TODO teardown
        pass

    def test_method1(self):
        #TODO test function1
        pass
    def test_method2(self):
        #TODO test function 2
        pass
    def test_method3(self):
        #TODO test function 3
        pass

    def print_summary(self):
        #TODO pretty print the summary
        pass

    def __call__(self, *args, **kwargs):
        # TODO wrap call in try
        pass

if __name__ == "__main__":
    #TODO call test functions, then call print summary
    pass