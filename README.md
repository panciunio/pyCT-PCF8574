# pyCT-PCF8574
LCD script using I2C based on PCF8574

           hd44870_lib.py
  LCD script using I2C based on PCF8574.
  Supports 16x2 and 20x4 screens.

 Author : based on Matt's Hawkins work
 Date   : 20/09/2015#
 http://www.raspberrypi-spy.co.uk/

 Cubieboard version : Blazej Biernat
 https://cubietrack.pl

 The wiring for the LCD is as follows:
 1 : GND
 2 : 5V
 3 : Contrast (0-5V)*
 4 : RS (Register Select)
 5 : R/W (Read Write)       - GROUND THIS PIN
 6 : Enable or Strobe
 7 : Data Bit 0             - NOT USED
 8 : Data Bit 1             - NOT USED
 9 : Data Bit 2             - NOT USED
 10: Data Bit 3             - NOT USED
 11: Data Bit 4
 12: Data Bit 5
 13: Data Bit 6
 14: Data Bit 7
 15: LCD Backlight +5V**
 16: LCD Backlight GND
--------------------------------------
