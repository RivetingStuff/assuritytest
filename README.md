# assurity_test
 simple testcase exercise

## Test requirements
The following requirements were provided for the included testcases:
- Name = "Carbon credits"
- CanRelist = true
- The Promotions element with Name = "Gallery" has a Description that contains the text "2x larger image"

## Test cases 

1) test_response_name: Tests that the response from the provided endpoint includes the key-value pair Name:'Carbon credits'
2) test_relist_true: Tests that the response from the provided endpoint includes the key-value pair CanRelist:True
3) test_gallery_promotion_description: Test that the response from the endpoint includes an entry in the promotions array with the key-value pair Name:Gallery and that the string '2x larger image' exists in the description

## Running the code
### Environment

The minimum required python version is >=3.6 but 3.8 has been the target interpreter during writing. 

The test module was written and run on windows10. Setting up a python virtualenv is very much recommended before installing any requirements. 

The requirements are included in the file 'requirements.txt' and can be installed with `pip install -r requirements.txt`

### Execution

With the virtual environment activated. Run `python {Path_to_repo}/src/test_api_response.py`

## Design
### Structure

Three modules are included in this repository. 
- test_api_response.py: contains the TestSuite and test functions. Entry point to execute tests.
- utilities.py: contains functionality required by test_api_response refactored to improve test readability. 
- exceptions.py: contains exceptions required by utilities.py 

### Considerations

In hopes of avoiding over-engineering a solution to an otherwise simple problem, some limitations were accepted in the code.

- None of the code included has unit-tests
- Communication with the API is subject to only minimal fault tolerance 
- No test framework was used (e.g. pytest)
- Tests as short as these do not require log messages to improve clarity
- The utility module does not encapsulate responsibility well

Few dependencies outside of python's builtin modules are required.



