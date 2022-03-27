
from datetime import datetime
import csv
import time
import grovepi
import accel_driver

# GLOBAL VARIABLES

LOOP_LEN = 0.1 # seconds
NOT_MOVING_THRESH = int(2.0/LOOP_LEN) # iterations
OBJ_DETECT_THRESH = int(1.0/LOOP_LEN) # iterations

# Trash-Talking Trash Can Class
class TTTcan:
    def __init__(self):
        self.state = "IDLE"
        self.baseline_trash = self.get_trash_level()
        self.trash_level = 0
        self.trash_count = 0
        self.obj_detect_count = 0
        self.trash_data = []

        try:
        	with open("datafile.csv", "r") as datafile:
        		datareader = csv.reader(datafile)
        		for row in datareader:
        			self.trash_data.append(row)
       	except:
       		pass
        # self.not_moving_threshold = 2/LOOP_LEN # amt of time TTTcan is stationary b4 it considers itself resting

    '''
    STATES

    IDLE #default state
    OBJ_DETECTED
    MOVING #if we are emptying the trash it is important to know if we are moving
    '''
    def state_transition(self):
        if(self.state == "IDLE"):
            '''if(self.detect_motion()):
                self.state = "MOVING"
                self.say_voice_line()
            elif(self.detect_light()):
                self.state = "OPEN"
                self.say_voice_line()
            else:
                self.state = "IDLE"
            '''

            '''if(self.detect_motion):
                self.state = "MOVING"
                self.say_voice_line()
                
            elif(self.detect_darkness):
                self.state = "IDLE"
            else:
                self.state = "OPEN"
            '''
            if(self.detect_object()):
                self.trash_count += 1
                self.say_voice_line()
                self.log_data()
                self.state = "OBJ_DETECTED"
        
        '''
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
        '''
    
        if(self.state =="OBJ_DETECTED"):
            if(self.obj_detect_count == OBJ_DETECT_THRESH):
                self.state = "IDLE"
                self.obj_detect_count = 0            
            elif(not self.detect_object()):
                self.obj_detect_count += 1
            else:
                self.state = "OBJ_DETECTED"
                self.obj_detect_count = 0


    def log_data(self):
        self.trash_level = self.get_trash_level()
        self.trash_data.append([
        	datetime.now()
        	self.trash_level / self.baseline_trash, 
            self.trash_count
        ])
            
        with open("datafile.csv", "w") as datafile:
        	datawriter = csv.writer(datafile)
        	datawriter.writerows(trash_data)

    def detect_object(self):
        ultrasonic_ranger = 7
        try:
            # Read distance value from Ultrasonic
            distance = grovepi.ultrasonicRead(ultrasonic_ranger)

        except Exception as e:
            print ("Error:{}".format(e))
        
        if (distance < 30):
            return True
        else:
            return False


    def get_trash_level(self):
        ultrasonic_ranger = 8
        try:
            # Read distance value from Ultrasonic
            distance = grovepi.ultrasonicRead(ultrasonic_ranger)

        except Exception as e:
            print ("Error:{}".format(e))
        
        return distance
    
    def say_voice_line(self):
    	xl = accel()
        print(xl.read_accel())




if __name__ == "__main__":

    Fred = TTTcan()

    while True:
        time.sleep(0.1) # Wait for 1 second between state transition
        Fred.state_transition()
        





