from machine import Pin, SPI
from st7735 import TFT
from sysfont import sysfont
import time, dht

# настройка дисплея
spi = SPI(2, baudrate=20000000, polarity=0, phase=0, sck=Pin(23), mosi=Pin(18))
display = TFT(spi, aDC=17, aReset=16, aCS=4) 
display.initr()
display.rgb(True)
display.rotation(1)
blk_pin = Pin(14, Pin.OUT)
blk_pin.value(1)

last_state = None

try:
    sensor = dht.DHT11(Pin(5))
    
    while True:
        try:
            sensor.measure()
            current_state = "data"
        except OSError:
            current_state = "os_error"
        except ValueError:
            current_state = "value_error"
            
        if current_state != last_state:
            display.fill(TFT.BLACK)
            last_state = current_state
            
        if current_state == "os_error":
            display.rect((5, 5), (150, 118), TFT.MAROON)
            display.line((5, 22), (154, 22), TFT.MAROON)
            display.text((10, 10), "Error", TFT.RED, sysfont)
            display.text((10, 30), "No connection!", TFT.WHITE, sysfont)
            
            display.text((10, 50), "Check wires and pins.", TFT.WHITE, sysfont)

            display.text((10, 70), "Data pin - 5;", TFT.WHITE, sysfont)
            display.text((10, 80), "Plus pin - 3v3.", TFT.WHITE, sysfont)
        elif current_state == "value_error":
            display.rect((5, 5), (150, 118), TFT.MAROON)
            display.line((5, 22), (154, 22), TFT.MAROON)
            display.text((10, 10), "Error", TFT.RED, sysfont)
            display.text((10, 30), "Bad data!", TFT.WHITE, sysfont)
            
            display.text((10, 50), "Check pullup and DHT", TFT.WHITE, sysfont)
            display.text((10, 60), "types.", TFT.WHITE, sysfont)
        elif current_state == "data":
            display.rect((5, 5), (150, 118), TFT.GRAY)
            display.line((5, 22), (154, 22), TFT.GRAY)
            display.text((10, 10), "Data", TFT.WHITE, sysfont)
            display.text((10, 30), "Temperature:", TFT.WHITE, sysfont)
            display.text((10, 40), "Humidity:", TFT.WHITE, sysfont)
            
            display.fillrect((82, 30), (71, 8), TFT.BLACK)
            display.fillrect((63, 40), (91, 8), TFT.BLACK)
            
            display.text((85, 30), f"{sensor.temperature()}'C", TFT.WHITE, sysfont)
            display.text((66, 40), f"{sensor.humidity()}%", TFT.WHITE, sysfont)
        
        time.sleep_ms(100)
        
# действия при завершении работы программы
finally:
    # отключение подстветки дисплея
    blk_pin.value(0)