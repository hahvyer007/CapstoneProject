from colorama import Fore, Back         # IMPORT 'Fore' AND 'Back' FROM 'colorama' TO USE COLORED TEXT IN SCRIPT

import re                               # IMPORT 're' TO USE REGULAR EXPRESSION TO SEARCH FOR EMAIL FORMATS
import requests                         # IMPORT 'requests' TO ALLOW FOR HTTP REQUEST TO APIs AND FETCH INFORMATION
import time                             # IMPORT 'time' TO ALLOW BREAKS BETWEEN LOOPS AND VERIFICATION

listOfEmails = set()            # GLOBAL VARIABLE TO STORE EACH EMAIL FOUND GIVEN A URL

def find_email(url):
    # INFORMATION OBTAINED FROM: https://blog.finxter.com/how-to-extract-emails-from-any-website-using-python/

    try:                                                                                                                    # CATCH STATEMENT TO FIND ANY INVALID URL FED TO THE FUNCTION
        response = requests.get(url, timeout = 10)                                                                                        # SEND HTTP GET REQUEST TO URL
        instanceOfEmail = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', response.text, re.I)           # USE REGEX TO FIND ALL INSTANCES OF AN EMAIL ADDRESS IN SET FORMAT
        listOfEmails.update(instanceOfEmail)                                                                                # UDPATE GLOBAL VARIABLE WITH NEW EMAIL
    except requests.RequestException as error:                                                                              # CATCH IF URL IS INVALID
        print(Back.YELLOW + Fore.RED + 'ERROR: The URL provided is invalid. Try again.' + Fore.RESET + Back.RESET)          # PRINT ERROR MESSAGE
        exit()                                                                                                              # EXIT

    for uniqueEmail in listOfEmails:                                                                # ITERATE THROUGH GLOBAL SET VARIABLE
        print(Back.YELLOW + Fore.BLACK + 'FOUND: ' + uniqueEmail + Fore.RESET + Back.RESET)         # INFORM USER OF EMAIL FOUND
        validate_email(uniqueEmail)                                                                 # VALIDATE EMAIL USING DEFINED FUNCTION
        time.sleep(3)                                                                               # DELAY LOOP BY THREE SECONDS

