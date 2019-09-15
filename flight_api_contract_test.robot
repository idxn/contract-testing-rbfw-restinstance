*** Settings ***
Library         Process
Library         REST
Suite Setup     Start API Server
Suite Teardown  Stop API Server
Test Teardown   Clear Expectations
Test Setup      Expect response to match with snapshot

*** Variables ***
${BASELINE}     ${FALSE}
${JSONSCHEMA_SNAPSHOT}    ${CURDIR}/json/flight_baseline.json

*** Test Cases ***
Flight API should match with the json schema
    REST.Get     http://localhost:8000/flights
    Run Keyword If  ${BASELINE}  REST.Output Schema  response  ${JSONSCHEMA_SNAPSHOT}
    Flight Status Should Be One Of SCHEDULED, DELAYED and DIVERTED
    Arrive And Depart Should Be In Datetime Format

Flight Status from API should be one of SCHEDULED DELAYED AND DIVERTED
    [Tags]  fail
    REST.Get     http://localhost:8000/flights?statusinvalid=true
    Flight Status Should Be One Of SCHEDULED, DELAYED and DIVERTED

Flight API does not match with the snapshot
    [Tags]  fail
    REST.Get     http://localhost:8000/flights?invalidschema=true
    Flight Status Should Be One Of SCHEDULED, DELAYED and DIVERTED

*** Keywords ***
Expect response to match with snapshot
    Run Keyword If  not ${BASELINE}    REST.Expect Response     ${JSONSCHEMA_SNAPSHOT}

Flight Status Should Be One Of SCHEDULED, DELAYED and DIVERTED
    String  $..flightStatus    enum=["SCHEDULED","DELAYED","DIVERTED"]

Arrive And Depart Should Be In Datetime Format
    String  $..arrive    format=date-time
    String  $..depart    format=date-time

Start API Server
    Process.Start Process  python  ${CURDIR}/flight_api_server.py

Stop API Server
    Process.Terminate Process