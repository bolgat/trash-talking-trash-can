
from datetime import datetime
import math
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
        self.motion_detect_count = 0
        self.trash_data = []

        self.xl = accel_driver.accel()
        self.baseline_accel = self.xl.read_accel()

        try:
            with open("datafile.csv", "r") as datafile:
                datareader = csv.reader(datafile)
                for row in datareader:
                    self.trash_data.append(row)
                self.trash_count = int(datareader[-1][-1])
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

            if(self.detect_motion()):
                self.state = "MOVING"
                self.say_voice_line()
            else:
                self.state = "IDLE"
            if(self.detect_object()):
                self.trash_count += 1
                self.say_voice_line()
                self.log_data()
                self.state = "OBJ_DETECTED"
        
        
        if(self.state == "MOVING"):

            if(self.motion_detect_count == NOT_MOVING_THRESH):
                self.state = "IDLE"
                self.motion_detect_count = 0
            elif(not self.detect_motion()):
                self.motion_detect_count += 1
            else:
                self.state = "MOVING"
                self.motion_detect_count = 0
    
        if(self.state =="OBJ_DETECTED"):
            if(self.detect_motion()):
                self.state = "MOVING"
                self.say_voice_line()
            elif(self.obj_detect_count == OBJ_DETECT_THRESH):
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
            datetime.now(),
            self.trash_level / self.baseline_trash, 
            self.trash_count
        ])
            
        with open("datafile.csv", "w") as datafile:
            datawriter = csv.writer(datafile)
            datawriter.writerows(self.trash_data)

    def detect_object(self):
        ultrasonic_ranger = 4
        try:
            # Read distance value from Ultrasonic
            distance = grovepi.ultrasonicRead(ultrasonic_ranger)

        except Exception as e:
            print ("Error:{}".format(e))
        
        if (distance < 20):
            return True
        else:
            return False

    def detect_motion(self):
        accel = self.xl.read_accel()
        diff = [ accel[0]-self.baseline_accel[0] , accel[1]-self.baseline_accel[1] , accel[2]-self.baseline_accel[2] ]
        mag_diff = math.sqrt(diff[0]*diff[0] + diff[1]*diff[1] + diff[2]*diff[2])

        if (mag_diff > 0.5):
            return True
        else:
            return False

    def get_trash_level(self):
        ultrasonic_ranger = 8
        try:
            # Read distance value from Ultrasonic
            distance = grovepi.ultrasonicRead(ultrasonic_ranger)
            print(distance)

        except Exception as e:
            print ("Error:{}".format(e))
        
        return distance
    
    def say_voice_line(self):
        # This is temporary
        xl = accel_driver.accel()
        print(xl.read_accel())



if __name__ == "__main__":

    Fred = TTTcan()

    while True:
        time.sleep(0.1) # Wait for 1 second between state transition
        Fred.state_transition()
        





