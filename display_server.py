# A display server to drive ws281x led strips
# 
# It acepts a stream of unsigned ints on a socket, and light the ledstrip with the corresponding values
# 
# Author: Bruno Laurencich (https://github.com/daylanKifky)
# 
# Based on the Python wrapper for the rpi_ws281x library.
# Author: Tony DiCola (tony@tonydicola.com)
# 
# Based on rpi_ws281x library by Jeremy Garff
#  * Copyright (c) 2014 Jeremy Garff <jer @ jers.net>
# *
# * All rights reserved.
# *
# * Redistribution and use in source and binary forms, with or without modification, are permitted
# * provided that the following conditions are met:
# *
# *     1.  Redistributions of source code must retain the above copyright notice, this list of
# *         conditions and the following disclaimer.
# *     2.  Redistributions in binary form must reproduce the above copyright notice, this list
# *         of conditions and the following disclaimer in the documentation and/or other materials
# *         provided with the distribution.
# *     3.  Neither the name of the owner nor the names of its contributors may be used to endorse
# *         or promote products derived from this software without specific prior written permission.
# *
# * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR
# * IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
# * FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER BE
# * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# * (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# * OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
# * OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
from sys import path as pypath
pypath.append("lib")
from usleep import delay as uwait

from struct import unpack
import socket
import time
import os

# ws2811 setup
from ws_2811_conf import *

#The format string to unpack the stream
#A little endian  with as many unsigned bytes as the passed buffer size
#see: https://docs.python.org/2/library/struct.html#byte-order-size-and-alignment
#and: https://docs.python.org/2/library/struct.html#format-characters
streamFormat = b"<" + b"I"*args.buffer
#convert buffer size to bits  
bufSize = args.buffer * 8 

path = args.socket

if os.path.exists(path):
    os.remove(path)

sock = socket.socket(socket.AF_UNIX, 
                     socket.SOCK_DGRAM) 

sock.bind(path)

print "POV DISPLAY SERVER\nListening in SOCKET {}".format(path)

print "Stream format: {}".format(streamFormat)

try:
	if args.dump:
		while True:
			stream= sock.recv(bufSize) 
			t = time.time()
			data = unpack(streamFormat, stream)[0]
			print "[{} | us: {:.0f}] --> {}".format(time.ctime(t), (t-int(t))*1000000, data )

	else:
		while True:
			stream= sock.recv(bufSize) 
			uwait(0.001)
			data = unpack(streamFormat, stream)
			for i in range(LED_COUNT):
				# Set the LED color buffer value.
				ws.ws2811_led_set(channel, i, data[i])

			resp = ws.ws2811_render(leds)
			if resp != ws.WS2811_SUCCESS:
				message = ws.ws2811_get_return_t_str(resp)
				raise RuntimeError('ws2811_render failed with code {0} ({1})'.format(resp, message))
	
except KeyboardInterrupt:
	ws.ws2811_fini(leds)
	ws.delete_ws2811_t(leds)

except Exception as e:
	print ">"*20+" DISPLAY SERVER ERROR:"
	print e.__doc__
	print e.message
	print ">"*20

finally:
	ws.ws2811_fini(leds)
	ws.delete_ws2811_t(leds)


