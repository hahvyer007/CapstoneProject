from colorama import Fore, Back         # IMPORT 'Fore' AND 'Back' FROM 'colorama' TO USE COLORED TEXT IN SCRIPT

import json                             # IMPORT 'json' TO CONVERT STRING RESULT TO JSON FORMAT
import requests                         # IMPORT 'requests' TO ALLOW FOR HTTP REQUEST TO APIs AND FETCH INFORMATION
import time                             # IMPORT 'time' TO ALLOW BREAKS BETWEEN LOOPS

def printHomeInformation(index):
    information = index.get('url')          # OBTAIN THE LISTING ADDRESS THROUGH THE URL VARIABLE

    parser = information.split('/')         # PARSE THE URL BY DELIMETER '/'

    address = parser[-3].replace('-', ' ')              # OBTAIN THE LISTING ADDRESS (REPLACE ALL '-' WITH SPACES)
    city = index.get('city')                            # OBTAIN THE LISTING CITY
    state = index.get('state')                          # OBTAIN THE LISTING STATE
    zipcode = index.get('zip')                          # OBTAIN THE LISTING ZIP CODE
    price = index.get('priceInfo', {}).get('amount')    # OBTAIN THE LISTING PRICE

    print(f"{address}, {city}, {state}, {zipcode}: " + Back.GREEN + Fore.BLACK + "${:,.2f}".format(price) + Fore.RESET + Back.RESET)         # PRINT ALL THE INFORMATION DISSECTED AND FORMAT THE PRICE

def average_price(inputAddress):
    # INFORMATION OBTAINED FROM: https://scrapfly.io/blog/how-to-scrape-redfin/

    autoID = ''                                                                     # INSTANTIATE ID TO BE USED
    api_key = 'aa8d851eebmsh8d75dbabdcdd447p15ba20jsn35dac8e4e76f'                  # API KEY OBTAINED BY: https://rapidapi.com (TO BE USED IN THESIS DEFENSE: 'aa8d851eebmsh8d75dbabdcdd447p15ba20jsn35dac8e4e76f') - 415a95edbemsh247c443994f0b77p1917e8jsn11d9e2f64047
    urlAUTO = 'https://redfin5.p.rapidapi.com/auto-complete'                        # BASE URL FOR REDFIN API (auto-complete)
    urlProperties = 'https://redfin5.p.rapidapi.com/properties/get-info'            # BASE URL FOR REDFIN API (properties/list)
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

            autoID = response.get('payload', {}).get('exactMatch', {}).get('id')            # OBTAIN ID AND UPDATE VARIABLE

            noneFound = False           # TRIGGER VARIABLE IF ID IS NONE

            if autoID == None:                                                                          # VERIFY ID IS NOT NONE
                autoID = response.get('payload', {}).get('sections', [{}])[0].get('rows', [])           # IF NONE, ID LOCATED IN THE SECOND INDEX (ARRAY WITHIN A DICTIONARY)
                autoID = autoID[0].get('id')                                                            # OBTAIN ID AND UPDATE VARIABLE
                autoID = autoID[2:]                                                                     # REMOVE THE FIRST TWO CHARACTERS TO FIND NEARBY LISTING PRICES
                noneFound = True                                                                        # TRIGGER VARIABLE
            else:                                                                                       # ID IS NOT NONE...
                autoID = autoID[2:]                                                                     # ...REMOVE THE FIRST TWO CHARACTERS TO FIND NEARBY LISTING PRICES

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

            if noneFound == True:                                                                                                                                       # IF TRIGGER VARIABLE IS TRUE
                subString = response.get('payload', {}).get('sections', [{}])[0].get('rows', [{}])[0]                                                                   # SUBSTRING DICTIONARY TO EASILY OBTAIN INDICES
                message = subString.get('name') + ", " + subString.get('subName') + " " + zipcode                                                                       # PREPARE ADDRESS TO PRINT
                print(Back.BLACK + Fore.WHITE + "ADDRESS FOUND:" + Fore.RESET + Back.RESET + " " + Back.GREEN + Fore.WHITE + message + Fore.RESET + Back.RESET)         # PRINT ADDRESS TO USER
            else:                                                                                                                                                                           # ELSE TRIGGER VARIABLE IS FALSE
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
        response = requests.get(urlProperties, headers = headerParameters, params = requiredParametersProperties)           # SEND GET REQUEST WTIH GIVEN HEADER PARAMETERS AND REQUIRED PARAMETERS

        if response.status_code == 200:         # STATUS CODE 200 INDICATES A SUCCESSFUL FIND (OK)
            results = response.json()           # CONVERT RESPONSE INTO JSON FORMAT

            """

            similars/listings: {}
                homes: []
                    price: {}
                        value

            """

            nearbyHomes = results.get('avm', {}).get('comparables', [])         # RETRIVE 'homes' DATA FROM 'avm' DATA

            nearbyPrices = []           # RETURN VARIABLE CONTAINING PRICES OF NEARBY LISTING PROPERTIES

            print(Back.LIGHTBLACK_EX + Fore.WHITE + "Listing the price for nearby listings found:" + Fore.RESET + Back.RESET)           # PRINT LISTING INFORMATION TO USER

            for index in nearbyHomes:                                                   # ITERATE THROUGH NEARBY LISTINGS
                if index.get('priceInfo', {}).get('amount') is not None:                # ENSURE THE NEARBY LISTING PRICE IS NOT NONE
                    time.sleep(3)                                                       # DELAY LOOP BY THREE SECONDS
                    printHomeInformation(index)                                         # PRINT LISTING ADDRESS AND PRICE TO USER USING MADE FUNCTION
                    nearbyPrices.append(index.get('priceInfo', {}).get('amount'))       # APPEND NEARBY LISTING PRICE TO DICTIONARY VARIABLE

            return nearbyPrices         # RETURN DICTIONARY VARIABLE
            
        else:                                                                                                                               # STATUS CODE 300 (OR OTHER) INDICATES AN UNSUCCESSFUL FIND
            print(Back.YELLOW + Fore.RED + 'No listing prices found nearby.' + Fore.RESET + Back.RESET)          # PRINT ERROR MESSAGE
            exit()                                                                                                                          # EXIT

    except requests.RequestException as error:                                                                                          # CATCH IF URL ADDRESS IS INVALID
        print(Back.YELLOW + Fore.RED + 'ERROR: The listing address provided is invalid. Try again.' + Fore.RESET + Back.RESET)          # PRINT ERROR MESSAGE
        exit()                                                                                                                          # EXIT

