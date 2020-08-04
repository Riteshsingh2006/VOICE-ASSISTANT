import playsound
import wikipedia
from datetime import datetime
import os
import webbrowser

import re
import pygame
import wolframalpha
import requests
import pyaudio
import datetime
import speech_recognition as sr
from pytz import timezone
from gtts import gTTS
import re
from pyowm import OWM

def speak(text):
    tts = gTTS(text=text, lang=&#39;en&#39;)
    tts.save(&quot;audio.mp3&quot;)
    file = &#39;audio.mp3&#39;
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()
    
def listen():
    r = sr.Recognizer()
    text=&#39;&#39;
    with sr.Microphone() as source:
        print(&quot;speak&quot;)

        speak(&quot;Speak...&quot;)
        audio = r.listen(source, phrase_time_limit = 3)
        try:
            text= r.recognize_google(audio, language =&#39;en-US&#39;)
            text=text.lower()
            print(&quot;You : &quot;, text)
        except :
            pass
            
        return text
    
def wish():
    hour = datetime.datetime.now()
    hour= (hour.astimezone(timezone(&#39;Asia/kolkata&#39;))).hour
    print(hour)
    if hour&gt;=0 and hour&lt;12:
        speak(&quot;Good Morning!&quot;)
    elif hour&gt;=12 and hour&lt;18:
        speak(&quot;Good Afternoon!&quot;)   
    else:
        speak(&quot;Good Evening!&quot;)
    speak(&quot;how can i help u&quot;)

def control(query):
        import RPi.GPIO as GPIO
        from time import sleep

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(3, GPIO.OUT, initial=GPIO.LOW)
        if common(query,[[&quot;led&quot;,&quot;on&quot;]])==True:
            GPIO.output(8, GPIO.HIGH)
            print(&quot;led is turned on&quot;)
            speak(&quot;led is turned on&quot;)
        if common(query,[[&quot;led&quot;,&quot;off&quot;]])==True:
            GPIO.output(8, GPIO.LOW)
            print(&quot;led is turned off&quot;)
            speak(&quot;led is turned off&quot;)
        if common(query,[[&quot;buzzer&quot;,&quot;on&quot;],[&quot;play&quot;,&quot;sound&quot;]])==True:
            GPIO.output(3, GPIO.LOW)
            print(&quot;buzzer is turned on&quot;)
            speak(&quot;buzzer is turned on&quot;)
        if common(query,[[&quot;buzzer&quot;,&quot;off&quot;],[&quot;stop&quot;,&quot;sound&quot;]])==True:
            GPIO.output(3, GPIO.LOW)
            print(&quot;buzzer is turned off&quot;)
            speak(&quot;buzzer is turned off&quot;)
             
def search(text):
    try:
        results = wikipedia.summary(text, sentences=2)
        print(results)
        speak(results)

    except:
        pass
    return 0
    
def calculate(query):
    app_id = &quot;TH57PT-W4XYVTEY5L&quot;
    client = wolframalpha.Client(app_id) 
    indx = query.lower().split().index(&quot;calculate&quot;) 
    query = query.split()[indx + 1:] 
    res = client.query(&#39; &#39;.join(query))
    try:
        answer = next(res.results).text
        print(answer)
        speak(answer)
    except:
        pass
    return 0

def note(text):
    fd=os.open(&quot;py.txt&quot;,os.O_RDWR|os.O_CREAT)
    line = text
    b = str.encode(line)
    try:
        os.write(fd, b)
        os.close(fd)
        print(&quot;note created on desktop,thank u&quot;)

        speak(&quot;note created on desktop,thank u&quot;)
    except:
        pass
    return 0

def location(text):
    indx=0
    if &quot;location&quot; in text:
        indx = text.lower().split().index(&quot;location&quot;)
    elif &quot;map&quot; in text:
        indx = text.lower().split().index(&quot;map&quot;)
    text = text.split()[indx + 1:]
    location = text[1]
    try:
        os.system(&quot;chromium-browser https://www.google.nl/maps/place/&quot; + location + &quot;/&amp;amp;&quot;)
    except :
        pass
    return 0
    
def browse(text):
    reg_ex = re.search(&#39;open (.+)&#39;,text)
    if reg_ex:
        domain = reg_ex.group(1)
        print(domain)
        url = &#39;https://www.&#39;+ domain +&#39;.com&#39;
        print(url)

        try:
            webbrowser.open(url)
            print(&quot;you have opened &quot;+text+&quot; succesfully&quot;)
            speak(&quot;you have opened &quot;+text+&quot; succesfully&quot;)
        except:
            pass
        return 0
    
def weather(text):
    reg_ex = re.search(&#39; weather in (.*)&#39;, text)
    if reg_ex:
        try:
            city = reg_ex.group(1)
            owm = OWM(API_key=&#39;ab0d5e80e8dafb2cb81fa9e82431c1fa&#39;)
            obs = owm.weather_at_place(city)
            w = obs.get_weather()
            k = w.get_status()
            x = w.get_temperature(unit=&#39;celsius&#39;)
            print(&#39;Current weather in %s is %s. The maximum temperature is %0.2f and the
minimum temperature is %0.2f degree celcius&#39; % (city, k, x[&#39;temp_max&#39;], x[&#39;temp_min&#39;]))
            speak(&#39;Current weather in %s is %s. The maximum temperature is %0.2f and the
minimum temperature is %0.2f degree celcius&#39; % (city, k, x[&#39;temp_max&#39;], x[&#39;temp_min&#39;]))
        except:
            pass
        return 0
        
def date():

    time = datetime.datetime.now()
    time = time.astimezone(timezone(&#39;Asia/kolkata&#39;))
    print(&#39;todays date is %d day %s month %d year&#39;%(time.day,time.month,time.year))
    speak(&#39;todays date is %d day %s month %d year&#39;%(time.day,time.month,time.year))

def time():
    hour=datetime.datetime.now()
    hour=(hour.astimezone(timezone(&#39;Asia/kolkata&#39;)))
    print(&#39;Current time is %d hours %d minutes&#39; % (hour.hour, hour.minute))
    speak(&#39;Current time is %d hours %d minutes&#39; % (hour.hour, hour.minute))

def substring(text,matchlist):
    res = [ele for ele in matchlist if(ele in text)]
    s=bool(res)
    return s
    
def common(text,matchlist):
    s=False
    for i in range(len(matchlist)):
        res = [all([k in text for k in matchlist[i]])]
        if res[0]==True:
            s=True
    return s

if __name__ == &quot;__main__&quot;:
    wish()

    while True:
        query=listen()
        print(query)
        if query == &quot;&quot;:
            continue
        elif common(query,[[&quot;who&quot;,&quot;you&quot;],[&quot;describe&quot;,&quot;yourself&quot;],[&quot;give&quot;,&quot;introduction&quot;]])==True:
            speak(&quot;Hello, I am  Your personal Assistant.I am here to make your life easier&quot;)
        elif common(query,[[&quot;created&quot;,&quot;you&quot;],[&quot;made&quot;,&quot;you&quot;],[&quot;your&quot;,&quot;inventor&quot;]])==True:
            speak(&quot;I am created by Ritesh singh&quot;)
        elif common(query,[[&quot;how&quot;,&quot;you&quot;],[&quot;whats&quot;,&quot;going&quot;],[&quot;everything&quot;,&quot;fine&quot;]])==True:
            speak(&quot;ya i am fine , hope u r alo same &quot;)
        elif common(query,[[&quot;when&quot;,&quot;invented&quot;,&quot;you&quot;],[&quot;birthday&quot;,&quot;your&quot;],[&quot;you&quot;,&quot;created&quot;]])==True:
            speak(&quot;my birthday is on 5 november 2019&quot;)
        elif common(query,[[&quot;goodbye&quot;],[&quot;sleep&quot;,],[&quot;exit&quot;]])==True:
            speak(&quot;ok bye , have a nice day . meet u again &quot;)
            break
        elif substring(query,[&quot;location&quot;,&quot;map&quot;])==True:
            location(query)
        elif substring(query,[&quot;led&quot;,&quot;buzzer&quot;,&quot;motor&quot;])==True:
            control(query)
        elif substring(query,[&quot;calculate&quot;])==True:
            calculate(query)
        elif substring(query,[&quot;reminder&quot;,&quot;note&quot;,&quot;write&quot;,&quot;create file&quot;])==True:
            print(&quot;what do u want to note down ?&quot;)
            text=listen()
            note(text)

        elif substring(query,[&quot;browse&quot;,&quot;open&quot;,&quot;play&quot;,&quot;start&quot;])==True:
            query=query.replace(&quot;browse&quot;,&quot;open&quot;)
            query=query.replace(&quot;play&quot;,&quot;open&quot;)
            query=query.replace(&quot;start&quot;,&quot;open&quot;)
            browse(query)
        elif common(query,[[&quot;what&quot;,&quot;time&quot;],[&quot;current&quot;,&quot;time&quot;],[&quot;clock&quot;,&quot;status&quot;]])==True:
            time()
        elif common(query,[[&quot;today&quot;,&quot;date&quot;],[&quot;day&quot;,&quot;year&quot;],[&quot;current&quot;,&quot;date&quot;]])==True:
            date()
        elif substring(query,[&quot;weather in&quot;])==True:
            weather(query)
        else:
            search(query)

WORKING
