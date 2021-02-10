"""
Module housing the utility functions required by test_api_response.py
"""
import requests

from tabulate import tabulate
import colored
from colored import stylize

from .exceptions import APIException, VerificationException


def execute_test_loop(setup_function: any, teardown_function: any, test_functions: list) -> dict:
    """
    Utility function for handling the execution of tests provided by the test class
    :param setup_function: function run before a test. Must produce a dictionary object
    :param teardown_function: function run after a test has finished
    :param test_functions: list of test functions that will be called and passed the return from the setup_function
    :return: summary of test run results
    """
    result_summary = {}
    for test in test_functions:
        # Keeping the stage value up-to-date makes debugging much easier
        stage = "pre-test"
        message = ""
        try:
            stage = "setup"
            request_response: dict = setup_function()
            stage = "call"
            test(request_response)
            stage = "teardown"
            teardown_function()
            result = "PASSED"
            stage = "complete"
        except Exception as ex:
            result = "FAILED"
            message = f"{str(ex)}"

        result_summary[test.__name__] = {
            "stage": stage,
            "result": result,
            "message": message
        }
    return result_summary


def print_result_summary(result_summary: dict, test_duration: float) -> None:
    """
    Utility function for printing the result summary produced by execute_test_loop
    :param result_summary: dictionary containing test run information
    :param test_duration: amount of time spent running the tests
    :return: None
    """
    columns = ["Test Name", "Stage", "Outcome"]
    color_map = {
        "PASSED": colored.fg('green'),
        "FAILED": colored.fg('red'),
    }
    table_rows = []
    # Tabulate expects a 2D array as the format of table data. The result_summary needs to be restructured
    for test_name, test_summary in result_summary.items():
        test_result = test_summary.get("result")
        test_message = test_summary.get("message")

        color_fg = color_map.get(test_result, colored.fg('yellow'))
        test_result_long = f"{test_result}{': ' if test_message else ''}{test_message}"

        table_rows.append([
            stylize(test_name, color_fg),
            stylize(test_summary.get("stage"), color_fg),
            stylize(test_result_long, color_fg),
        ])

    print("\n")
    print(tabulate(table_rows, headers=columns, tablefmt="grid"))
    print("\n")
    passed_tests = filter(lambda x: x["result"] == "PASSED", result_summary.values())
    print(f"Tests passed: {len(list(passed_tests))}/{len(result_summary)}"
          f"\tduration: {test_duration:.2f} seconds")


def api_request(api_address: str, request: dict) -> dict:
    """
    Make a GET request to the provided API endpoint given the parameters provided in request
    :param api_address: URL of the API endpoint being tested
    :param request: GET parameters for the request
    :return: json reponse from endpoint
    """

    error_tolerance = 3
    error_count = 0
    response = None

    while (error_count := error_count + 1) <= error_tolerance:
        response = requests.get(api_address, request)
        if response.status_code == 200:
            break
    else:
        raise APIException(f"API request failed with the following cause {response.reason}")

    return response.json()


def verify(conditional: bool, message: str) -> None:
    """
    If conditional is falsey, raise verification exception with the provided message.
    Else print the message
    :param conditional: Evaluated conditional statement
    :param message: log message explaining the intention of this verification
    :return: None
    """

    message = f"Verification {'PASSED' if conditional else 'FAILED'}: {message}"
    print(stylize(message, colored.fg('green') if conditional else colored.fg('red')))
    if not conditional:
        raise VerificationException(message)
