import pyttsx3    #to speak
import os		
from pathlib import Path
import playsound 	#play music
import speech_recognition as sr
import verify
r=sr.Recognizer()
def play_audio(filename):
	playsound.playsound(filename, True)

def saysomething(textval):
	engine = pyttsx3.init()
	engine.say(textval)
	engine.setProperty('rate',100)
	engine.setProperty('volume', 0.9)
	engine.runAndWait()

def initSpeech():
	check=True
	while(check):
		play_audio("start.mp3")
		with sr.Microphone() as source:
			print("say something")
			audio=r.listen(source)
		play_audio("end.mp3")
		try:
			command=r.recognize_google(audio)
			check=False
		except:
			saysomething("Sorry..., could't catch that")
	print("You said  : "+command)

def getmail():
	check=True;
	while(check):
		saysomething("Please tell me the email id")
		emailid=initSpeech()
		saysomething("your email you said is  :"+emailid)
		saysomething("Do you want to change that ?")
		decision=initSpeech()
		if(decision!="yes" or decision !="s" ):
			check=False

	return emailid;

	




