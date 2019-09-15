# contract-testing-rbfw-restinstance
An example on how to create the contract testing test with rbfw and restinstance library

# Steps:
0. The flight api server is tested on python3. I'm not sure the api server could be run on python2 so let's use the python3. The python2 anyway will be sunset in next year.
1. Install python package required
        ```pip install -r requirements.txt```
2. To run contract test with robot
        ```robot flight_api_contract_test.robot```
