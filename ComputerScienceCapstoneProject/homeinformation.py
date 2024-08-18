from colorama import Fore, Back         # IMPORT 'Fore' AND 'Back' FROM 'colorama' TO USE COLORED TEXT IN SCRIPT

import json                             # IMPORT 'json' TO CONVERT STRING RESULT TO JSON FORMAT
import requests                         # IMPORT 'requests' TO ALLOW FOR HTTP REQUEST TO APIs AND FETCH INFORMATION
import time                             # IMPORT 'time' TO ALLOW BREAKS BETWEEN LOOPS

def addressInformation(inputAddress):
    autoID = ''                                                                     # INSTANTIATE ID TO BE USED
    api_key = '415a95edbemsh247c443994f0b77p1917e8jsn11d9e2f64047'                  # API KEY OBTAINED BY: https://rapidapi.com (TO BE USED IN THESIS DEFENSE: '') - 415a95edbemsh247c443994f0b77p1917e8jsn11d9e2f64047
    urlAUTO = 'https://redfin5.p.rapidapi.com/auto-complete'                        # BASE URL FOR REDFIN API (auto-complete)
    urlInformation = 'https://redfin5.p.rapidapi.com/properties/get-info'           # BASE URL FOR REDFIN API (properties/list)
    addressURL = ''                                                                 # URL OF USER INPUTTED ADDRESS

    headerParameters = {'X-RapidAPI-Key': api_key, 'X-RapidAPI-Host': 'redfin5.p.rapidapi.com'}         # HEADER PARAMETERS PROVIDED BY https://rapidapi.com

    """

    location        --> STRING

    """

    requiredParametersAUTO = {'location': inputAddress}         # REQUIRED PARAMETERS PROVIDED BY https://rapidapi.com; FEED USER INPUT

    try:                                                                                                        # CATCH STATEMENT IF PROVIDED LISTING ADDRESS IS INVALID
        response = requests.get(urlAUTO, headers = headerParameters, params = requiredParametersAUTO)           # SEND GET REQUEST WTIH GIVEN HEADER PARAMETERS AND REQUIRED PARAMETERS

        if response.status_code == 200:         # STATUS CODE 200 INDICATES A SUCCESSFUL FIND (OK)
            response = response.json()          # CONVERT RESPONSE INTO JSON FORMAT

            """
        
            errorMessage: "Success"
            payload: {}
                exactMatch: {}       - active, businessMarketIds, claimedHome, countryCode, id, ..., name, subName, ...
                extraResults: {}
                sections: []
            resultCode: 0
            version: 515

            """

            url = response.get('payload', {}).get('exactMatch', {}).get('url')          # OBTAIN URL FROM JSON DATA; WILL NEED TO BE COMBINED WITH HEADER URL
            addressURL = url                                                            # UPDATE ADDRESS URL

            if url == None:                                                                         # VERIFY URL IS NOT NONE
                url = response.get('payload', {}).get('sections', [{}])[0].get('rows', [])          # IF NONE, URL LOCATED IN THE SECOND INDEX (ARRAY WITHIN A DICTIONARY)
                url = url[0].get('url')                                                             # OBTAIN URL AND UPDATE VARIABLE
                addressURL = url                                                                    # UPDATE ADDRESS URL

            parser = url.split('/')             # OBTAIN THE ZIP CODE BY PARSING THE URL
            miniAddress = parser[-3]            # ZIP CODE LOCATED IN THE THIRD-TO-LAST INDEX

            parser = miniAddress.split('-')         # OBTAIN THE ZIP CODE BY PARSING THE ADDRESS SECTION
            zipcode = parser[-1]                    # ZIP CODE LOCATED IN THE LAST INDEX
            
            message = response.get('payload', {}).get('exactMatch', {}).get('name') + ", " + response.get('payload', {}).get('exactMatch', {}).get('subName') + " " + zipcode           # PREPARE ADDRESS TO PRINT
            print(Back.BLACK + Fore.WHITE + "ADDRESS FOUND:" + Fore.RESET + Back.RESET + " " + Back.GREEN + Fore.WHITE + message + Fore.RESET + Back.RESET)                             # PRINT ADDRESS TO USER
        else:                                                                                                                               # STATUS CODE 300 (OR OTHER) INDICATES AN UNSUCCESSFUL FIND
            print(Back.YELLOW + Fore.RED + 'ERROR: The listing address provided is invalid. Try again.' + Fore.RESET + Back.RESET)          # PRINT ERROR MESSAGE
            exit()                                                                                                                          # EXIT

    except requests.RequestException as error:                                                                                          # CATCH IF ADDRESS IS INVALID
        print(Back.YELLOW + Fore.RED + 'ERROR: The listing address provided is invalid. Try again.' + Fore.RESET + Back.RESET)          # PRINT ERROR MESSAGE
        exit()                                                                                                                          # EXIT

    """

    url             --> value of the ...home/url in the /auto-complete endpoint

    """

    requiredParametersProperties = {'url': addressURL}          # REQUIRED PARAMETERS PROVIDED BY https://rapidapi.com; FEED URL OBTAINED

    try:                                                                                                                    # CATCH STATEMENT IF PROVIDED URL ADDRESS IS INVALID
        response = requests.get(urlInformation, headers = headerParameters, params = requiredParametersProperties)          # SEND GET REQUEST WTIH GIVEN HEADER PARAMETERS AND REQUIRED PARAMETERS

        if response.status_code == 200:         # STATUS CODE 200 INDICATES A SUCCESSFUL FIND (OK)
            results = response.json()           # CONVERT RESPONSE INTO JSON FORMAT

            primaryInformation = results.get('aboveTheFold', {}).get('addressSectionInfo', {})          # OBTAIN PRIMARY ADDRESS INFORMATION TO PARSE

            bathCount = primaryInformation.get('baths')
            bedCount = primaryInformation.get('beds')
            sqft = primaryInformation.get('sqFt', {}).get('value')
            status = primaryInformation.get('status', {}).get('displayValue')
            statusDefinition = primaryInformation.get('status', {}).get('definition')


            print(Back.YELLOW + Fore.BLACK + 'Baths:' + Fore.RESET + Back.RESET + ' ' + f'{bathCount}')
            print(Back.YELLOW + Fore.BLACK + 'Beds:' + Fore.RESET + Back.RESET + ' ' + f'{bedCount}')
            print(Back.YELLOW + Fore.BLACK + 'Square Footage:' + Fore.RESET + Back.RESET + ' ' + f'{sqft}' + ' sq. ft.')

            if(status == 'Active'):
                print(Back.YELLOW + Fore.BLACK + 'Status: ' + Fore.RESET + Back.RESET + ' ' + Back.GREEN + Fore.BLACK + status + ' - ' + statusDefinition + Fore.RESET + Back.RESET)
            elif(status == 'Closed'):
                print(Back.YELLOW + Fore.BLACK + 'Status:' + Fore.RESET + Back.RESET + ' ' + Back.RED + Fore.YELLOW + status + ' - ' + statusDefinition + Fore.RESET + Back.RESET)
            
        else:                                                                                                                               # STATUS CODE 300 (OR OTHER) INDICATES AN UNSUCCESSFUL FIND
            print(Back.YELLOW + Fore.RED + 'ERROR: The listing address provided is invalid. Try again.' + Fore.RESET + Back.RESET)          # PRINT ERROR MESSAGE
            exit()                                                                                                                          # EXIT

    except requests.RequestException as error:                                                                                          # CATCH IF URL ADDRESS IS INVALID
        print(Back.YELLOW + Fore.RED + 'ERROR: The listing address provided is invalid. Try again.' + Fore.RESET + Back.RESET)          # PRINT ERROR MESSAGE
        exit()                                                                                                                          # EXIT

def main():
    print(Back.GREEN + Fore.RED + "~~~ SAFEHOUSE: Fighting Real Estate Scams! ~~~" + Fore.RESET + Back.RESET)                       # HEADER OF PROJECT
    print(Back.BLACK + Fore.WHITE + "Instruction: Provide the listing address." + Fore.RESET + Back.RESET)                          # INSTRUCT USER TO INPUT THE LISTING ADDRESS
    print(Back.BLACK + Fore.WHITE + "Provide the CITY, STATE, and ZIP CODE for better accuracy." + Fore.RESET + Back.RESET)         # SUGGEST TO THE USER TO INPUT DETAILED INFORMATION

    providedAddress = input(Back.WHITE + Fore.BLACK + 'Listing Address:' + Fore.RESET + Back.RESET + ' ')           # OBTAIN LISTING ADDRESS FROM THE USER
    addressInformation(providedAddress)                                                                             # JUMP TO 'addressInformation' FUNCTION

if __name__ == "__main__":
    main()          # MAIN FUNCTION