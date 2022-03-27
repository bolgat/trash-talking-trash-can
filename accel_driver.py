import grovepi

#some MPU6050 Registers and their Address
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F

class accel
	def __init__(self):
		#write to various registers
		write_i2c_block(Device_Address, SMPLRT_DIV, 7)
		write_i2c_block(Device_Address, PWR_MGMT_1, 1)
		write_i2c_block(Device_Address, CONFIG, 0)
		write_i2c_block(Device_Address, GYRO_CONFIG, 24)
		write_i2c_block(Device_Address, INT_ENABLE, 1)

	def read_bytes(self,addr):
		#Accelero and Gyro value are 16-bit
	        high = bus.read_i2c_block(Device_Address, addr)
	        low = bus.read_i2c_block(Device_Address, addr+1)
	    
	        #concatenate higher and lower value
	        value = ((high << 8) | low)
	        
	        #to get signed value from mpu6050
	        if(value > 32768):
	                value = value - 65536
	        return value

	def read_accel(self):
		return [
			self.read_data(ACCEL_XOUT_H)/16384.0
			self.read_data(ACCEL_YOUT_H)/16384.0
			self.read_data(ACCEL_ZOUT_H)/16384.0
		]