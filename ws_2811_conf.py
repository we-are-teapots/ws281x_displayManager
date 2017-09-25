import sys
sys.path.append("lib/rpi_ws281x/python/build/lib.linux-armv7l-2.7")

import _rpi_ws281x as ws

from argparse import ArgumentParser
# 
# 
parser = ArgumentParser(description='WS281x Led-strip display manager.')
parser.add_argument('--buffer', '-b', nargs='?', default=16, help= "The receive buffer size (in bytes)", type=int)
parser.add_argument('--socket', '-s', nargs='?', default="/tmp/python-socket", help= "The path to the socket")
parser.add_argument('--dump', '-d', nargs='?', default=False, help= "Just print the incoming message on stdout ")
args = parser.parse_args() 



# LED configuration.
LED_CHANNEL    = 0

LED_COUNT      = args.buffer
# if len(sys.argv) > 1:
# 	LED_COUNT      = int(sys.argv[1])         # How many LEDs to light.

LED_FREQ_HZ    = 800000     # Frequency of the LED signal.  Should be 800khz or 400khz.
LED_DMA_NUM    = 5          # DMA channel to use, can be 0-14.

LED_GPIO       = 18         # GPIO connected to the LED signal line.  Must support PWM!

# if len(sys.argv) > 3:
	# LED_GPIO       =  int(sys.argv[3]) 

LED_BRIGHTNESS = 200        # Set to 0 for darkest and 255 for brightest
LED_INVERT     = 0          # Set to 1 to invert the LED signal, good if using NPN
							# transistor as a 3.3V->5V level converter.  Keep at 0
							# for a normal/non-inverted signal.

# Define colors which will be used by the example.  Each color is an unsigned
# 32-bit value where the lower 24 bits define the red, green, blue data (each
# being 8 bits long).
DOT_COLORS = [  0x200000,   # red
				0x201000,   # orange
				0x202000,   # yellow
				0x002000,   # green
				0x002020,   # lightblue
				0x000020,   # blue
				0x100010,   # purple
				0x200010 ]  # pink

# Create a ws2811_t structure from the LED configuration.
# Note that this structure will be created on the heap so you need to be careful
# that you delete its memory by calling delete_ws2811_t when it's not needed.
leds = ws.new_ws2811_t()

# Initialize all channels to off
for channum in range(2):
    channel = ws.ws2811_channel_get(leds, channum)
    ws.ws2811_channel_t_count_set(channel, 0)
    ws.ws2811_channel_t_gpionum_set(channel, 0)
    ws.ws2811_channel_t_invert_set(channel, 0)
    ws.ws2811_channel_t_brightness_set(channel, 0)

channel = ws.ws2811_channel_get(leds, LED_CHANNEL)

ws.ws2811_channel_t_count_set(channel, LED_COUNT)
ws.ws2811_channel_t_gpionum_set(channel, LED_GPIO)
ws.ws2811_channel_t_invert_set(channel, LED_INVERT)
ws.ws2811_channel_t_brightness_set(channel, LED_BRIGHTNESS)
ws.ws2811_channel_t_strip_type_set(channel, ws.WS2811_STRIP_GRB)
ws.ws2811_t_freq_set(leds, LED_FREQ_HZ)
ws.ws2811_t_dmanum_set(leds, LED_DMA_NUM)

# Initialize library with LED configuration.
resp = ws.ws2811_init(leds)
if resp != ws.WS2811_SUCCESS:
	message = ws.ws2811_get_return_t_str(resp)
	raise RuntimeError('ws2811_init failed with code {0} ({1})'.format(resp, message))