def validate_email(email):
    # INFORMATION OBTAINED FROM: https://www.abstractapi.com/guides/how-to-validate-an-email-address-in-python

    api_key = 'e0ab34ea28da479e92ed377c53821ff6'                                                                    # API KEY PROVIDED BY: http://app.abstractapi.com (TO BE USED IN THESIS DEFENSE: e0ab34ea28da479e92ed377c53821ff6) - 2920fb2a70e345398a444d3e004b357c
    response = requests.get(f'https://emailvalidation.abstractapi.com/v1/?api_key={api_key}&email={email}')         # MAKE API REQUEST AND PERFORM A GET REQUEST

    data = response.json()          # PARSE RESPONSE AS JSON FORMAT (WILL CONVERT INTO PYTHON DICTIONARY)

    """

    # DOCUMENTATION PROVIDED BY: https://docs.abstractapi.com/email-validation

    {
        'email': 'jaguil37@asu.edu',            # VALUE FOR "email" ENTERED INTO THE REQUEST
        'autocorrect': 'jaguil37@aol.com',      # IF TYPO DETECTED, RETURNS A SUGGESTION OF THE CORRECT EMAIL
        'deliverability': 'DELIVERABLE',        # EVALUATION OF THE DELIVERABILITY OF THE EMAIL {DELIVERABLE, UNDELIVERABLE, UNKNOWN}
        'quality_score': '0.80',                # ABSTRACT'S CONFIDENCE IN QUALITY AND DELIVERABILITY OF GIVEN EMAIL {0.01 - 0.99}
        'is_valid_format': {                    # RETURNS TRUE IF EMAIL IS FOUND TO FOLLOW CONVENTIONAL FORMAT OF "address@domain.TLD"
            'value': True,
            'text': 'TRUE'
        },
        'is_free_email': {                      # RETURNS TRUE IF EMAIL IS FOUND AMONGST ABSTRACT'S LIST OF FREE EMAIL PROVIDERS (I.E. GOOGLE, YAHOO, ETC)
            'value': False,
            'text': 'FALSE'
        },
        'is_disposable_email': {                # RETURNS TRUE IF EMAIL IS FOUND AMONGST ABSTRACT'S LIST OF DISPOSABLE EMAIL PROVIDERS (I.E. MAILINATOR, YOPMAIL, ETC)
            'value': False,
            'text': 'FALSE'
        },
        'is_role_email': {                      # RETURNS TRUE IF EMAIL IS FOUND TO BE FOR A ROLE RATHER THAN AN INDIVIDUAL (I.E. TEAM@, SALES@, INFO@, ETC)
            'value': False,
            'text': 'FALSE'
        },
        'is_catchall_email': {                  # RETURNS TRUE IF EMAIL IS FOUND TO CATCH ALL EMAIL (https://www.corporatecomm.com/faqs/other-questions/what-is-a-catch-all-account)
            'value': None,
            'text': 'UNKNOWN'
        },
        'is_mx_found': {                        # RETURNS TRUE IF MX RECORDS FOR DOMAIN IS FOUND (https://www.thetechedvocate.org/what-is-a-mail-exchange-record-mx-record/)
            'value': True,
            'text': 'TRUE'
        },
        'is_smtp_valid': {                      # RETURNS TRUE IF SMTP CHECK OF THE EMAIL WAS SUCCESSFUL (https://sendgrid.com/blog/what-is-an-smtp-server/) ELSE RETURNS UNKNWON IF CHECK FAILS BUT OTHER CHECKS ARE VALID
            'value': True,
            'text': 'TRUE'
        }
    }

    """

    if data['autocorrect'] != '':                                                                                                   # IF THERE IS A SUGGESTED EMAIL CORRECTION, ...
        print(Back.CYAN + Fore.YELLOW + f"DID YOU MEAN: {data['autocorrect']}?" + Fore.RESET + Back.RESET)                          # INFORM THE USER
        userInput = input(Back.BLACK + Fore.WHITE + "Is this the correct email? (Y/N):" + Fore.RESET + Back.RESET + " ")            # ENSURE THE USER HAS OBTAINED THE CORRECT EMAIL

        if userInput == 'Y':                                                                                                # IF SUGGESTED EMAIL IS CORRECT, ...
            email = data['autocorrect']                                                                                     # UPDATE EMAIL VARIABLE
            response = requests.get(f'https://emailvalidation.abstractapi.com/v1/?api_key={api_key}&email={email}')         # NEW API REQUEST AND PERFORM A GET REQUEST
            data = response.json()                                                                                          # PARSE RESPONSE AS JSON FORMAT (WILL CONVERT INTO PYTHON DICTIONARY)
            time.sleep(1)                                                                                                   # DELAY BY TWO SECONDS

    manualScore = 0         # MANUAL SCORE TO BE COMPARED WITH API'S QUALITY SCORE

    # is_valid_format CHECK

    if data['is_valid_format']['value'] == True:                                                                    # API DETERMINES EMAIL FOLLOWS CONVENTIONAL FORMAT
        print(Back.GREEN + Fore.BLACK + '[+] EMAIL FOLLOWS CONVENTIONAL FORMAT.' + Fore.RESET + Back.RESET)         # INFORM USER
        manualScore += 20                                                                                           # UPDATE MANUAL SCORE
        time.sleep(1)                                                                                               # DELAY BY TWO SECONDS
    else:                                                                                                                           # API DETERMINES EMAIL DOES NOT FOLLLOW CONVENTIONAL FORMAT
        print(Back.RED + Fore.BLACK + '[-] WARNING: EMAIL DOES NOT FOLLOW CONVENTIONAL FORMAT' + Fore.RESET + Back.RESET)           # INFORM USER
        manualScore -= 20                                                                                                           # UPDATE MANUAL SCORE
        time.sleep(1)                                                                                                               # DELAY BY TWO SECONDS

    # is_free_email CHECK
        
    if data['is_free_email']['value'] == True:                                                                                  # API DETERMINES EMAIL IS FROM FREE EMAIL PROVIDERS
        print(Back.RED + Fore.BLACK + '[-] WARNING: EMAIL FOUND FROM FREE EMAIL PROVIDERS.' + Fore.RESET + Back.RESET)          # INFORM USER
        manualScore -= 10                                                                                                       # UPDATE MANUAL SCORE
        time.sleep(1)                                                                                                           # DELAY BY TWO SECONDS
    else:                                                                                                                       # API DETERMINES EMAIL IS NOT FROM FREE EMAIL PROVIDERS
        print(Back.GREEN + Fore.BLACK + '[+] EMAIL IS FROM A CORPORATION EMAIL PROVIDER.' + Fore.RESET + Back.RESET)            # INFORM USER
        manualScore += 10                                                                                                       # UPDATE MANUAL SCORE
        time.sleep(1)                                                                                                           # DELAY BY TWO SECONDS

    # is_disposable_email CHECK
        
    if data['is_disposable_email']['value'] == True:                                                            # API DETERMINES EMAIL MADE TO BE DISPOSABLE
        print(Back.RED + Fore.BLACK + '[-] WARNING: EMAIL IS DISPOSABLE.' + Fore.RESET + Back.RESET)            # INFORM USER
        manualScore -= 15                                                                                       # UPDATE MANUAL SCORE
        time.sleep(1)                                                                                           # DELAY BY TWO SECONDS
    else:                                                                                                   # API DETERMINES EMAIL NOT MADE TO BE DISPOSABLE
        print(Back.GREEN + Fore.BLACK + '[+] EMAIL IS NOT DISPOSABLE.' + Fore.RESET + Back.RESET)           # INFORM USER
        manualScore += 15                                                                                   # UPDATE MANUAL SCORE
        time.sleep(1)                                                                                       # DELAY BY TWO SECONDS

    # is_role_email CHECK
        
    if data['is_role_email']['value'] == True:                                                                      # API DETERMINES EMAIL MADE FOR ROLE USE
        print(Back.RED + Fore.BLACK + '[-] WARNING: EMAIL RELATED FOR ROLE USE.' + Fore.RESET + Back.RESET)         # INFORM USER
        manualScore -= 10                                                                                           # UPDATE MANUAL SCORE
        time.sleep(2)                                                                                               # DELAY BY TWO SECONDS
    else:                                                                                                           # API DETERMINES EMAIL MADE FOR INDIVIDUAL USE
        print(Back.GREEN + Fore.BLACK + '[+] EMAIL RELATED FOR INDIVIDUAL USE.' + Fore.RESET + Back.RESET)          # INFORM USER
        manualScore += 10                                                                                           # UPDATE MANUAL SCORE
        time.sleep(1)                                                                                               # DELAY BY TWO SECONDS

    # is_mx_found CHECK
        
    if data['is_mx_found']['value'] == True:                                                                # API DETERMINES DOMAIN CAN RECEIVE EMAILS
        print(Back.GREEN + Fore.BLACK + '[+] DOMAIN CAN RECEIVE EMAILS.' + Fore.RESET + Back.RESET)         # INFORM USER
        manualScore += 20                                                                                   # UPDATE MANUAL SCORE
        time.sleep(1)                                                                                       # DELAY BY TWO SECONDS
    else:                                                                                                               # API DETERMINES DOMAIN CANNOT RECEIVE EMAILS
        print(Back.RED + Fore.BLACK + '[-] WARNING: DOMAIN CANNOT RECEIVE EMAILS.' + Fore.RESET + Back.RESET)           # INFORM USER
        manualScore -= 20                                                                                               # UPDATE MANUAL SCORE
        time.sleep(1)                                                                                                   # DELAY BY TWO SECONDS

    # is_smtp_valid CHECK
        
    if data['is_smtp_valid']['value'] == True:                                                                                  # API DETERMINES EMAIL ADDRESS AS VALID
        print(Back.GREEN + Fore.BLACK + '[+] SERVER ACKNOWLEDGES EMAIL ADDRESS AS VALID.' + Fore.RESET + Back.RESET)            # INFORM USER
        manualScore += 25                                                                                                       # UPDATE MANUAL SCORE
        time.sleep(1)                                                                                                           # DELAY BY TWO SECONDS
    else:                                                                                                                                   # API DETERMINES EMAIL ADDRESS AS NOT VALID
        print(Back.RED + Fore.BLACK + '[-] WARNING: SERVER DOES NOT ACKNOWLEDGE EMAIL ADDRESS AS VALID.' + Fore.RESET + Back.RESET)         # INFORM USER
        manualScore -= 25                                                                                                                   # UPDATE MANUAL SCORE
        time.sleep(1)                                                                                                                       # DELAY BY TWO SECONDS

    """

    WEIGHTING SYSTEM

    is_valid_format: a valid email format is crucial for email legitimacy
    + 20 : significant role in determining email legitimacy
    - 20 : significant risk associated in determining email legitimacy

    is_free_email: emails from free providers may associate with misuse and less credibility
    + 10 : email credible (but may still lead to misuse)
    - 10 : email NOT credible

    is_disposable_email: disposable emails frequently used for temporary purposes (suspicious activities)
    + 15 : not associated with suspicious activites
    - 15 : may associate with suspicious activites

    is_role_email: emails associated with personal use may increase trustworthiness
    + 10 : acknowledge personal use (increase trustworthiness)
    - 10 : acknowledge role use (decrease trustworthiness)

    is_mx_found: ability of domain to receive emails
    + 20 : inability to receive emails
    - 20 : ability to receive emails

    is_smtp_valid: server acknowledgement
    + 25 : server validates email (credibility gained)
    - 25 : server does NOT validate email (credibility lost)

    """

    if(manualScore == 100):         # SCORE SHOULD NEVER REACH 100% ACCURACY
        manualScore -= 1            # IF SCORE IS 100%, DECREASE BY 1
    elif(manualScore == -100):          # SCORE SHOULD NEVER REACH -100% ACCURACY
        manualScore += 1                # IF SCORE IS -100%, INCREASE BY 1
    elif(manualScore < 0):
        manualScore = 10

    if(manualScore > 89):                                                                           # SCORE: 90 - 99
        print(Back.GREEN + Fore.BLACK + f'SCORE: {manualScore}%' + Fore.RESET + Back.RESET)         # INFORM USER OF SCORE
        print(Back.GREEN + Fore.BLACK + 'EMAIL ADDRESS IS SAFE' + Fore.RESET + Back.RESET)          # INFORM USER OF EVALUATION
    elif(manualScore < 90 and manualScore > 69):                                                                                        # SCORE: 70 - 89
        print(Back.YELLOW + Fore.BLACK + f'SCORE: {manualScore}%' + Fore.RESET + Back.RESET)                                            # INFORM USER OF SCORE
        print(Back.YELLOW + Fore.BLACK + 'EMAIL ADDRESS IS CONSIDERED SAFE - PROCEED WITH CAUTION' + Fore.RESET + Back.RESET)           # INFORM USER OF EVALUATION
    elif(manualScore < 70 and manualScore > 49):                                                                                                # SCORE: 50 - 70
        print(Back.CYAN + Fore.BLACK + f'SCORE: {manualScore}%' + Fore.RESET + Back.RESET)                                                      # INFORM USER OF SCORE
        print(Back.CYAN + Fore.BLACK + 'EMAIL ADDRESS IS NOT CONSIDERED SAFE - PERFORM OTHER VERIFICATION' + Fore.RESET + Back.RESET)           # INFORM USER OF EVALUATION
    else:                                                                                               # SCORE: LESS THAN 50
        print(Back.RED + Fore.BLACK + f'SCORE: {manualScore}%' + Fore.RESET + Back.RESET)               # INFORM USER OF SCORE
        print(Back.RED + Fore.BLACK + 'EMAIL ADDRESS IS NOT SAFE' + Fore.RESET + Back.RESET)            # INFORM USER OF EVALUATION

