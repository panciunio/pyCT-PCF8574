#!/usr/bin/python
import smbus
import time
import hd44870_lib as lcd

lcd.lcd_init()
lcd.lcd_clean()

while(1):
	lcd.lcd_backlite(True)
	lcd.lcd_write_lines("test1","test2")	
	time.sleep(1)	
	lcd.lcd_write_lines("test2","test1")
	time.sleep(1)
		
	lcd.lcd_backlite(False)
	lcd.lcd_write_lines("test1","test2")	
	time.sleep(1)	
	lcd.lcd_write_lines("test2","test1")
	time.sleep(1)	
