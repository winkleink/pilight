# using pilight web service to change colours of RGB LEDs
# Using example from rpi_ws281x library as basis for LED lighting bit

# this code is a mess
# it needs to be cleaned up
# some error trapping needs to be added
# some long winded code needs to factored.


import time

import _rpi_ws281x as ws

import urllib2


LED_COUNT      = 24         # How many LEDs to light.

#
# Start: Do not edit anything in this section as it works from the example
#

# LED configuration.
LED_CHANNEL    = 0
LED_FREQ_HZ    = 800000     # Frequency of the LED signal.  Should be 800khz or 400khz.
LED_DMA_NUM    = 5          # DMA channel to use, can be 0-14.
LED_GPIO       = 18         # GPIO connected to the LED signal line.  Must support PWM!
LED_BRIGHTNESS = 255        # Set to 0 for darkest and 255 for brightest
LED_INVERT     = 0          # Set to 1 to invert the LED signal, good if using NPN
							# transistor as a 3.3V->5V level converter.  Keep at 0
							# for a normal/non-inverted signal.

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

ws.ws2811_t_freq_set(leds, LED_FREQ_HZ)
ws.ws2811_t_dmanum_set(leds, LED_DMA_NUM)

# Initialize library with LED configuration.
resp = ws.ws2811_init(leds)
if resp != 0:
	raise RuntimeError('ws2811_init failed with code {0}'.format(resp))

#
# End: Do not edit anything in this section as it works from the example
#

# Wrap following code in a try/finally to ensure cleanup functions are called
# after library is initialized.


lastcolor = "" # last color value received successfully
red = 0 # default for red
green = 0 # default for green 
blue = 0 # default for blue
offset = 0 # In this example code goes along 3 each time and this set starting position
colorname = "blank"
 
# Change this to the hash tag for your specific project.
colorhash = "pilight"

# url to call for the pilight code
url = 'http://www.webbhickey.com/pilights/searchhash.php?colhash='+colorhash
print url

try:
	
#	while True:
	for loop in range(30):
		
		# get the pilight details
		response = urllib2.urlopen(url)

		html = response.read()
		print html
		
		# find ColorName value
		colornamestart = html.find("ColourName is ") + 14
		colornameend = html.find("<br>", colornamestart)
		if colornameend != colornamestart:
			colorname = html[colornamestart:colornameend]
		else:
			colorname = "blank"
		print colorname

		if colorname != "blank":
				
			# find RED value
			redstart = html.find("Red is ") + 7
			redend = html.find("<br>", redstart)
			if redend != redstart:
				red = int(html[redstart:redend])
				# print redstart
				# print redend
			print red
	
			# find GREEN value
			greenstart = html.find("Green is ") + 9
			greenend = html.find("<br>", greenstart)
			if greenend != greenstart:
				green = int(html[greenstart:greenend])
			# print greenstart
			# print greenend
			print green
			
			# find BLUE value
			bluestart = html.find("Blue is ") + 8
			blueend = html.find("<br>", bluestart)
			if blueend != bluestart:
				blue = int(html[bluestart:blueend])
				
			# print bluestart
			# print blueend
			print blue
	
			hexcolor = (red * 65536) + (green * 256) + blue
			# hexcolor = hex(hexcolor)
			print hexcolor
			if hexcolor != lastcolor:
				lastcolor = hexcolor
				offset +=1
				if offset == 3:
					offset =0
					
				# Update each LED color in the buffer.
				for i in range(offset,LED_COUNT,3):
					# set color variable
					color = hexcolor
		
					# Set the LED color buffer value.
					ws.ws2811_led_set(channel, i, color)
					# Send the LED color data to the hardware.
					resp = ws.ws2811_render(leds)
					if resp != 0:
						raise RuntimeError('ws2811_render failed with code {0}'.format(resp))
		else:
			for i in range(LED_COUNT):
				ws.ws2811_led_set(channel, i, 0x000000)
				resp = ws.ws2811_render(leds)
				if resp != 0:
					raise RuntimeError('ws2811_render failed with code {0}'.format(resp))

			
			# create a delay but with a counter so you can see it move.
		for waiting in range(15):
			time.sleep(1)
			print str(loop)+"."+str(waiting)+"."+str(offset)
			



	for i in range(LED_COUNT):
		ws.ws2811_led_set(channel, i, 0x000000)
		resp = ws.ws2811_render(leds)
		if resp != 0:
			raise RuntimeError('ws2811_render failed with code {0}'.format(resp))



finally:
	# Ensure ws2811_fini is called before the program quits.
	ws.ws2811_fini(leds)
	# Example of calling delete function to clean up structure memory.  Isn't
	# strictly necessary at the end of the program execution here, but is good practice.
	ws.delete_ws2811_t(leds)








