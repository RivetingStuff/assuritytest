#!/usr/env/python3
"""
Test script for the basic API tests.
Test design requirements:
    1) Name = "Carbon credits"
    2) CanRelist = true
    3) The Promotions element with Name = "Gallery" has a Description that contains the text "2x larger image"

Test coverage:
    Requirement 1) covered by test_response_name
    Requirement 2) covered by test_relist_true
    Requirement 3) covered by test_gallery_promotion_description

"""
import requests
import time

API_URI = "https://api.tmsandbox.co.nz/v1/Categories/6327/Details.json?"
API_PARAMETERS = {"catalogue": "false"}


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
    print(f"Verification {'PASSED' if conditional else 'FAILED'}: {message}")
    if not conditional:
        raise VerificationException(message)


class TestSuite(object):
    """
    Class containing this modules test functions. Initalizing then calling this object will cause to it run each
    test function in sequence then print a test summary to the output buffer. Test functions can be called directly
    to avoid test summary aggregation.
    """
    result_summary: dict
    test_duration: float

    def __init__(self):
        self.result_summary = {}
        self.test_duration = 0.0

    @staticmethod
    def _setup() -> dict:
        result = api_request(API_URI, API_PARAMETERS)
        return result

    @staticmethod
    def _teardown():
        pass

    @staticmethod
    def test_response_name(request_response: dict):
        """
        Verify that the request_response value under the key 'Name' is set as expected.

        :param request_response: json response from the API
        :return:
        """
        expected_value = "Carbon credits"
        name = request_response.get("Name")
        verify(name == expected_value, f"Name returned as expected. '{name}'=='{expected_value}'")

    @staticmethod
    def test_relist_true(request_response: dict):
        """
        Verify that the request_response value under the key 'CanRelist' is set as expected.

        :param request_response: json response from the API
        :return:
        """
        expected_value = True
        can_relist = request_response.get("CanRelist")
        verify(can_relist == expected_value, f"CanRelist returned as expected. '{can_relist}'=='{expected_value}'")

    @staticmethod
    def test_gallery_promotion_description(request_response: dict):
        """
        Verify that the request_response dictionary has an entry under 'Promotions' with the name 'Gallery' and that
        the description of this entry contains the expected text.

        :param request_response: json response from the API
        :return:
        """
        expected_text = "2x larger image"
        target_name = "Gallery"
        promotions = request_response.get("Promotions", {})
        filtered_promotions = list(filter(lambda x: x.get("Name") == target_name, promotions))
        # If we get more than one promotion entry with the targeted name, we should fail
        verify(len(filtered_promotions) == 1, f"Target name is unique within the promotions array. "
                                              f"Found {len(filtered_promotions)} entries")
        target_description = filtered_promotions[0].get("Description", "")
        verify(expected_text in target_description,
               f"Expected text found within targeted promotion. '{expected_text}' in '{target_description}'")

    def _print_summary(self):
        print("//===============================\\\\")
        print("Test Name - Stage - Outcome")
        for test_name, test_summary in self.result_summary.items():
            print(f"{test_name} - {test_summary.get('stage')} - {test_summary.get('result')}")
        print("\n")
        passed_tests = filter(lambda x: x["result"] == "PASSED", self.result_summary.values())
        print(f"Tests passed: {len(list(passed_tests))}/{len(self.result_summary)}"
              f"\tduration: {self.test_duration:.2f} seconds")

    def __call__(self, *args, **kwargs):
        test_methods = [
            self.test_response_name,
            self.test_relist_true,
            self.test_gallery_promotion_description
        ]
        start_time = time.monotonic()
        for test in test_methods:
            # Keeping the stage value up-to-date makes debugging much easier
            stage = "pre-test"
            try:
                stage = "setup"
                request_response: dict = self._setup()
                stage = "call"
                test(request_response)
                stage = "teardown"
                self._teardown()
                result = "PASSED"
                stage = "complete"
            except Exception as ex:
                result = f"FAILED: {str(ex)}"

            self.result_summary[test.__name__] = {
                "stage": stage,
                "result": result
            }
        self.test_duration = time.monotonic() - start_time
        self._print_summary()


if __name__ == "__main__":
    # Initialize TestSuite object for member fields (i.e. result_summary)
    test_suite = TestSuite()
    # Calling the TestSuite object directly allows us to run all the test methods and print the test summary
    test_suite()
