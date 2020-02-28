print("Trying to start cattrotar...")
print("Loading base libraries...")
from RPi import GPIO
from time import sleep
import logging, sys, os
from Oled import Oled
print("Loading catt lib...")
import catt.api as cat_api
logging.basicConfig(filename=os.path.dirname(os.path.abspath(__file__)) + "/error.log")

# todo: put these in readme.md
# enable i2c with and install
# follow https://learn.adafruit.com/monochrome-oled-breakouts/python-setup
# python3 -m pip install Pillow
# sudo apt-get install libopenjp2-7


class cattrotar:

    def __init__(self):

        self.clk = 17
        self.dt = 18
        self.sw = 23
        self.volume = 20
        self.preMuteVolume = self.volume
        self.button = 0
        print('Trying to initialize screen on default i2c bus...')
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
                print("Min volume!")
                sleep(0.5)
                self.screen.display(round(self.volume))
                return 0

        elif volume > 100:
            if not silent:
                print("Max volume!")
                self.screen.display("MAX")
                sleep(0.5)
                self.screen.display(round(self.volume))
                return 100

        else:
            self.volume = volume
            print('Setting volume to ' + str(round(self.volume)))
            if not silent:
                self.screen.display(round(self.volume))
            # todo - actually call call catt here
            return volume

    def main(self):
        lastVolume = self.volume
        clkLastState = GPIO.input(self.clk)
        newVolume = lastVolume
        try:
            print("Started cattrotar!");
            while True:

                clkState = GPIO.input(self.clk)
                dtState = GPIO.input(self.dt)

                # see if we got a valid change
                if clkState != clkLastState:
                    # reset button state to be up
                    self.button = 0
                    if dtState != clkState:
                        newVolume += .5
                    else:
                        newVolume -= .5

                    # only if new volume has changed more than .5 and it's different than prior
                    # volume levels do we actually update volume
                    if newVolume % 1 == 0 and lastVolume != newVolume:
                        newVolume = self.setVolume(newVolume)
                        lastVolume = newVolume

                clkLastState = clkState
                sleep(0.001)

        except KeyboardInterrupt:
            print("\nkeyboard killed the process")

        finally:
            self.screen.display('Bye!')
            sleep(0.5)
            self.screen.display(' ')
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
