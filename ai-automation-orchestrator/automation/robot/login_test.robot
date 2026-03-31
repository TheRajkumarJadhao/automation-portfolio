*** Settings ***
Library           SeleniumLibrary
Suite Setup       Open Browser Session
Suite Teardown    Close Browser Session

*** Variables ***
${URL}            https://maharera.maharashtra.gov.in/
${BROWSER}        headlesschrome

*** Keywords ***
Open Browser Session
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window

Close Browser Session
    Close All Browsers

Get And Log Page Title
    ${title}=    Get Title
    Log    Page Title is: ${title}    console=True
    Log To Console    Page Title: ${title}
    RETURN    ${title}

*** Test Cases ***
Main
    Get And Log Page Title
