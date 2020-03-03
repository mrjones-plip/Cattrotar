# Cattrotar

Use a Raspbery Pi, a GPIO rotary encoder and optionally a screen to control the volume of your chromecast. 
This a port of [Cattmate](https://github.com/Ths2-9Y-LqJt6/cattmate) to use GPIO devices instead of USB devices.

## Status

All working except mute.  See [#3](https://github.com/Ths2-9Y-LqJt6/Cattrotar/issues/3)

## Hardware

* Raspbery Pi - I used a [Raspberry Pi Model 3B Rev 1.2](https://amzn.to/2REZXwb)
* Rotary Encorder - Either [with jumper cables](https://amzn.to/2VlHF4W) or [without](https://amzn.to/2Ih01fA)!
* 0.96" SSD1336 OLED Screen (_optional_) - I use [these from MakerFocus](https://amzn.to/2PKMQqL)
* [Chromecast](https://en.wikipedia.org/wiki/Chromecast) - any sort will do, original, audio or ultra

## Install

These steps assume you have your Pi set up with Raspbian, that it's booted up, connected
to the same WiFi as your Chromecast. If your Chromecast is on a different network, but 
you can get to it by IP, the
config supports IPs instead of Chromecast names.  It also assumes you're using the `pi`
default user with a home directory of `/home/pi` and that you have both 
[pip3](https://pip.pypa.io/en/stable/installing/) and optionally 
[virtualenv](https://virtualenv.pypa.io/en/stable/) installed:

1. Clone this repo and cd into it:
 `git clone https://github.com/Ths2-9Y-LqJt6/cattrotar.git /home/pi/cattrotar; cd /home/pi/cattmate`
1. Create your own virtualenv and activate it `python3 -m venv venv;. venv/bin/activate` (_optional_)
1. Install all the python prerequisites with `pip3 install -r requirements.txt`
1. Connect your rotary encoder to these GPIO pins. You're welcome to use different ones, but be
sure to update your `config.py` on the next step. See [this diagram](rotary-encoder_bb_1024x1024.png) to help
get you started ([thx Pi Hut](https://thepihut.com/blogs/raspberry-pi-tutorials/how-to-use-a-rotary-encoder-with-the-raspberry-pi)):
    ```python
    clk = 17
    dt = 18
    sw = 23
    + = 3.3
    GND = Ground 
    ```
1. Create your own config file `cp config.dist.py config.dist` and edit `config.dist` if needed:
   1. names or IPs of the chromecasts you want to use (ony first one supported right now ;)
   1. whether you want to use an external I2C screen or not
   1. the pins you'll use for the rotary encoder
1. Copy the systemd file into place, reload systemd, start and enable it:
    ```bash
    sudo cp cattrotar.service /etc/systemd/system/
    sudo systemctl daemon-reload
    sudo systemctl enable cattrotar
    sudo systemctl start cattrotar
    ```

 
You should be good to go!  

# Troubleshooting 

You can debug the system in syslog with `sudo tail -f /var/log/syslog`. I try to do a lot 
of testing and explicit have `except` errors that explicitly tell you what went wrong
and how to fix it.  If all else fails, open an issue and I'l try and help ya!


## Releases

* 3 mar 2020 v0.2 - All working except mute (see [#3](https://github.com/Ths2-9Y-LqJt6/Cattrotar/issues/3)). Fixed 
[#1](https://github.com/Ths2-9Y-LqJt6/Cattrotar/issues/1) 
* 24 Feb 2020 v0.1 - First Post! 
