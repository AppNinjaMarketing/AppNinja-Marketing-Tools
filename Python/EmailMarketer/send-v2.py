#!/usr/bin/python

import smtplib
import sys
import os
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import base64

__location__ = os.path.dirname(__file__)

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

numberOfEmails = 0
fromAddress = ""
bccAddress = ""
appName = ""
appUrl = ""
isAndroid = True
emailNumber = 1

def readInfo():
    with open(os.path.join(__location__, "Info.txt")) as text_file:
        info = text_file.readlines()

    global numberOfEmails, fromAddress, bccAddress, appName, appUrl, isAndroid, emailNumber

    numberOfEmails = int(info[0])
    fromAddress = info[1].strip()
    bccAddress = info[2].strip()
    appName = info[3].strip()
    appUrl = info[4].strip()
    isAndroid = "Y" in info[5].upper()
    emailNumber = int(info[6])

def verify():
    print("Is the following information correct?:\n")
    print(f"Number of Emails:\t{numberOfEmails}")
    print(f"From Address:\t\t{fromAddress}")
    print(f"BCC Address:\t\t{bccAddress}")
    print(f"App Name:\t\t{appName}")
    print(f"App URL:\t\t{appUrl}")
    print(f"isAndroid:\t\t{isAndroid}")
    print(f"startingNumber:\t\t{emailNumber}")

    answer = input("Y = Yes, N = no\n\n")
    if answer.lower() != "y":
        print("Exiting...")
        sys.exit()

def readEmailList(isAndroid):
    filename = "AndroidEmailList.txt" if isAndroid else "IphoneEmailList.txt"
    with open(filename, "r") as text_file:
        return text_file.readlines()

def readEmailMessageList():
    with open("EmailMessages.txt", "r") as text_file:
        return text_file.readlines()[0::2]

def composeEmailMessage(message, appName, appUrl):
    newMessage = message.replace("[appname]", appName.strip())
    return f"Hi there,\n\n{newMessage.strip()}\n\nHere is the link to the app:\n{appUrl}\nThank you!"

def get_gmail_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def sendEmail(service, fromAddress, toAddress, subject, message):
    print(f"from: {fromAddress} to: {toAddress}")

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = fromAddress
    msg['To'] = toAddress

    body = MIMEText(message, 'plain')
    msg.attach(body)

    raw_message = {'raw': base64.urlsafe_b64encode(msg.as_bytes()).decode()}
    
    try:
        message = service.users().messages().send(userId="me", body=raw_message).execute()
        print(f"Message Id: {message['id']}")
    except Exception as error:
        print(f'An error occurred: {error}')

def readSubjectLines():
    with open(os.path.join(__location__, "SubjectLines.txt"), "r") as file:
        return [line.strip() for line in file if line.strip()]

def chooseSubjectLine(subjectLines, appName):
    subject = random.choice(subjectLines)
    return subject.replace("[appname]", appName)

print("Running...")

readInfo()
verify()
print("Sending...")

emailList = readEmailList(isAndroid)
emailMessageList = readEmailMessageList()
subjectLines = readSubjectLines()
random.shuffle(emailMessageList)
messageCount = emailNumber

print(messageCount)

service = get_gmail_service()

for num in range(numberOfEmails):
    finalMessage = composeEmailMessage(emailMessageList[messageCount % len(emailMessageList)], appName, appUrl)
    subject = chooseSubjectLine(subjectLines, appName)
    
    sendEmail(service, fromAddress, emailList[messageCount % len(emailList)], subject, finalMessage)
    sendEmail(service, fromAddress, bccAddress, f"Campaign Email #{messageCount + 1}", 
             f"This is a message from AppNinja letting you know for your marketing campaign the following message was sent to the email {emailList[messageCount % len(emailList)]}\n\n{finalMessage}")

    print(f"{num + 1} sent\n")
    messageCount += 1

    time.sleep(5)

print("\nSuccess!")