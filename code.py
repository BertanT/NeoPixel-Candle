# NeoPixel Candle - Realistic candle effect with NeoPixel LEDs!
# Created by Bertan on 30.10.2021
# Copyright (c) 2021 Mehmet Bertan Tarakçıoğlu, licsensed under the MIT Licsense

import time
import alarm
import random
import board
import neopixel

# Adjust the preferences to your liking!
power_timeout_hours = 8     # The candle will sleep after the given value of hours and turn back on at the initial power-up time the next day
max_brightness = 1          # Brightness of your candle, set float value between 0-1
candle_color = (255, 70, 0) # 8 Bit RGB color of your candle
pixel_count = 1             # The number of neopixels that your candle has
pixel_pin = board.GP16      # The pin your NeoPixel(s) is connected to

# Initialize the NeoPixel(s)
pixels = neopixel.NeoPixel(pixel_pin, pixel_count, brightness=max_brightness, pixel_order=neopixel.RGB)

# Smooth brigthness adjustment makes it look more natural!
def smooth_brightness(brightness):
    # Set the step value of the for loop 1 if the new brightness value is greater than the current brightness, -1 if less
    if brightness > pixels.brightness:
        step = 1
    else:
        step = -1

    # The for loop give the smoothness by dividing the change in brightness to 100 points and adding a slight delay between each incrementation
    for i in range(int(pixels.brightness * 100), int(brightness * 100) - 1, step):
        pixels.brightness =  i / 100
        time.sleep(0.001)

# Turn the pixels on for the first time!        
pixels.fill(candle_color)
# Log the start time to keep track of uptime
start_time = time.monotonic()

while True:
    # Calculate the uptime and convert it to hours
    time_passed_hours = (time.monotonic() - start_time) / 3600

    # Go to deep sleep if the uptime is greater or equal to the power timeout specified above
    if time_passed_hours >= power_timeout_hours:
        smooth_brightness(0)
        # Set up the time alarm to wake the next day at the time of initail power-up
        sleep_period = (24 - power_timeout_hours) * 3600
        wake_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + sleep_period)
        alarm.exit_and_deep_sleep_until_alarms(wake_alarm)

    # Set the brighness of the NeoPixel(s) to a random number between 0.2-1 with a random delay between 50-800ms
    rand_brightness = random.uniform(0.2, max_brightness)
    flicker_delay = random.uniform(0.05, 0.8)
    smooth_brightness(rand_brightness)
    time.sleep(flicker_delay)
    smooth_brightness(max_brightness)
    time.sleep(flicker_delay)
