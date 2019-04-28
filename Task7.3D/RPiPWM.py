import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

TRIG = 23
ECHO = 24
LED = 18
Frequency = 200

# initialise pins
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(LED, GPIO.OUT)
pwmLED = GPIO.PWM(LED, Frequency)

# wait for sensor to settle
GPIO.output(TRIG, False)
pwmLED.start(0)
time.sleep(2)


def SenseDistance():

    # send pulse
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while (GPIO.input(ECHO) == 0):
        pulseStart = time.time()

    while (GPIO.input(ECHO) == 1):
        pulseEnd = time.time()

    # calculate pulse duration
    pulseDuration = pulseEnd - pulseStart
    Distance = pulseDuration*17150
    Distance = round(Distance, 2)
    
    return Distance


# sense distance first off to get baseline
InitialDistance = SenseDistance()

if (InitialDistance > 50):
    print "No objects detected within 0.5m."
    
else:
    # duty cycle must be between 0-100%
    pwmLED.ChangeDutyCycle(100 - (InitialDistance*2))
    print "Initial distance:", InitialDistance, "cm"

try:
    while True:
        # send pulse and measure distance
        DistanceNow = SenseDistance()

        # bad data as sensor only works up to 400cm
        if (DistanceNow > 400):
            print " - - - "

        # we're not interested in more than 0.5m
        elif (DistanceNow > 50):
            pwmLED.ChangeDutyCycle(0)
            print "Distance:", DistanceNow, "cm"
        
        # something is within 0.5m
        else:
            # is it approaching?
            if (DistanceNow < (InitialDistance*0.9)):
                print "Object approaching!!!"
            
            # or is it retreating?
            elif (DistanceNow > (InitialDistance*1.1)):
                print "Object retreating ..."

            pwmLED.ChangeDutyCycle(100 - (InitialDistance*2))
            print "Distance:", DistanceNow, "cm"
            InitialDistance = DistanceNow

        time.sleep(1)


except KeyboardInterrupt:
    print "Exiting Distance Sensor Program."

except:
    print "An error has occured."

finally:
    GPIO.cleanup()
