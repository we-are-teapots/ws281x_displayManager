# A display server to drive ws281x led strips on an ambeded ARM computer

It acepts a stream of unsigned ints

Author: Bruno Laurencich (https://github.com/daylanKifky)

Based on the Python wrapper for the rpi_ws281x library.
Author: Tony DiCola (tony@tonydicola.com)

Based on rpi_ws281x library by Jeremy Garff
Copyright (c) 2014 Jeremy Garff <jer @ jers.net>

## Installation:

Make sure you have `scons` and `swig` installed, or (on a debian based system)

```
sudo apt install scons swig python-dev
```


Then, you need to get the base library from [https://github.com/jgarff/rpi_ws281x](https://github.com/jgarff/rpi_ws281x), and build it inside `/lib`

```bash
cd lib
git clone https://github.com/jgarff/rpi_ws281x
cd rpi_ws281x
```
- Make sure to adjust the parameters in main.c to suit your hardare.
  - Signal rate (400kHz to 800kHz).  Default 800kHz.
  - ledstring.invert=1 if using a inverting level shifter.
  - Width and height of LED matrix (height=1 for LED string).

Build it
```bash
scons

```

Now, you have to build the python wrapper

```bash
cd python
python ./setup.py build

```

If you are rebuilding after fetching some updated commits, you might need to remove the build directory first

```
rm -rf ./build
```


## Usage:
_instructions to test it on a Raspberry Pi 3_

- Power your led strip and connect the data pin to your GPIO pin 18. If you wish you can configure the GPIO pin and other parameters inside `ws_2811_conf.py`.

- Run the display server with administrator privileges:

```bash
sudo python display_server.py
``` 

- Send a test message to the display server:

```bash
sudo python socket_send_test.py

```
(you should see a blue gradient on the leds)


- Now you can send messages the UNIX socket: `/tmp/display-server-socket`, with the format: `'<IIIIIIIIIIIIIIII'` where each of the integers correspond to the 32bits rgb value of each led on a 16 leds strip. 

The server can also be initialized to manage a different amount of leds:

```bash
sudo python display_server.py -b [NUMBER_OF_LEDS]
```

or to use a different Socket file:

```bash
sudo python display_server.py -s [PATH_TO_SOCKET]
```