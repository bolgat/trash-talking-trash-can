
from datetime import datetime
import csv
import pickle
import time

# Data storage format
class TrashData:

	def __init__(self, trash_level, trash_count):
		self.time = datetime.now()
		self.trash_level = trash_level
		self.trash_count = trash_count

# Trash-Talking Trash Can Class
class TTTcan:
	def __init__(self):
		self.state = "IDLE"
		self.trash_level = 0
		self.trash_count = 0
		# self.not_moving_threshold = 2/LOOP_LEN # amt of time TTTcan is stationary b4 it considers itself resting
		try:
			with open("datafile.txt", "rb") as datafile:
				self.trash_data = pickle.load(datafile)
		except:
			self.trash_data = []

	'''
	STATES

	IDLE #default state
	OPEN
	MOVING #if we are emptying the trash it is important to know if we are moving
	'''
	def state_transition(self):
		if(self.state == "IDLE"):
			if(self.detect_motion()):
				self.state = "MOVING"
				self.say_voice_line()
			elif(self.detect_light()):
				self.state = "OPEN"
				self.say_voice_line()
			else:
				self.state = "IDLE"

		if(self.state == "OPEN"):

			if(self.detect_motion):
				self.state = "MOVING"
				self.say_voice_line()
			elif(self.detect_darkness):
				self.state = "IDLE"
			else:
				self.state = "OPEN"

			if(self.detect_object):
				self.trash_count += 1
				self.say_voice_line()
				self.log_data()

		if(self.state == "MOVING"):

			if(self.not_moving_time == 0):
				self.state = "IDLE"
				self.not_moving_time = 20
				self.log_data()
			elif(not_moving):
				self.not_moving_time -= 1
			else:
				self.state = "MOVING"
				self.not_moving_time = 20

	def log_data(self):
		trash_level = self.get_trash_level()
		trash_data.append(TrashData(
			self.trash_level, 
			self.trash_count
		))
		with open("datafile.txt", "wb") as datafile:
			pickle.dumps(self.data, data_file)


# GLOBAL VARIABLES

LOOP_LEN = 0.1 # seconds
NOT_MOVING_THRESH = 2.0 # seconds


if __name__ == "__main__":

	Fred = TTTcan()

	while True:
		time.sleep(0.1) # Wait for 1 second between state transition
		Fred.state_transition()
