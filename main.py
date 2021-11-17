import machine
from machine import Pin, UART, PWM
from machine import I2C
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd
from time import sleep_us 
import utime


I2C_ADDR     = 0x27
I2C_NUM_ROWS = 4
I2C_NUM_COLS = 20

i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

MID = 1500000
MIN = 1000000
MAX = 2000000

BT = UART(1, 9600)
LED_G = Pin(11, Pin.OUT)
LED_R = Pin(10, Pin.OUT)
LED_W = Pin(27, Pin.OUT)
pwm = PWM(Pin(15))
trigger = Pin(18, Pin.OUT)
echo = Pin(19, Pin.IN)

def ultra():
   trigger.low()
   utime.sleep_us(2)
   trigger.high()
   utime.sleep_us(3)
   trigger.low()
   while echo.value() == 0:
       signaloff = utime.ticks_us()
   while echo.value() == 1:
       signalon = utime.ticks_us()
   timepassed = signalon - signaloff
   gap = (timepassed * 0.0343) / 2
   
   if gap < 20:
       print("Item available")
       lcd.clear()
       lcd.move_to(0,0)
       lcd.putstr("Code: 1")
       LED_W.high()
       BT.write('Collect item;')

   elif gap >20:
       print("Box empty")
       lcd.clear()
       lcd.move_to(0,0)
       lcd.putstr("Code: 0")
       LED_W.low()
       BT.write('Box Empty;')
       
   utime.sleep(1)

def key():
    if BT.any() > 0:
        data = BT.read(1)
        
        if "1" in data:
            LED_G.high()
            LED_R.low()
            pwm.duty_ns(MIN)
        
        else:
            LED_G.low()
            LED_R.high()
            pwm.duty_ns(MAX)

pwm.freq(50)

while True:
    ultra()
    key()