def main():
    print(Back.GREEN + Fore.RED + "~~~ SAFEHOUSE: Fighting Real Estate Scams! ~~~" + Fore.RESET + Back.RESET)                       # HEADER OF PROJECT
    print(Back.BLACK + Fore.WHITE + "Instruction: Provide the direct URL to the listing page." + Fore.RESET + Back.RESET)           # INSTRUCT USER TO INPUT THE DIRECT URL TO THE LISTING

    url = input(Back.WHITE + Fore.BLACK + 'URL:' + Fore.RESET + Back.RESET + ' ')           # OBTAIN URL FROM USER

    if "https://" in url:               # VERIFY URL BEGINS WITH 'https://'
        find_email(url)                 # IF TRUE, PROCEED
    else:                               # IF FALSE, ...
        url = "https://" + url          # ... APPEND 'https://'
        find_email(url)                 # PROCEED

    if len(listOfEmails) == 0:                                                                                      # CASE: NO EMAIL FOUND USING DIRECT URL
        print(Back.YELLOW + Fore.RED + 'Unfortunately, no email can be found.' + Fore.RESET + Back.RESET)           # INFORM USER NO EMAIL WAS FOUND
        print(Back.BLACK + Fore.WHITE + "Manually provide an email." + Fore.RESET + Back.RESET)                     # ALLOW USER TO MANUALLY INPUT EMAIL
        email = input(Back.WHITE + Fore.BLACK + "Email:" + Fore.RESET + Back.RESET + " ")                           # ALLOW USER TO MANUALLY INPUT EMAIL
        validate_email(email)                                                                                       # JUMP TO 'validate_email' FUNCTION

if __name__ == "__main__":
    main()          # MAIN FUNCTION