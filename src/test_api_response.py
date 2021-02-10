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
import time

from .utilities import execute_test_loop, print_result_summary, verify, api_request

API_URI = "https://api.tmsandbox.co.nz/v1/Categories/6327/Details.json?"
API_PARAMETERS = {"catalogue": "false"}


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
        print_result_summary(self.result_summary, self.test_duration)

    def __call__(self, *args, **kwargs):
        test_methods = [
            self.test_response_name,
            self.test_relist_true,
            self.test_gallery_promotion_description
        ]
        start_time = time.monotonic()
        execute_test_loop(self._setup, self._teardown, test_methods)
        self.test_duration = time.monotonic() - start_time
        self._print_summary()


if __name__ == "__main__":
    # Initialize TestSuite object for member fields (i.e. result_summary)
    test_suite = TestSuite()
    # Calling the TestSuite object directly allows us to run all the test methods and print the test summary
    test_suite()