def main():
    print(Back.GREEN + Fore.RED + "~~~ SAFEHOUSE: Fighting Real Estate Scams! ~~~" + Fore.RESET + Back.RESET)                       # HEADER OF PROJECT
    print(Back.BLACK + Fore.WHITE + "Instruction: Provide the listing address." + Fore.RESET + Back.RESET)                          # INSTRUCT USER TO INPUT THE LISTING ADDRESS
    print(Back.BLACK + Fore.WHITE + "Provide the CITY, STATE, and ZIP CODE for better accuracy." + Fore.RESET + Back.RESET)         # SUGGEST TO THE USER TO INPUT DETAILED INFORMATION

    providedAddress = input(Back.WHITE + Fore.BLACK + 'Listing Address:' + Fore.RESET + Back.RESET + ' ')           # OBTAIN LISTING ADDRESS FROM THE USER
    averagePrice = average_price(providedAddress)                                                                   # JUMP TO 'average_price' FUNCTION

    sum = 0                                         # INSTANTIATE THE SUM VARIABLE
    for index in averagePrice:                      # ITERATE THROUGH THE ARRAY VARIABLE
        sum += index                                # ADD THE PRICE TO THE SUM VARIABLE
    averagePrice = sum / len(averagePrice)          # OBTAIN THE AVERAGE BY DIVIDING BY THE LENGTH OF THE VARIABLE

    print(Back.BLACK + Fore.WHITE + "The average price in the located area is:" + Fore.RESET + Back.RESET + " " + Back.GREEN + Fore.BLACK + "${:,.2f}".format(averagePrice) + Fore.RESET + Back.RESET)          # PRINT THE AVERAGE TO THE USER

if __name__ == "__main__":
    main()          # MAIN FUNCTION