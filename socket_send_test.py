import time
import socket
import argparse
from struct import pack
from sys import exit as die

def auto_int(x):
    return int(x, 0)

parser = argparse.ArgumentParser(description='Send an UDP message.')

parser.add_argument('--socket', '-s', nargs='?', default='/tmp/python-socket') 
# parser.add_argument('--address', '-a', nargs='?', default='127.0.0.1')
# parser.add_argument('--port', '-p', nargs='?', default=5005, type=int)
t = time.time()
parser.add_argument('message', nargs='*', default=[a*256/16 for a in range(16)], type=auto_int)
args = parser.parse_args()

while len(args.message) != 16:
	args.message.append(0)


MESSAGE = args.message
streamFormat = b"<" + b"I"*16

print "Sending to socket:", args.socket
print "Values: {}".format(args.message)
 
sock = socket.socket(socket.AF_UNIX,
                     socket.SOCK_DGRAM)
sock.connect(args.socket)


sock.send(pack(streamFormat, *args.message))

