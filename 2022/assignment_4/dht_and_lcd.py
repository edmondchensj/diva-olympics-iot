import grovepi
import grove_rgb_lcd
import time
import math

dht_sensor_port = 7 # connect the DHt sensor to port 7
dht_sensor_type = 0 # use 0 for the blue-colored sensor and 1 for the white-colored sensor

# set green as backlight color
# we need to do it just once
# setting the backlight color once reduces the amount of data transfer over the I2C line
grove_rgb_lcd.setRGB(0,255,0)

while True:
    try:
        # get the temperature and Humidity from the DHT sensor
        [ temp,hum ] = grovepi.dht(dht_sensor_port,dht_sensor_type)
        print("temp =", temp, "C\thumidity =", hum,"%")

        # check if we have nans
        # if so, then raise a type error exception
        if math.isnan(temp) is True or math.isnan(hum) is True:
            print('Cannot get valid reading from sensor')
            continue

        t = str(temp)
        h = str(hum)

        # instead of inserting a bunch of whitespace, we can just insert a \n
        # we're ensuring that if we get some strange strings on one line, the 2nd one won't be affected
        grove_rgb_lcd.setText_norefresh("Temp:" + t + "C\n" + "Humidity :" + h + "%")

    except (IOError, TypeError) as e:
        print(str(e))
        # and since we got a type error
        # then reset the LCD's text
        grove_rgb_lcd.setText('OS Error')

    except KeyboardInterrupt as e:
        print(str(e))
        # since we're exiting the program
        # it's better to leave the LCD with a blank text
        grove_rgb_lcd.setText("")
        break

    # wait some time before re-updating the LCD
    time.sleep(0.2)