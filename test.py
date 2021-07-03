import random

def dumb_case(message: str)-> str:
    dumb_case_msg = []
    counter = 0
    for letter in message:
        if counter % 2 == 0:
            dumb_case_msg.append(letter.lower())
        else:
            dumb_case_msg.append(letter.upper())
        counter+=1
    return ''.join(dumb_case_msg)


choice = 'y'

while choice == 'y':
    sentence = input("Enter a sentence to dumbcase: ")
    print(dumb_case(sentence))
    choice = input("Continue?:\n")