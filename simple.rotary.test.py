from RPi import GPIO
from time import sleep

clk = 17
dt = 18
sw = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(sw, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

counter = 1
lastCounter = counter
clkLastState = GPIO.input(clk)


def buttonCallback(channel):
    print('button' + str(GPIO.input(channel)))


GPIO.add_event_detect(sw, GPIO.BOTH, callback=buttonCallback, bouncetime=100)

try:
    while True:
            clkState = GPIO.input(clk)
            dtState = GPIO.input(dt)
            if clkState != clkLastState:
                if dtState != clkState:
                    counter += .5
                else:
                    counter -= .5
                if counter % 1 == 0 and lastCounter != counter:
                    lastCounter = counter
                    print(counter)

            clkLastState = clkState
            sleep(0.001)
finally:
    GPIO.cleanup()