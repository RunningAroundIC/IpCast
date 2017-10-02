import time
import socket
import fcntl
import struct
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

UDP_IP = "255.255.255.255"
UDP_PORT = 5005

def getIpAddress(network):
	return socket.inet_ntoa(fcntl.ioctl(
		s.fileno(),
		0x8915,  # SIOCGIFADDR
		struct.pack('256s', network[:15])
	)[20:24])

hostname = socket.gethostname()
ip = (getIpAddress('wlan0'.encode('utf-8')))

MESSAGE = "Pi Name: " + hostname + ", IP: " + ip

count = 30
msg = 1

print("")
print("*******************************************************")
print("* Welcome to your local Raspberry Pi weather station! *")
print("* This RPi sends a message for 1 min when booting.    *")
print("* The message is as follows:                          *")
print("*",MESSAGE,"                  *")
print("*******************************************************")
print("")
print("Broadcasting Raspberry Pi info:")
while count > 0:
	s.sendto(bytes(MESSAGE,'utf-8'),(UDP_IP, UDP_PORT))
	print("Message " + str(msg) + " Send")
	time.sleep(2)
	count -= 1
	msg += 1

s.close

print("Broadcaster closed")

sys.exit()
