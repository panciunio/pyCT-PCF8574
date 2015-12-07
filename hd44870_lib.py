#!/usr/bin/python
#--------------------------------------
#           hd44870_lib.py
#  LCD script using I2C based on PCF8574.
#  Supports 16x2 and 20x4 screens.
#
# Author : based on Matt's Hawkins work
# Date   : 20/09/2015#
# http://www.raspberrypi-spy.co.uk/
#
# Cubieboard version : Blazej Biernat
#
# The wiring for the LCD is as follows:
# 1 : GND
# 2 : 5V
# 3 : Contrast (0-5V)*
# 4 : RS (Register Select)
# 5 : R/W (Read Write)       - GROUND THIS PIN
# 6 : Enable or Strobe
# 7 : Data Bit 0             - NOT USED
# 8 : Data Bit 1             - NOT USED
# 9 : Data Bit 2             - NOT USED
# 10: Data Bit 3             - NOT USED
# 11: Data Bit 4
# 12: Data Bit 5
# 13: Data Bit 6
# 14: Data Bit 7
# 15: LCD Backlight +5V**
# 16: LCD Backlight GND
#--------------------------------------
import smbus
from itertools import cycle
import time

bus = smbus.SMBus(1)
I2C_ADDR	=	0x27

#LCD_SIG = PORT(BIT)
LCD_RS	=	0
LCD_RW	=	1
LCD_E	=	2
LCD_BL	=	3
LCD_D4	=	4
LCD_D5	=	5
LCD_D6	=	6
LCD_D7	=	7

# Define some device constants
LCD_WIDTH = 20		# Maximum characters per line
LCD_CHR = True
LCD_CMD = False

# Some commands
LCD_CLRSCR = 0x01
 
LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xc0 # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94 # LCD RAM address for the 1st line
LCD_LINE_4 = 0xd4 # LCD RAM address for the 2nd line
 
# Timing constants
INIT_DELAY = 0.00100
E_PULSE = 0.00005
E_DELAY = 0.00005

def lcd_init():
	#read actual PCF8574 variable
	i2c_value = bus.read_byte(I2C_ADDR)
	
	i2c_value = clearBit(i2c_value,LCD_RW)
	bus.write_byte(I2C_ADDR,i2c_value)
	
	# Initialise display sequense
	lcd_byte(0x03,LCD_CMD)
	time.sleep(INIT_DELAY)		
	lcd_byte(0x03,LCD_CMD)
	time.sleep(INIT_DELAY)	
	lcd_byte(0x03,LCD_CMD)
	time.sleep(INIT_DELAY)	
	lcd_byte(0x02,LCD_CMD)
	time.sleep(INIT_DELAY)	
	lcd_byte(0x02,LCD_CMD)
	time.sleep(E_DELAY)	
	lcd_byte(0x08,LCD_CMD)
	time.sleep(E_DELAY)	
	lcd_byte(0x01,LCD_CMD)
	time.sleep(E_DELAY/2)	
	lcd_byte(0x06,LCD_CMD)	
	time.sleep(E_DELAY)
	
	lcd_byte(0x0c,LCD_CMD)	

def lcd_clean():
	lcd_byte(LCD_CLRSCR, LCD_CMD)
	
def lcd_backlite(mode):
	i2c_value = bus.read_byte(I2C_ADDR)
	
	if (mode):
		i2c_value = setBit(i2c_value,LCD_BL)
	else:
		i2c_value = clearBit(i2c_value,LCD_BL)
	bus.write_byte(I2C_ADDR,i2c_value)

def lcd_write_lines(msg1, msg2):
	if(msg1)<>"":
		lcd_byte(LCD_LINE_1, LCD_CMD)
		lcd_string(msg1)

	if(msg2)<>"":
		lcd_byte(LCD_LINE_2, LCD_CMD)
		lcd_string(msg2)

def lcd_write_4lines(msg1, msg2, msg3, msg4):
	if(msg1)<>"":
		lcd_byte(LCD_LINE_1, LCD_CMD)
		lcd_string(msg1)

	if(msg2)<>"":
		lcd_byte(LCD_LINE_2, LCD_CMD)
		lcd_string(msg2)

	if(msg3)<>"":
		lcd_byte(LCD_LINE_3, LCD_CMD)
		lcd_string(msg3)

	if(msg4)<>"":
		lcd_byte(LCD_LINE_4, LCD_CMD)
		lcd_string(msg4)

			
