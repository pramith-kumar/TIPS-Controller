#**************************************************************************************************
#
#                                      TIPS Controller Ver 1.1
#
#**************************************************************************************************
import os
import socket
import sys
from gpiozero import Button, LED
import time

Device_Id = 21

SERVER_IP = "192.168.100.234"				# THIS IS YOUR SERVER IP
SERVER_PORT = 20108

CLIENT_IP = "192.168.100.250"				# DO NOT FORGET TO SET RASPBERRY PI
CLIENT_PORT = 20107
sock = socket.socket(socket.AF_INET,
socket.SOCK_DGRAM) 							# UDP Receive
sock.bind((CLIENT_IP, CLIENT_PORT))


V_Loop = Button(1)							#	GPIO1
N_Loop = Button(2)							#	GPIO2
Barrier_Arm_Broken = Button(3)				#	GPIO3
Barrier_Up = Button(4)						#	GPIO4
Barrier_Down = Button(5)

Open_Sp = LED(17)
Close = LED(18)
Barrier_On = LED(19)
Open_St = LED(20)

V_Loop_Prev_Status = 0
N_Loop_Prev_Status = 0
Barrier_Arm_Broken_Prev_Status = 0
Barrier_Up_Prev_Status = 0
Barrier_Down_Prev_Status = 0

while True:
# GPIO input check in loop
	if (( V_Loop.is_pressed ) and ( V_Loop_Prev_Status == 0 )) :
		V_Loop_Prev_Status = 1
		sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		sock.sendto(Device_Id + "101", (SERVER_IP,SERVER_PORT))

	if (( N_Loop.is_pressed ) and ( N_Loop_Prev_Status == 0 )):
		N_Loop_Prev_Status = 1

	if (( Barrier_Arm_Broken.is_pressed ) and ( Barrier_Arm_Broken_Prev_Status == 0 )):
		Barrier_Down_Prev_Status = 1

	if (( Barrier_Up.is_pressed ) and ( Barrier_Up_Prev_Status == 0 )):
		Barrier_Up_Prev_Status = 1

	if ((Barrier_Down.is_pressed) and ( Barrier_Down_Prev_Status == 0 )):
		Barrier_Down_Prev_Status = 1

# GPIO out - UDP Receive starts here
	data, addr = sock.recvfrom(1024) 
	print("received command: %s" % data)
	if ( data == "45" ):
		Open_St.on()
		time.sleep(0.1)
		Open_St.off()
	if ( data == "46" ):
		Close.on()
		time.sleep(0.1)
		Close.off()
	if ( data == "81" ):
		os.system("sudo reboot")