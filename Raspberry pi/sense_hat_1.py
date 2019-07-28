from sense_emu import SenseHat
sense = SenseHat()
#sense.scroll_speed(0.5)
#sense.show_message("Hello Raspberry Pi")
while 1:
    t = sense.get_temperature()
    p = sense.get_pressure()
    h = sense.get_humidity()

    t = round(t, 1)
    p = round(p, 1)
    h = round(h, 1)
    #sense.show_message("Hello World")
    msg = "Tempeature = %s, Pressure = %s, Humidity = %s"%(t,p,h)
    sense.show_message(msg, scroll_speed=0.05)
