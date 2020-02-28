# todo: put these in readme.md
# enable i2c with and install
# follow https://learn.adafruit.com/monochrome-oled-breakouts/python-setup
# python3 -m pip install Pillow
# sudo apt-get install libopenjp2-7

print("Trying to start cattrotar...")
from RPi import GPIO
from time import sleep
from Oled import Oled
import logging, sys, os
# print("Libs loaded except catt lib...")
# import catt.api as cat_api
# print("catt lib loaded...")
logging.basicConfig(filename=os.path.dirname(os.path.abspath(__file__)) + "/error.log")


class cattrotar:

    def __init__(self):

        self.clk = 17
        self.dt = 18
        self.sw = 23
        self.volume = 99
        self.preMuteVolume = self.volume
        self.button = 0
        print('Trying to initialize screen on default i2c bus')
        try:
            self.screen = Oled(48);
            self.screen.display(';)')
            sleep(.5)
        except Exception as e:
            logging.error(logging.exception(e))
            sys.exit('ERROR Could not access screen: ' + str(e))

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.sw, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        GPIO.add_event_detect(self.sw, GPIO.FALLING, callback=self.toggleMute, bouncetime=500)

    def setVolume(self, volume, silent = False):
        if volume < 0:
            if not silent:
                self.screen.display("MIN")
                sleep(0.5)
                self.screen.display(round(self.volume))

        elif volume > 100:
            if not silent:
                self.screen.display("MAX")
                sleep(0.5)
                self.screen.display(round(self.volume))

        else:
            self.volume = volume
            print('Setting volume to ' + str(round(self.volume)))
            if not silent:
                self.screen.display(round(self.volume))
            # todo - actually call call catt here

    def main(self):
        lastVolume = self.volume
        clkLastState = GPIO.input(self.clk)
        newVolume = lastVolume
        try:
            print("Started cattrotar!");
            while True:
                # nukeMike suggests maybe doing debouncing in software by checking
                # the GPIO values a few times before trusting them
                deboucnce_wait = 0.001
                clkState = GPIO.input(self.clk)
                dtState = GPIO.input(self.dt)
                sleep(deboucnce_wait)
                clkState2 = GPIO.input(self.clk)
                dtState2 = GPIO.input(self.dt)
                sleep(deboucnce_wait)
                clkState3 = GPIO.input(self.clk)
                dtState3 = GPIO.input(self.dt)

                # see if we got a valid change
                if clkState != clkLastState and\
                        clkState == clkState2 and\
                        clkState2 == clkState3 and\
                        clkState == clkState3 and\
                        dtState == dtState2 and\
                        dtState2 == dtState3 and\
                        dtState == dtState3:
                    # reset button state to be up
                    self.button = 0
                    print("DEBUG start clkState: " + str(clkState) + " dtState: " + str(dtState) + " self.volume: " + str(self.volume) + " newVolume: " + str(newVolume))
                    if dtState != clkState:
                        newVolume += .5
                    else:
                        newVolume -= .5

                    # only if new volume has changed more than .5 and it's different than prior
                    # volume levels do we actually update volume
                    if newVolume % 1 == 0 and lastVolume != newVolume:
                        lastVolume = newVolume
                        self.setVolume(newVolume)

                clkLastState = clkState
                sleep(0.001)
        except KeyboardInterrupt:
            print("\nkeyboard killed the process")
        finally:
            print('cattrotar exiting')
            GPIO.cleanup()

    def toggleMute(self, channel):
        if self.button == 0:
            print("DEBUG toggleMute MUTE!: " + str(self.button))
            self.button = 1
            self.preMuteVolume = self.volume
            self.setVolume(0, True)
            self.screen.display("MUTE")
        else:
            print("DEBUG toggleMute UNMUTE!: " + str(self.button))
            self.button = 0
            self.setVolume(self.preMuteVolume)


if __name__ == "__main__":
    cr = cattrotar()
    cr.main()