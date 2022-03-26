import pyttsx3

class Voice:
	def __init__(self):
		self.engine = pyttsx3.init('espeak')            # Initialize using Microsoft Speech API
		voices = self.engine.getProperty('voices')     # Gets properties of the current voice
		self.engine.setProperty('voice', voices[0].id)

	def speak(self, audio):
		self.engine.say(audio)
		self.engine.runAndWait() # Makes the audio available to the user
		
if __name__ == "__main__":
	fred = Voice()
	fred.speak('Put that away, idiot!')
