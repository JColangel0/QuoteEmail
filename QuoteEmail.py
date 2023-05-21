"""
    Program to email one quote from this database each day
"""
import random
from email.message import EmailMessage
import os
import ssl
import smtplib

progress = open("Progress.txt", "r")
usedIndices = []
for x in progress:
    usedIndices.append(int(x))
progress.close()


def getMaxIndex():
    quotes = open("Quotes.txt", "r")
    data = quotes.read()
    quotes.close()

    startValue = -1
    maxIndex = data[startValue]
    while maxIndex != "\n":
        startValue -= 1
        maxIndex = data[startValue]
    startValue += 1
    stopValue = startValue
    while maxIndex != ".":
        stopValue += 1
        maxIndex = data[stopValue]
    return int(data[startValue:stopValue])


def generateQuote():
    maxIndex = getMaxIndex()
    index = random.randrange(maxIndex)

    while index in usedIndices:
        index = random.randrange(maxIndex)

    used = open("Progress.txt", "a")
    used.write(str(index)+"\n")
    used.close()

    quote = ""
    with open("Quotes.txt") as lines:
        for x in lines:
            if str(index) in x:
                quote = x
                break
        return quote


def sendEmail():
    sender = 'dailyquoteemail@gmail.com'
    password = os.environ.get("QUOTE_EMAIL_PASSWORD")
    receiver = os.environ.get("QUOTE_EMAIL_RECIPIENT")
    subject = "Quote Number: " + str(len(usedIndices)+1)
    body = generateQuote()

    em = EmailMessage()
    em['From'] = sender
    em['To'] = receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(sender, password)
        smtp.sendmail(sender, receiver, em.as_string())


sendEmail()
