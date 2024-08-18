from colorama import Fore, Back         # IMPORT 'Fore' AND 'Back' FROM 'colorama' TO USE COLORED TEXT IN SCRIPT
from phonenumbers import geocoder
from phonenumbers import carrier

import re                               # IMPORT 're' TO USE REGULAR EXPRESSION TO SEARCH FOR EMAIL FORMATS
import json
import requests                         # IMPORT 'requests' TO ALLOW FOR HTTP REQUEST TO APIs AND FETCH INFORMATION
import time                             # IMPORT 'time' TO ALLOW BREAKS BETWEEN LOOPS AND VERIFICATION

import phonenumbers
import sys

def periodStatements():
    time.sleep(1)                   # DELAY BY ONE SECOND
    print('.', end = " ")           # PRINT PERIOD ON SAME LINE
    time.sleep(1)                   # DELAY BY ONE SECOND
    print('.', end = " ")           # PRINT PERIOD ON SAME LINE
    time.sleep(1)                   # DELAY BY ONE SECOND
    print('.', end = " ")           # PRINT PERIOD ON SAME LINE
    time.sleep(1)                   # DELAY BY ONE SECOND

def fix_phonenumber(phoneNumber):
    phoneNumber = phoneNumber.replace('+', '')          # REPLACE ANY INSTANCE OF '+'
    phoneNumber = phoneNumber.replace('-', '')          # REPLACE ANY INSTANCE OF '-'
    phoneNumber = phoneNumber.replace('(', '')          # REPLACE ANY INSTANCE OF '('
    phoneNumber = phoneNumber.replace(')', '')          # REPLACE ANY INSTANCE OF ')'
    phoneNumber = phoneNumber.replace(' ', '')          # REPLACE ANY INSTANCE OF ' '

    if len(phoneNumber) == 10:                  # IF LENGTH OF PHONE NUMBER IS 10, ...
        phoneNumber = '1' + phoneNumber         # ..., APPEND 1 TO HEAD OF PHONE NUMBER

    verify_phonenumber(phoneNumber)         # VERIFY PHONE NUMBER USING FUNCTION

def verify_phonenumber(phoneNumber):
    # INFORMATION OBTAINED FROM: https://www.ipqualityscore.com/documentation/phone-number-validation-api/overview

    key = 'aa8d851eebmsh8d75dbabdcdd447p15ba20jsn35dac8e4e76f'
    url = "https://personator2.p.rapidapi.com/v3/WEB/ContactVerify/doContactVerify"
    querystring = {"act":"check,verify,append,move","format":"json","phone":f'{phoneNumber}'}
    headers = {"X-RapidAPI-Key": key, "X-RapidAPI-Host": "personator2.p.rapidapi.com"}
    
    response = requests.get(url, headers=headers, params=querystring)
    response = response.json()          # CONVERT RESPONSE INTO JSON FORMAT

    if 'Records' in response:
        records = response['Records']
        if records and records[0].get('AddressHouseNumber') != ' ' and records[0].get('NameFull') != ' ' and records[0].get('EmailAddress') != ' ':
            information = records[0]

            countryCode = information.get('CountryCode')
            countryName = information.get('CountryName')
            print(Back.YELLOW + Fore.RED + "Country Location:" + Fore.RESET + Back.RESET + ' ' + countryCode + ' - ' + countryName)

            addressNumber = information.get('AddressHouseNumber')
            addressDirection = information.get('AddressPreDirection')
            addressStreet = information.get('AddressStreetName')
            addressSuffix = information.get('AddressStreetSuffix')
            city = information.get('City')
            state = information.get('State')
            postalCode = information.get('PostalCode')
            print(Back.YELLOW + Fore.RED + "Related Address:" + Fore.RESET + Back.RESET + ' ' + addressNumber + ' ' + addressDirection + '. ' + addressStreet + ' ' + addressSuffix + '. ' + city + ', ' + state + ' ' + postalCode)

            email = information.get('EmailAddress')
            print(Back.YELLOW + Fore.RED + "Related Email:" + Fore.RESET + Back.RESET + ' ' + email)

            name = information.get('NameFull')
            print(Back.YELLOW + Fore.RED + "Related Name:" + Fore.RESET + Back.RESET + ' ' + name)
        else:
            print(Back.RED + Fore.BLACK + "ERROR: No Information Found. Try Again." + Fore.RESET + Back.RESET)
    else:
        print(Back.RED + Fore.BLACK + "ERROR: Invalid Phone Number." + Fore.RESET + Back.RESET)
    


def main():
    print(Back.GREEN + Fore.RED + "~~~ SAFEHOUSE: Fighting Real Estate Scams! ~~~" + Fore.RESET + Back.RESET)           # HEADER OF PROJECT
    print(Back.BLACK + Fore.WHITE + "Instruction: Provide the phone number listed." + Fore.RESET + Back.RESET)          # INSTRUCT USER TO INPUT THE PHONE NUMBER

    listingPhone = input(Back.WHITE + Fore.BLACK + 'Phone Number:' + Fore.RESET + Back.RESET + ' ')         # OBTAIN NUMBER FROM USER

    if len(listingPhone) != 11:                     # VERIFY PHONE NUMBER IS OF FORMAT: 1XXXXXXXXX AND LENGTH OF 11
        fix_phonenumber(listingPhone)               # IF FALSE, FIX PHONE NUMBER USING FUNCTION
    else:                                           # IF TRUE, ...
        verify_phonenumber(listingPhone)            # ..., VERIFY PHONE NUMBER USING FUNCTION

if __name__ == "__main__":
    main()          # MAIN FUNCTION