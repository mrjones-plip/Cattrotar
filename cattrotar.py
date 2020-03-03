print("Trying to start cattrotar...")
print("Loading base libraries...")
import socket, time
from RPi import GPIO
from time import sleep
import logging, sys, os
from Oled import Oled
print("Loading catt lib...")
import catt.api as cat_api
logging.basicConfig(filename=os.path.dirname(os.path.abspath(__file__)) + "/error.log")
try:
    import config
except ModuleNotFoundError as e:
    logging.error(logging.exception(e))
    sys.exit("ERROR: Couldn't find file 'config.py'. Did you copy and edit 'config.dist.py' per readme.md?")

# todo: put these in readme.md
# enable i2c with and install
# follow https://learn.adafruit.com/monochrome-oled-breakouts/python-setup
# python3 -m pip install Pillow
# sudo apt-get install libopenjp2-7


class cattrotar:

    def __init__(self):

        self.volume = 1
        self.preMuteVolume = self.volume
        self.button = 0
        self.last_screen_update = time.time()
        self.cast = False

        print('Trying to get handle to Chromecast ' + config.chromecasts[0] + '...')
        try:
            self.get_cast_handle(config.chromecasts[0])
        except cat_api.CastError as error:
            logging.error(logging.exception(error))
            sys.exit("ERROR: Couldn't connect to '" + config.chromecasts[0] + "'. Check config.py and name/IP.")

        if config.use_display:
            print('Trying to initialize screen on default i2c bus...')
            try:
                self.screen = Oled();
                self.show(';)')
                sleep(.5)
            except Exception as error:
                logging.error(logging.exception(error))
                sys.exit('ERROR Could not access screen: ' + str(error))

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(config.clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(config.dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(config.sw, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(config.sw, GPIO.FALLING, callback=self.toggleMute, bouncetime=500)

    def get_cast_handle(self, name_or_ip):
        try:
            socket.inet_pton(socket.AF_INET6, name_or_ip)
            self.cast = cat_api.CattDevice(ip_addr=name_or_ip)
        except socket.error:
            try:
                socket.inet_aton(name_or_ip)
                self.cast = cat_api.CattDevice(ip_addr=name_or_ip)
            except socket.error:
                self.cast = cat_api.CattDevice(name=name_or_ip)

    def setVolume(self, volume, silent=False):
        if volume < 0:
            if not silent:
                self.show("MIN")

            self.cast.volume(int(0) / 100)
            print("Min volume!")
            sleep(0.5)
            self.show(round(self.volume))
            return 0

        elif volume > 100:
            if not silent:
                self.screen.display("MAX")
            print("Max volume!")
            sleep(0.5)
            self.show(round(self.volume))
            return 100

        else:
            print('Setting chromecast ' + config.chromecasts[0] + ' volume to ' + str(round(self.volume)))
            self.cast.volume(int(self.volume) / 100)
            self.volume = volume
            if not silent:
                self.show(round(self.volume))
            return volume

    def show(self, text, size=config.font_size):
        if config.use_display:
            self.screen.display(text, size)
            self.last_screen_update = time.time()

    def main(self):
        lastVolume = self.volume
        clkLastState = GPIO.input(config.clk)
        newVolume = lastVolume
        try:
            print("Started cattrotar!");
            while True:

                clkState = GPIO.input(config.clk)
                dtState = GPIO.input(config.dt)

                # see if we got a change since last iteration of loop
                if clkState != clkLastState:
                    if dtState != clkState:
                        newVolume += .5
                    else:
                        newVolume -= .5

                    # only if new volume has changed more than .5 and it's different than prior
                    # volume levels do we actually update volume
                    if newVolume % 1 == 0 and lastVolume != newVolume:
                        # reset button state to be up
                        self.button = 0

                        # set volume
                        newVolume = self.setVolume(newVolume)
                        lastVolume = newVolume

                # empty screen after 10 seconds
                if (time.time() - self.last_screen_update) > 10:
                    self.show(' ')

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
            self.show("MUTE")
        else:
            print("DEBUG toggleMute UNMUTE!: " + str(self.button))
            self.button = 0
            self.setVolume(self.preMuteVolume)


if __name__ == "__main__":
    cr = cattrotar()
    cr.main()
