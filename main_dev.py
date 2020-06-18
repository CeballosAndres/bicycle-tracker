from ublox_gps import MicropyGPS
import time
import utime
from machine import UART, Pin, I2C
import sh1106

# GPS
UPDATE_GPS = const(10000)
uart = UART(2, 9600)
uart.init(9600, bits=8, parity=None, stop=1, timeout_char=300)
my_gps = MicropyGPS()
stat = None
updateGPS = utime.ticks_ms()

# Oled
i2c = I2C(-1, scl=Pin(22), sda=Pin(21))
oled = sh1106.SH1106_I2C(128, 64, i2c)
oled.rotate(True)

while True:
    try:
        # Updating GPS position
        if(utime.ticks_ms() - updateGPS >= UPDATE_GPS):
            updateGPS = utime.ticks_ms()
            stat = my_gps.updateall(uart.read())
        if(stat != None):
            oled.fill(0)
            oled.text(my_gps.speed_string(), 5, 10, 1)
            oled.text(str(my_gps.altitude), 5, 20, 1)
            oled.text(my_gps.date_string(), 5, 40, 1)
            oled.text(str(my_gps.satellites_in_view), 120, 50, 1)
            oled.text(my_gps.compass_direction(), 120, 60, 1)
            oled.show()
            print(my_gps.compass_direction())
            print(my_gps.date_string())
            print(my_gps.latitude_string())
            print(my_gps.longitude_string())
            print(my_gps.satellites_visible())
            print(my_gps.satellites_in_view)
            print(my_gps.speed_string())
            print(str(my_gps.altitude))
        else:
            oled.fill(0)
            oled.text('X', 120, 55, 1)
            oled.show()
    except:
        my_gps.stringclean()  # cleaning string and starting again

    time.sleep_ms(1000)   # sleeping 1 second
