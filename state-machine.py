'''
STATES

IDLE #default state
OPEN
MOVING #if we are emptying the trash it is important to know if we are moving
'''

state = "IDLE"
int trash_level = 0
int detect_count = 0

int not_moving_time = 20

if __name__ == "__main__":
	while True:
		time.sleep(0.1) # Wait for 1 second between state transition

		if(state == "IDLE"):
			if(detect_motion):
				state = "MOVING"
				say_voice_line()
			elif(detect_light):
				state = "OPEN"
				say_voice_line()
			else:
				state = "IDLE"

		if(state == "OPEN"):

			if(detect_motion):
				state = "MOVING"
				say_voice_line()
			elif(detect_darkness):
				state = "IDLE"
			else:
				state = "OPEN"

			if(detect_object):
				do_something()

		if(state == "MOVING"):

			if(not_moving_time == 0):
				state = "IDLE"
				not_moving_time = 20
			elif(not_moving):
				not_moving_time -= 1
			else:
				state = "MOVING"
				not_moving_time = 20

