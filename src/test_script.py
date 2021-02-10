#!/usr/env/python3
"""
Test script
"""
import requests

API_URI = "https://api.tmsandbox.co.nz/v1/Categories/6327/Details.json?"
API_PARAMETERS = {"catalogue": "false"}


class APIException(Exception):
    message: str

    def __init__(self, message: str):
        self.message = message


class VerificationException(Exception):
    message: str

    def __init__(self, message: str):
        self.message = message


def api_request(api_address: str, request: dict) -> dict:
    """
    Make a GET request to the provided API endpoint given the parameters provided in request
    :param api_address: URL of the API endpoint being tested
    :param request: GET parameters for the request
    :return:
    """

    error_tolerance = 3
    error_count = 0
    response = None

    while (error_count := error_count + 1) < error_tolerance:
        response = requests.get(api_address, request)
        if response.status_code == 200:
            break
    else:
        raise APIException(f"API request failed with the following cause {response.reason}")

    return response.json()


# TODO verification function
def verify(conditional: bool, message: str) -> None:
    """
    If conditional is falsey, raise verification exception with the provided message.
    Else print the message
    :param conditional: Evaluated conditional statement
    :param message: log message explaining the intention of this verification
    :return: None
    """
    if not conditional:
        raise VerificationException(message)

    print(f"Verification PASSED: {message}")


class TestSuite:
    result_summary: dict

    def _setup(self) -> dict:
        result = api_request(API_URI, API_PARAMETERS)
        return result

    def _teardown(self):
        pass

    def test_response_name(self, request_response: dict):
        expected_value = "Carbon credits"
        name = request_response.get("Name")
        verify(name == expected_value, f"Name returned as expected. {name}=={expected_value}")

    def test_relist_true(self, request_response: dict):
        expected_value = "True"
        can_relist = request_response.get("CanRelist")
        verify(can_relist == expected_value, f"CanRelist returned as expected. {can_relist}=={expected_value}")

    def test_gallery_promotion_description(self, request_response: dict):
        expected_text = "2x larger image"
        target_name = "Gallery"
        promotions = request_response.get("Promotions", {})
        filtered_promotions = list(filter(lambda x: x.get("Name") == target_name, promotions))
        verify(len(filtered_promotions) == 1, f"Target name is unique within the promotions array. "
                                              f"Found {len(filtered_promotions)} entries")

        verify(expected_text in filtered_promotions[0].get("description", ""),
               f"Expected text found within targeted promotion. {expected_text} in {filtered_promotions}")


    def print_summary(self):
        #TODO pretty print the summary
        pass

    def __call__(self, *args, **kwargs):
        for test in [self.test_method1, self.test_method2, self.test_method3]:
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

            self.result_summary[str(test)]["stage"] = stage
            self.result_summary[str(test)]["result"] = result

        self.print_summary()


if __name__ == "__main__":
    #TODO call test functions, then call print summary
    TestSuite()