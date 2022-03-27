import pyttsx3

class Voice:
	def __init__(self):
		self.engine = pyttsx3.init('espeak')            # Initialize using Microsoft Speech API
		voices = self.engine.getProperty('voices')     # Gets properties of the current voice
		self.engine.setProperty('voice', voices[2].id)

	def speak(self, audio):
		self.engine.say(audio)
		self.engine.runAndWait() # Makes the audio available to the user
		
	def save_audio(self, audio, audiofile):
		self.engine.save_to_file(audio, audiofile)
		self.engine.runAndWait()
		
		
if __name__ == "__main__":
	fred = Voice()
	fred.save_audio('I\'m not meant to be airborne...', './audio/1.mp3')
