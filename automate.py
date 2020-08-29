from PIL import Image, ImageOps
import pytesseract
import adb
import json
import time
import re
import random

# FILTERING/FARMING FOR: ENTERTAINMENT CATEGORY

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract'

# these are manually calculated. Please add ur own buttons here (x,y)
myButtons = {"start": (561, 1625), "first":(880, 1089), "second":(880, 1236), "third":(880, 1400), "fourth":(880, 1536), "next":(710, 1678), "done":(311, 1678)} 

mySmallOptions = {"first":(184,1044,886,1142), "second":(184,1193, 886, 1292), "third":(184, 1342, 886, 1437), "fourth":(184, 1487, 886, 1580)} # you my need to edit these for yourself
myBigOptions = {"first":(184,1098,886,1192), "second":(184,1247, 886, 1336), "third":(184, 1393, 886, 1495), "fourth":(184, 1543, 886, 1615)} # you my need to edit these for yourself


with open('questions.json') as json_file:
    myQuestions = json.load(json_file)

# Check if the answer was green, correct
def checkanswerstatus(device, choices, questionText):
    # change crop aspect ratio based on question length
    myCurOptions = {}
    if (len(questionText) < 38):
        myCurOptions = mySmallOptions.copy()
    else:
        myCurOptions = myBigOptions.copy()

    adb.take_screenshot(device)
    answerimagecropped = Image.open('screen.png').convert('RGB')
    grayscaleimg = (ImageOps.invert(Image.open('screen.png').convert('RGB'))).convert('LA')
    # checking all choice
    for i in range(0,4):
        (r, g, b) = answerimagecropped.getpixel((myButtons[choices[i]][0], myButtons[choices[i]][1]))
        if (g > 200) and (r < 180) and (b < 180):
            temp = grayscaleimg.crop(myCurOptions[choices[i]]).convert('RGB')
            newval = re.sub('\s+',' ', pytesseract.image_to_string(temp)).strip().lstrip()
            print("The correct answer is:")
            print(newval)
            myQuestions[questionText] = newval
            break


# Check if the answer was green, correct
def getanswer(device, questionText):
    # change crop aspect ratio based on question length
    myCurOptions = {}
    if (len(questionText) < 38):
        myCurOptions = mySmallOptions.copy()
    else:
        myCurOptions = myBigOptions.copy()

    adb.take_screenshot(device)
    grayscaleimg = Image.open('screen.png').convert('RGB')
    choices = ["first", "second", "third", "fourth"]
    # checking all choice
    for i in range(0,4):
        temp = grayscaleimg.crop(myCurOptions[choices[i]]).convert('RGB')
        response = pytesseract.image_to_string(temp)
        if myQuestions[questionText] in response:
            print("The found answer is:")
            print(response)
            device.shell(f'input tap {myButtons[choices[i]][0]} {myButtons[choices[i]][1]}')
            device.shell(f'input tap {myButtons[choices[i]][0]} {myButtons[choices[i]][1]}')
            break
    

    

def process_question(device):
    # Take Screenshot of the screen and save it in screen.png, crop, get question text
    adb.take_screenshot(device)
    questionimage = Image.open('screen.png')
    questionText = re.sub('\s+',' ', pytesseract.image_to_string(questionimage.crop((107,760, 1018, 983)))).lstrip().strip()

    # check if question exists, if so give correct answer
    if ((questionText in myQuestions) and (any((c.isalpha() or c.isnumeric()) for c in myQuestions[questionText]))):
            getanswer(device, questionText)  
            #time.sleep(0.5)

    else:
        # doesnt exist, need to choose random answer
        choices = ["first", "second", "third", "fourth"]
        randomchoice = random.choice(choices)

        device.shell(f'input tap {myButtons[randomchoice][0]} {myButtons[randomchoice][1]}')
        device.shell(f'input tap {myButtons[randomchoice][0]} {myButtons[randomchoice][1]}')
        #time.sleep(0.5)

        # now find the correct answer and store it
        checkanswerstatus(device, choices, questionText)  



if __name__ == "__main__":
    # Connect the device using ADB
    device = adb.connect_device()

    # Press start on the start screen
    device.shell(f'input tap {myButtons["start"][0]} {myButtons["start"][1]}')

    # run for 200 points straight
    for i in range(0,10001):
        time.sleep(0.4)
        process_question(device)
        # save to JSON every 25 questions
        if (i % 50 == 0 and i != 0): k
            with open('questions.json', 'w') as outfile:
                json.dump(myQuestions, outfile)
            print("saved to json!")
        # move onto next question
        device.shell(f'input tap {myButtons["next"][0]} {myButtons["next"][1]}') 

    # end game session
    device.shell(f'input tap {myButtons["done"][0]} {myButtons["done"][1]}')


