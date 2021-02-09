# LCD 16x2 Display for Pi Pico
# 2021 andy.crook@gmail.com

# Not I2C based, this uses a 4 wire scheme for the data. No library required.



# The wiring for the LCD is as follows:
# 1 : GND
# 2 : 5V from VBUS
# 3 : Contrast (0-5V) via variable resistor
# 4 : RS (Register Select)   - PIN 7
# 5 : R/W (Read Write)       - CONNECT PIN TO GROUND
# 6 : Enable or Strobe       - PIN 8
# 7 : Data Bit 0             - NOT USED
# 8 : Data Bit 1             - NOT USED
# 9 : Data Bit 2             - NOT USED
# 10: Data Bit 3             - NOT USED
# 11: Data Bit 4             - PIN 17
# 12: Data Bit 5             - PIN 16
# 13: Data Bit 6             - PIN 19
# 14: Data Bit 7             - PIN 18
# 15: LCD Backlight +5V
# 16: LCD Backlight GND

from machine import Pin
import time

# Define GPIO to LCD mapping - Pay attention to correct pins on PICO
LCD_RS = 7
LCD_E  = 8
LCD_D4 = 17
LCD_D5 = 16
LCD_D6 = 19
LCD_D7 = 18


# Define LCD Device Width
LCD_WIDTH = 16    # Maximum characters per line


# Define LCD Command or Character send boolean
LCD_CHR = True
LCD_CMD = False


LCD_LINE_1 = int(0x80) # LCD address in RAM for the 1st line
LCD_LINE_2 = int(0xC0) # LCD address in RAM for the 2nd line


# Timing 
E_PULSE = 0.0005
E_DELAY = 0.0005


L_E  = Pin(LCD_E, Pin.OUT)
L_RS = Pin(LCD_RS, Pin.OUT)
L_D4 = Pin(LCD_D4, Pin.OUT)
L_D5 = Pin(LCD_D5, Pin.OUT)
L_D6 = Pin(LCD_D6, Pin.OUT)
L_D7 = Pin(LCD_D7, Pin.OUT)


def main():

  # Initialise display
  lcd_init()
  
  # LOAD SPECIAL CHARACTER EXAMPLE
  lcd_CG()

  while True:

    time.sleep(1) 

    lcd_string("Raspberry PICO",LCD_LINE_1)
    lcd_string("  LCD  TESTING  ",LCD_LINE_2)
    


    time.sleep(3)
    
    # Scroll display to the left, then to the right then back to center
    for x in range(0,16):
        lcd_scrollleft()
        time.sleep(1)
    for x in range(0,32):
        lcd_scrollright()
        time.sleep(1)
    for x in range(0,16):
        lcd_scrollleft()
        time.sleep(1)






def lcd_CG():
    # Loads a special character into the first character address in RAM - 0x40
    time.sleep(0.1)
    lcd_byte(int(0x40),LCD_CMD) # sending cg char
    time.sleep(0.1)
    lcd_byte(int(0x1B),LCD_CHR) # sending data to cg 10101010
    lcd_byte(int(0x1B),LCD_CHR) # sending data to cg 10101010
    lcd_byte(int(0x1B),LCD_CHR) # sending data to cg 10101010
    lcd_byte(int(0x00),LCD_CHR) # sending data to cg 10101010
    lcd_byte(int(0x11),LCD_CHR) # sending data to cg 10101010
    lcd_byte(int(0x0E),LCD_CHR) # sending data to cg 10101010
    lcd_byte(int(0x0E),LCD_CHR) # sending data to cg 10101010
    lcd_byte(int(0x00),LCD_CHR) # sending data to cg 10101010




def lcd_scrollleft():
    
    lcd_byte(int(0x18),LCD_CMD) # CMD to scroll display left


def lcd_scrollright():
    
    lcd_byte(int(0x1C),LCD_CMD) # CMD to scroll display right




def lcd_init():

  lcd_byte(int(0x33),LCD_CMD) # Initialise 1
  lcd_byte(int(0x32),LCD_CMD) # Initialise 2
  lcd_byte(int(0x06),LCD_CMD) # Cursor move direction
  lcd_byte(int(0x0C),LCD_CMD) # Display On,Cursor Off, Blink Off
  lcd_byte(int(0x28),LCD_CMD) # Data length, number of lines, font size
  lcd_byte(int(0x01),LCD_CMD) # Clear display
  time.sleep(E_DELAY)

def lcd_byte(bits, mode):
  # Send byte to data pins
  if (mode == True):    # sending a CHR
    L_RS.high()
  if (mode == False):   # sending a CMD
    L_RS.low()

  L_D4.low()
  L_D5.low()
  L_D6.low()
  L_D7.low()
  
  # Send HIGH bits
  
  if (bits&16):
    L_D4.high()

  if (bits&32):
    L_D5.high()

  if (bits&64):
    L_D6.high()

  if (bits&128):
    L_D7.high()

  # Toggle Enable pin
  lcd_toggle_enable()

  # Send LOW bits

  L_D4.low()
  L_D5.low()
  L_D6.low()
  L_D7.low()
  if (bits&1):
    L_D4.high()

  if (bits&2):
    L_D5.high()

  if (bits&4):
    L_D6.high()

  if (bits&8):
    L_D7.high()

  # Toggle Enable pin
  lcd_toggle_enable()


def lcd_toggle_enable():
  # Toggle enable
  time.sleep(E_DELAY)
  L_E.high()
  time.sleep(E_PULSE)
  L_E.low()
  time.sleep(E_DELAY)


def lcd_string(message,line):
  # Send string to display
  message = message + "                " # Add whitespace to message
  lcd_byte(line, LCD_CMD)
  lcd_byte(0,LCD_CHR) # send a CG CHR (CHR 0) to the display
  
  for i in range(LCD_WIDTH):    
    lcd_byte(ord(message[i]),LCD_CHR) # Send each CHR in the message to the display
    
# Call main loop
main()