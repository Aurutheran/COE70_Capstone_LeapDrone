"""
Ajithan Urutheran
Ruthvik Penumatcha
Navjot Sandhu
PyParrot Drone Code
November 9th, 2021
"""

from Minidrone import Mambo
from helperdelim import spliter
import time
import socket 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1234))
s.listen(5)

class setget:
	def __init__(self,success=False):
		self.success=success
	def get_success(self):
		return self._success   
	def set_success(self,x):
		self._success=x

mamboAddr = "e0:14:1e:bd:3d:fe"
mambo = Mambo(mamboAddr, use_wifi=True)
privatesuccess = setget()
privatesuccess.set_success(False)



def resultchecker(input):
	if(input == ("Takeoff")):
		print("Drone is taking off!")
		
		mambo.ask_for_state_update()
		
		#mambo.set_max_vertical_speed(5)   #max speed forward 50cm/s
		#mambo.set_max_tilt(5)             #max speed sideways 50cm/s
		mambo.safe_takeoff(5)
		 
	elif(input==("land")):
		mambo.safe_land(5)
		mambo.smart_sleep(5)
		print("Landing the drone")
		privatesuccess.set_success(False)
		print("First" + str(privatesuccess.get_success()))
		print("Second"+ str(privatesuccess.get_success()))
		exit()

	elif(input[0]==('2')):
		#mambo.fly_direct(int(input[1]),int(input[2]),int(input[3]),int(input[4]),0) #chnage this
		
		
		
		if (int(input[2]) > -10 and int(input[2]) <10):    #PITCH IS 0
			if(int(input[1]) > -10 and int(input[1]) < 10):   # IF THE ROLL IS ALSO zero, NO MOVEMENT
				mambo.fly_direct(0,0,0,0,0.5)
				print("Drone Stationary")
			elif(int(input[1]) > 10):   #IF ROLL IS POSITIVE AND PITCH IS 0, MOVE RIGHT
				mambo.fly_direct(20,-8,0,0,0.5)
				print("Drone Move East")
			elif(int(input[1]) < -10):  #IF ROLL IS NEGATIVE AND PITCH IS 0, MOVE LEFT
				mambo.fly_direct(-20,-8,0,0,0.5)
				print("Drone Move West")
		
		elif(int(input[2]) > 10):  #PITCH IS POSITIVE
			if(int(input[1]) > -10 and int(input[1]) < 10):  #PITCH POSITIVE AND ROLL IS ZERO, MOVE UP
				mambo.fly_direct(0,5,0,0,0.5)
				print("Drone Move North")
			elif(int(input[1]) > 10):   #PITCH POSITIVE AND ROLL IS POSTIVE, MOVE NORTH EAST
				mambo.fly_direct(20,5,0,0,0.5)
				print("Drone Move North East")
			elif(int(input[1]) < -10):  #PITCH POSIIVE AND ROLL IS NEGATIVE, MOVE NORTH WEST
				mambo.fly_direct(-20,5,0,0,0.5)
				print("Drone Move North West")
		
		elif(int(input[2])< -10):  #PITCH IS NEGATIVE
			if(int(input[1]) > -10 and int(input[1]) < 10): #PITCH NEGATIVE AND ROLL IS ZERO, MOVE BACK
				mambo.fly_direct(0,-40,0,0,0.5)    
				print("Drone Move South")
			elif(int(input[1]) > 10): #PITCH NEGATIVE AND ROLL IS POSITIVE, MOVE SOUTH EAST
				mambo.fly_direct(20,-40,0,0,0.5)
				print("Drone Move South East")
			elif(int(input[1]) < -10): #PITCH NEGATIVE AND ROLL IS NEGATIVE, MOVE SOUTH WEST
				mambo.fly_direct(-20,-40,0,0,0.5)
				print("Drone Move South West")

		#if(int(input[1]) > 10):   #for moving left or right  (ROLL)
		#	input[1] = '5'
		#if(int(input[1])< -10):
		#	input[1] = '-5'
		#print("Roll: "+(input[1]))
		#print("Pitch: "+(input[2]))
		#print("Yaw:"+(input[3]))
		#print("VMov:"+(input[4]))

		#mambo.fly_direct(int(input[0]),...)
		#mambo.fly_direct(0,int(input[2]),0,0,0.5)
	elif(input[0]==('4')):
		#mambo.fly_direct(int(input[1]),int(input[2]),int(input[3]),int(input[4]),0) #chnage this
		mambo.fly_direct(0,0,0,0,0)


		
	
def inputPasser(input):
	result = spliter(input)
	resultchecker(result)


print("Trying to connect")
if(mambo.connect(num_retries=3)):
	privatesuccess.set_success(True)

	
#remember to make it a while loop and set success to false if landing sequence

	

print("connected:"+str(privatesuccess.get_success()))

while(privatesuccess.get_success()):
	con, add = s.accept()
	print(f"connection is established via {add}")
	while True:
		data = con.recv(30)
		if not data:
			break
		full_msg = data.decode()
		print(""+full_msg+"\n")
		inputPasser(full_msg)
	
		
full_msg = ""
con.shutdown(1)
print("disconnect")
mambo.disconnect()

#spliter first than result checker