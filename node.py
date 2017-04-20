import socket
import time
import picamera
import io
import threading

whoami = socket.gethostname()
snapping = 0
shootstatus = 0
timer = 0
seq = 0
host = '192.168.0.110'


nodes = {'pan01':{'Hostname': 'pan01', 'IP': "192.168.0.101", 'Status': 'Unknown', 'Host': "10.0.11.1"},
	'pan02':{'Hostname': 'pan02', 'IP': "192.168.0.102", 'Status': 'Unknown', 'Host': "10.0.12.1"},
	'pan03':{'Hostname': 'pan03', 'IP': "192.168.0.103", 'Status': 'Unknown', 'Host': "10.0.13.1"},
	'pan04':{'Hostname': 'pan04', 'IP': "192.168.0.104", 'Status': 'Unknown', 'Host': "10.0.14.1"},
	'pan05':{'Hostname': 'pan05', 'IP': "192.168.0.105", 'Status': 'Unknown', 'Host': "10.0.15.1"},
	'pan06':{'Hostname': 'pan06', 'IP': "192.168.0.106", 'Status': 'Unknown', 'Host': "10.0.16.1"},
	'pan07':{'Hostname': 'pan07', 'IP': "192.168.0.107", 'Status': 'Unknown', 'Host': "10.0.17.1"},
	'pan08':{'Hostname': 'pan08', 'IP': "192.168.0.108", 'Status': 'Unknown', 'Host': "10.0.18.1"}}


# create the UDP socket
UDPSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#UDPSock.settimeout(5)
listen_addr = ("",21567)
UDPSock.bind(listen_addr)

class MyOutput(object):
	def __init__(self):
		self.file_num = 0
		self.write_frame = False
		self.output = None
		self.whoami = socket.gethostname()

	def write(self, buf):
		if buf.startswith(b'\xff\xd8'):
			if self.output:
				self.output.close()
			self.output = None
			if self.write_frame:
				self.file_num += 1
				self.output = io.open('%s_%d.jpg' % (self.whoami, self.file_num), 'wb')
				message = 'Frame %d' % self.file_num
				print(message)
				replytohost(message)
				self.write_frame = False
		if self.output:
			self.output.write(buf)

def start():
	with picamera.PiCamera(resolution=(1280, 720), framerate=15) as camera:
		output = MyOutput()
		camera.start_recording(output, format='mjpeg')
		replytohost("ready")
		try:
			while True:
				global shootstatus
				global timer
				if timer == 3:
					if shootstatus == 2:
						break
					elif shootstatus == 1:
						output.write_frame = True
						time.sleep(3)
					camera.wait_recording(0.1)
				elif  timer == 0:
					if shootstatus == 2:
						break
					elif shootstatus == 1:
						output.write_frame = True
						shootstatus = 0
						camera.wait_recording(0.1)
		finally:
				camera.stop_recording()
				print("Stopped Camera")
				shootstatus = 0
				timer = 0

def replytohost(data):
	global host
	addr = (host,21567)
	UDPSock.sendto(data,addr)

while True:
	try:
		data,addr = UDPSock.recvfrom(1024)
		print(data)
		source = addr[0]
		if data == "check":
			addr = (source,21567)
			data = "here"
			UDPSock.sendto(data,addr)
		elif data == "setup":
			s = threading.Thread(target=start)
			s.start()
		elif data == "stop":
			shootstatus = 2
		elif data == "3s":
			if shootstatus == 0:
				shootstatus = 1
				timer = 3
			elif shootstatus == 1:
				print "snap is snapping already"
		elif data == "snap":
			if shootstatus == 0:
				shootstatus = 1
				#seq = seq + 1
				#snap(camera, seq)
                #snap = threading.Thread(target=shoot)
                #snap.start()
			elif shootstatus == 1:
				print "snap is snapping already"
	except socket.timeout:
		data = 1
