import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia as wk
import smtplib
import ssl
import webbrowser as wb
import os
import pyautogui as pag
import cv2
import psutil
import pyjokes
from getpass import getpass

engine = pyttsx3.init()

query = "None"


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def time():
    Time = datetime.datetime.now().strftime("%I:%M:%S")
    speak("The time now is")
    speak(Time)
    print(Time)


def date():
    yr = int(datetime.datetime.now().year)

    mnth = datetime.datetime.now().month
    if(mnth == 1):
        mnth = "January"
    elif(mnth == 2):
        mnth = "February"
    elif(mnth == 3):
        mnth = "March"
    elif(mnth == 4):
        mnth = "April"
    elif(mnth == 5):
        mnth = "May"
    elif(mnth == 6):
        mnth = "June"
    elif(mnth == 7):
        mnth = "July"
    elif(mnth == 8):
        mnth = "August"
    elif(mnth == 9):
        mnth = "September"
    elif(mnth == 10):
        mnth = "October"
    elif(mnth == 11):
        mnth = "November"
    elif(mnth == 12):
        mnth = "December"

    date = int(datetime.datetime.now().day)

    speak("Today's date is")
    speak(date)
    speak(mnth)
    speak(yr)
    print(date, "-", mnth, "-", yr)


def greet():
    timeofday = datetime.datetime.now().hour
    # print(timeofday)
    if timeofday >= 0 and timeofday < 12:
        speak("Good Morning Corvo, This is JARVIS")
    elif timeofday >= 12 and timeofday < 17:
        speak("Good Afternoon Corvo, This is JARVIS")
    elif timeofday >= 17 and timeofday < 20:
        speak("Good Evening Corvo, This is JARVIS")
    elif timeofday >= 20 and timeofday < 23.59:
        speak("Welcome back Corvo, This is JARVIS")

    speak("Hope you are having a good day sir!!")
    speak("I am at your service, just let me know what you need!!")


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Waiting for your command Sir!!")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        speak("As you say Sir!!")
        global query
        query = r.recognize_google(audio, language='en-in')
        print("Corvo : ", query)
    except:
        speak("I am sorry Sir, I couldn't quite catch your command")
        speak("Could you please tell me again?")
        takeCommand()

    return query


def sendEmail(to, content):
    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
        speak("Please enter your password Sir")
        #password = input("Enter your password:- ")
        password = getpass()
        server.login('ygandhi2325.yg@gmail.com', password)
        speak("Login Successful Sir, Now sending the mail")
        server.sendmail('ygandhi2325.yg@gmail.com', to, content)
        server.close()


def screenshot():
    img = pag.screenshot()
    img.save(
        'D:/All Certificaiton Courses Completed/AI Assistant with Python/screenshots/ss.png')


def cpu():
    usage = str(psutil.cpu_percent())
    speak("CPU usage is at " + usage + "percent")
    print("CPU usage: ", usage)
    battery = psutil.sensors_battery()
    battery_remaining = str(battery.percent)
    speak("Battery is at " + battery_remaining + " percent")
    print("Battery percent: ", battery.percent)


def jokes():
    speak(pyjokes.get_joke())


if __name__ == "__main__":
    greet()
    while True:
        query = takeCommand().lower()

        if 'time' in query:
            time()
            speak("Task accomplished sir")

        elif 'date' in query:
            date()
            speak("Task accomplished sir")

        elif 'search' in query:
            speak("I shall search it for you Sir!!")
            result = wk.summary(query, sentences=2)
            speak(result)
            print(result)

        elif 'send an email' in query:
            try:
                speak("What message should I send Sir ?")
                content = takeCommand()
                speak("The content of the message will be as follows sir")
                speak(content)

                to = ["ygandhi2325.yg@gmail.com"]

                sendEmail(to, content)
                speak("Email sent Successfully")
            except:
                speak("I am sorry Sir, I was unable to send the Email sir")

        elif 'google' in query:
            speak("What should I google Sir ?")
            chromepath = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
            find = takeCommand().lower()
            find_query = str(find)
            for q in range(len(find_query)):
                if find_query[q] == " ":
                    find_query[q].replace(" ", "-")
            wb.get(chromepath).open_new_tab(find_query)

        elif 'logout' in query:
            speak("Logging out of the system Sir !!")
            os.system("shutdown -l")

        elif 'shutdown' in query:
            speak("Shutting down the system Sir, Have a good day ahead !!!")
            os.system("shutdown /s /t 1")

        elif 'restart' in query:
            speak("Restarting your system Sir, please give me a moment !!")
            os.system("shutdown /r /t 1")

        elif 'play songs' in query:
            songs_dir = 'D:/Music'
            songs = os.listdir(songs_dir)
            os.startfile(os.path.join(songs_dir, songs[0]))

        elif 'remember' in query:
            speak("What do you want me to remember Sir ?")
            data = takeCommand()
            speak("You have asked me to remember" + data)
            remember = open('data.txt', 'a')
            remember.write(data)
            remember.write("\n")
            remember.close()
            speak("I have added it to your reminders Sir")

        elif 'remind' in query:
            data_file = open('data.txt', 'r')
            contents = data_file.read()
            speak("These are the tasks that you had asked me to remember")
            speak(contents)

        elif 'screenshot' in query:
            speak("Clicking a snapshot for you Sir")
            screenshot()
            speak("Screenshot ready to be viewed !!")
            speak("Do you want me to show you the Snapshot ?")
            user = takeCommand().lower()
            if("yes" in user):
                content = cv2.imread('./screenshots/ss.png')
                cv2.imshow("Screenshot", content)
            elif "no" in user:
                pass

        elif 'computer details' in query:
            speak("Your laptop details are as follows:")
            cpu()

        elif 'joke' in query:
            speak("Sure, why not !! Here's a joke for you")
            jokes()

        elif 'offline' in query:
            speak("Going offline Sir!!")
            quit()
