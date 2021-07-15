'''
    IF YOU PLAN ON USING THIS FOR COMMERCIAL
    USE, PLEASE LOOK INTO MAKING A CHAT BOT AI,
    (I AM MAKING A CHAT BOT AI MODULE IF YOU WANT TO
    LOOK INTO THAT, IT'S CALLED TBAI-1, IT MAY NOT BE
    PUBLIC AT THE TIME YOU ARE LOOKING AT THIS - IT HANDLES
    EVERYTHING FOR YOU, THOUGH. IT'S GOOD FOR BEGINNERS).

    THIS IS PURELY FOR ENTERTAINMENT AND LEARNING
    POURPUSES AND I AM IN NO WAY LIABLE OF WHAT ANYONE
    MAKES OUT OF THIS.

    THIS PROJECT IS OPEN SOURCE AND FREE FOR EVERYONE,
    IT IS UNDER NO LICENSE OR COPYRIGHT.
'''

# imports
import json # used for settings
import speech_recognition as sr # used for speech recog
import wikipedia as wiki # used for looking up on wikipedia
import pyttsx3 # used for text to speech responses

config = json.loads(open("configuration.file").read())
print("Language configuration: {0} (change using \"set language\" command".format(config["language"]))

engine = pyttsx3.init() # initializes pyttsx3
engine.setProperty("rate", 200) # sets the TTS speed
engine.setProperty("volume", 0.7) # sets the volume of the TTS, 0.7 = 70% etc

rec = sr.Recognizer() # records the voice
mic = sr.Microphone(device_index = 1) # the default microphone
shutdown = False # handles the shutdown command, used later in while loop

def respond(saythis):
    print(saythis) # prints the response
    engine.say(saythis) # says the response
    engine.runAndWait() # runs engine.say() and pauses process until finished

while shutdown == False:
    with mic as source_audio: # uses mic with variable name of source_audio
        print("Say something!") # notifys the user that the voice recog is listening
        audio = rec.adjust_for_ambient_noise(source_audio) # adjusts ambient noise, making responses quicker and more accurate
        audio = rec.listen(source_audio) # listens for mic

    try:
        recog = rec.recognize_google(audio, language = config["language"]) # uses google to recgonize the given audio in the English language
        
        print("USER: {0}".format(recog)) # prints what the user said, good for troubleshooting
        if recog == "hello world": # check if the recog is equal to hello world, use the respond function to respond with "Hello to you too!"
            respond("Hello to you too!")
        elif recog == "how are you":
            respond("Good!")
        elif recog == "shutdown":
            respond("Shutting down...")
            shutdown = True
        elif recog.startswith("what is"):
            respond(wiki.summary(str(list(recog[slice(2)])), sentences = 5)) # this doesn't work but it's fine as it is
            respond("Read more on Wikipedia!")
        elif recog.startswith("set language"):
            recog_set = [i for j, i in enumerate(list(recog)) if j not in [0,1,2,3,4,5,6,7,8,9,10,11,12]] # remove "set language " from the list
            try:
                if("".join(recog_set) == "English"):
                    config["language"] = "en-US" # set "language" in configuration file to en-US
                    respond("Set language to English!")
                else:
                    respond("I cannot set the language to {0}".format("".join(recog_set)))
            except:
                respond("An unknown error occured")
        else: # defaults to this if all conditions are false
            respond("I don't understand what you said.")

    # not explaining the exceptions, just know its good to have these
    except sr.UnknownValueError:
        print("Google could not recognize what you were saying!")
    except sr.RequestError as e:
        print("Google could not complete your request: {0}".format(e))