def lcd_string(message):
	# Send string to display 
	message = message.ljust(LCD_WIDTH," ") 
 
	for i in range(LCD_WIDTH):
		lcd_byte(ord(message[i]),LCD_CHR)
 
def lcd_byte(bits, mode):
	# Send byte to PCF8574 data register 
	# bits = data
	# mode = True for character
	# mode = False for command
	# i2c_value = actually  data from PCF8574
	
	i2c_value=bus.read_byte(I2C_ADDR)	
	
	if (mode):
		i2c_value = setBit(i2c_value,LCD_RS)
	else:
		i2c_value = clearBit(i2c_value,LCD_RS)
	
	bus.write_byte(I2C_ADDR,i2c_value)	

	# High bits
	i2c_value = clearBit(i2c_value,LCD_D4)
	i2c_value = clearBit(i2c_value,LCD_D5)
	i2c_value = clearBit(i2c_value,LCD_D6)
	i2c_value = clearBit(i2c_value,LCD_D7)

	if bits&0x10==0x10:
		i2c_value = setBit(i2c_value,LCD_D4)
	if bits&0x20==0x20:
		i2c_value = setBit(i2c_value,LCD_D5)
	if bits&0x40==0x40:
		i2c_value = setBit(i2c_value,LCD_D6)
	if bits&0x80==0x80:
		i2c_value = setBit(i2c_value,LCD_D7)

	bus.write_byte(I2C_ADDR,i2c_value)
	
	# Toggle 'Enable' pin
	time.sleep(E_DELAY)
	
	i2c_value = setBit(i2c_value,LCD_E)
	bus.write_byte(I2C_ADDR,i2c_value)
	time.sleep(E_PULSE)
	
	i2c_value = clearBit(i2c_value,LCD_E)
	bus.write_byte(I2C_ADDR,i2c_value)
	time.sleep(E_DELAY)		
	
	# Low bits
 	i2c_value = clearBit(i2c_value,LCD_D4)
	i2c_value = clearBit(i2c_value,LCD_D5)
	i2c_value = clearBit(i2c_value,LCD_D6)
	i2c_value = clearBit(i2c_value,LCD_D7)

	if bits&0x01==0x01:
		i2c_value = setBit(i2c_value,LCD_D4)
	if bits&0x02==0x02:
		i2c_value = setBit(i2c_value,LCD_D5)
	if bits&0x04==0x04:
		i2c_value = setBit(i2c_value,LCD_D6)
	if bits&0x08==0x08:
		i2c_value = setBit(i2c_value,LCD_D7)

	bus.write_byte(I2C_ADDR,i2c_value)
	
	# Toggle 'Enable' pin
	time.sleep(E_DELAY)
	
	i2c_value = setBit(i2c_value,LCD_E)
	bus.write_byte(I2C_ADDR,i2c_value)
	time.sleep(E_PULSE)
	
	i2c_value = clearBit(i2c_value,LCD_E)
	bus.write_byte(I2C_ADDR,i2c_value)
	time.sleep(E_DELAY)	
		
# testBit() returns a nonzero result, 2**offset, if the bit at 'offset' is one.
def testBit(int_type, offset):
	mask = 1 << offset
	return(int_type & mask)

# setBit() returns an integer with the bit at 'offset' set to 1.
def setBit(int_type, offset):
	mask = 1 << offset
	return(int_type | mask)

# clearBit() returns an integer with the bit at 'offset' cleared.
def clearBit(int_type, offset):
	mask = ~(1 << offset)
	return(int_type & mask)

# toggleBit() returns an integer with the bit at 'offset' inverted, 0 -> 1 and 1 -> 0.
def toggleBit(int_type, offset):
	mask = 1 << offset
	return(int_type ^ mask)

def lcd_log2file(fp,line):
	pattern = "[LCD]: "
	logfile = open(fp, "a+")
	line = str(ticks) + '|' + pattern + line +'\n'
	logfile.write(line)
	logfile.close()	
