from hcsr04sensor import sensor
import time

def main():
    '''Calculate the distance of an object in centimeters using a HCSR04 sensor
       and a Raspberry Pi'''

    # Default values
    # unit = 'metric'
    # temperature = 20
    # round_to = 1

    #  Create a distance reading with the hcsr04 sensor module
    value = sensor.Measurement(trig_pin, echo_pin)
    raw_measurement = value.raw_distance()

    # To overide default values you can pass the following to value
    # value = sensor.Measurement(trig_pin,
    #                            echo_pin,
    #                            temperature=10,
    #                            round_to=2
    #                            )


    # Calculate the distance in centimeters
    metric_distance = value.distance_metric(raw_measurement)
    print("The Distance = {} centimeters".format(metric_distance))

if __name__ == "__main__":
    trig_pin = 17 #pin 11
    echo_pin = 27 #pin 13
    while 1:
        main()
        time.sleep(0.5)