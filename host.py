import curses
import socket
import threading
from time import sleep

timer = 0

nodes = {'pan01':{'Hostname': 'pan01', 'IP': "192.168.0.101", 'Status': 'unkown'},
	'pan02':{'Hostname': 'pan02', 'IP': "192.168.0.102", 'Status': 'unkown'},
	'pan03':{'Hostname': 'pan03', 'IP': "192.168.0.103", 'Status': 'unkown'},
	'pan04':{'Hostname': 'pan04', 'IP': "192.168.0.104", 'Status': 'unkown'},
	'pan05':{'Hostname': 'pan05', 'IP': "192.168.0.105", 'Status': 'unkown'},
	'pan06':{'Hostname': 'pan06', 'IP': "192.168.0.106", 'Status': 'unkown'},
	'pan07':{'Hostname': 'pan07', 'IP': "192.168.0.107", 'Status': 'unkown'},
	'pan08':{'Hostname': 'pan08', 'IP': "192.168.0.108", 'Status': 'unkown'}}

# create the UDP socket
UDPSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#UDPSock.settimeout(5)
listen_addr = ("",21567)
UDPSock.bind(listen_addr)
isshooting = 0

class StoppableThread(threading.Thread):

	def __init__(self):
		super(StoppableThread, self).__init__()
		self._stop = threading.Event()

	def stop(self):
		self._stop.set()

	def stopped(self):
		return self._stop.isSet()

def parsedata(data, server):
	if data == 'here':
		changestatus(data, server)
	if 'Frame' in data:
		changestatus(data, server)
	if data == 'ready':
		changestatus(data, server)

def updateframe(data, server):
	nodename = parsenodename(server)
	nodes[nodename]['Status'] = data;

def changestatus(data, server):
	nodename = parsenodename(server)
	nodes[nodename]['Status'] = data;

def showstatus():
	for i in nodes:
		 nodename = nodes[i]['Hostname']
		 status = nodes[i]['Status']
		 message = 'Node: %s is %s' % (nodename, status)
		 print(message)

def parsenodename(addr):
	for i in nodes:
		if nodes[i]['IP'] == addr[0]:
			return(nodes[i]['Hostname'])

def listen():
	while True:
		data,addr = UDPSock.recvfrom(1024)
		parsedat = threading.Thread(target=parsedata, args=(data, addr))
		parsedat.start()
		if exitgiven == 'stop':
			print('Stopped Listening')
			break
	return

def sendcmd(cmd):
	for i in nodes:
		addr = (nodes[i]['IP'],21567)
		UDPSock.sendto(cmd,addr)

def lapse():
	global timer
	while timer == 1:
		cmd = 'snap'
		sendcmd(cmd)
		sleep(3)
	timer = 0
	return

def main(window):
	window.nodelay(True)
	global timer
	try:
		temp = 0
		while True:
			num = 0
			temp = temp + 1
			for i in nodes:
				num = num + 1
				nodename = nodes[i]['Hostname']
	   		 	status = nodes[i]['Status']
	   		 	message = 'Node: %s is %s              ' % (nodename, status)
				window.addstr(int(num), 5, message)
			window.addstr(9, 0, 'Press Q to Quit')
			window.addstr(10, 0, 'Press C to check camera status')
			window.addstr(11, 0, 'Press S to start camera on nodes')
			window.addstr(12, 0, 'Press F to snap a frame')
			window.addstr(13, 0, 'Press 3 to start a 3sec Time-lapse')
			window.addstr(14, 0, 'Press P to stop all recording')

			window.refresh()
			c = window.getch()
			if c == ord('q'):
				break
			elif c == ord('c'):
				cmd = 'check'
				for i in nodes:
					nodes[i]['Status'] = 'check';
					addr = (nodes[i]['IP'],21567)
					UDPSock.sendto(cmd,addr)
				window.refresh()
			elif c == ord('s'):
				cmd = 'setup'
				sendcmd(cmd)
			elif c == ord('f'):
				cmd = 'snap'
				sendcmd(cmd)
			elif c == ord('3'):
				if timer == 0:
					timer = 1
					#need to look up how to remove a line
					window.addstr(15, 0, '                         ')
				elif timer == 1:
					window.addstr(15, 0, 'Timelapse already running')
				cmd = '3s'
			elif c == ord('p'):
				timer = 0
				lapse.join()
				cmd = 'stop'
				sendcmd(cmd)
	finally:
		print("Stopped")

listen = threading.Thread(target=listen)
listen.start()

lapse = threading.Thread(target=lapse)
lapse.start()

curses.initscr()
curses.wrapper(main)
