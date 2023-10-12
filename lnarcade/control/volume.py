import board
import os
from rainbowio import colorwheel
from adafruit_seesaw import seesaw, neopixel, rotaryio, digitalio

i2c = board.I2C()
seesaw = seesaw.Seesaw(i2c, 0x36)

encoder = rotaryio.IncrementalEncoder(seesaw)
seesaw.pin_mode(24, seesaw.INPUT_PULLUP)
switch = digitalio.DigitalIO(seesaw, 24)

pixel = neopixel.NeoPixel(seesaw, 6, 1)
pixel.brightness = 0.5

last_position = -1
color = 0

# Get current volume from the system
volume_query = os.popen("amixer get 'Master' | grep -m1 -o [0-9]*% | tr -d %").read().strip()
current_volume = int(volume_query)

while True:
    position = -encoder.position

    if position != last_position:
        print(position)

        if switch.value:
            # Change the LED color.
            if position > last_position:
                color += 1
            else:
                color -= 1
            color = (color + 256) % 256
            pixel.fill(colorwheel(color))
        else:  
            # Change the system volume.
            if position > last_position:
                current_volume = min(100, current_volume + 5)  # increase by 5%
            else:
                current_volume = max(0, current_volume - 5)  # decrease by 5%
            
            # Adjust system volume using the 'amixer' command
            v = f"amixer set 'Master' -- {current_volume}%"
            print(v)
            print(os.system( v ))

    last_position = position
