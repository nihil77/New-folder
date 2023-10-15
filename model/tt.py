import pyttsx3


# Initialize the Speech Engine
engine = pyttsx3.init()

# Text you want to convert to speech
text = "Man, I don't give a fuck who it is I spent  from tryna go to Don't give a fuck what y'all on Man, fuck all of you All of you"

# Use the speech engine to say the text
engine.say(text)

# Block while processing all the currently queued commands
engine.runAndWait()
