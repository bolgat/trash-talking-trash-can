from grovepi import *
import smbus            #import SMBus module of I2C
from time import sleep  #import

DEBUG = 0

#some MPU6050 Registers and their Address
bus = smbus.SMBus(1)     # or bus = smbus.SMBus(0) for older version boards
DEVICE_ADDRESS = 0x68
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F

class accel:
    def __init__(self):
        #write to sample rate register
        bus.write_byte_data(DEVICE_ADDRESS, SMPLRT_DIV, 7)
    
        #Write to power management register
        bus.write_byte_data(DEVICE_ADDRESS, PWR_MGMT_1, 1)
    
        #Write to Configuration register
        bus.write_byte_data(DEVICE_ADDRESS, CONFIG, 0)
    
        #Write to Gyro configuration register
        bus.write_byte_data(DEVICE_ADDRESS, GYRO_CONFIG, 24)
    
        #Write to interrupt enable register
        bus.write_byte_data(DEVICE_ADDRESS, INT_ENABLE, 1)

    def read_bytes(self,addr):
        #Accelero and Gyro value are 16-bit
        high = bus.read_byte_data(DEVICE_ADDRESS, addr)
        low = bus.read_byte_data(DEVICE_ADDRESS, addr+1)
    
        #concatenate higher and lower value
        value = ((high << 8) | low)
        
        #to get signed value from mpu6050
        if(value > 32768):
                value = value - 65536
        return value

    def read_accel(self):
        return [
            self.read_bytes(ACCEL_XOUT_H)/16384.0,
            self.read_bytes(ACCEL_YOUT_H)/16384.0,
            self.read_bytes(ACCEL_ZOUT_H)/16384.0
        ]