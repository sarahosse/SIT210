#!/usr/bin/env python

import RPi.GPIO as GPIO, sys, urllib2, json, pygame, time, pyaudio, wave, os, random

# APIs -----------------------------------------------------------------------------------

nightAPI = 'BW2W6IWUHOKX5EKC'
nightURL = 'https://api.thingspeak.com/update?api_key=%s' % nightAPI

dayAPI = 'DKTBQM0C1I7F8P14'
dayURL = 'https://api.thingspeak.com/update?api_key=%s' % dayAPI

movementAPI = '7XTWTUPRR1X6LVDW'
movementChannel = 783575

ledAPI = '9SR7KSRO33AQP380'
ledURL = 'https://api.thingspeak.com/update?api_key=%s' % ledAPI

# Variables ------------------------------------------------------------------------------

RED = 23     # stop recording
GREEN = 24   # start recording
BLUE = 18    # blue = nighttime
YELLOW = 12  # yellow = daytime

YellowButtonNotPressed = 1
dreamNumber = 1
stopRecording = False
stopAlarm = False
REM = False

nightTime = 0
successfulNight = False

dayTime = 0
successfulDay = False

form_1 = pyaudio.paInt16 # 16-bit resolution
chans = 2 # 1 channel
samp_rate = 44100 # 44.1kHz sampling rate
chunk = 1024 # samples for buffer
dev_index = 2 # device index found by p.get_device_info_by_index(ii)
filename = 'Dream_'           # start of name of .wav file

Music = ["Bach_Full.wav", "Bach_Prelude.wav", "Experience.wav", "NoRegret.wav", "Winter.wav"]

# Initiations ----------------------------------------------------------------------------

GPIO.setmode(GPIO.BCM)

GPIO.setup(RED, GPIO.IN)
GPIO.setup(GREEN, GPIO.IN)
GPIO.setup(BLUE, GPIO.IN)
GPIO.setup(YELLOW, GPIO.IN)

# ----------------------------------------------------------------------------------------

time.sleep(2)

# keep trying this for as long as the connection is running
try:
    while True:
        
        # NIGHTTIME ----------------------------------------------------------------------

        # when the blue button is pressed (to signal NIGHT)
        if (GPIO.input(BLUE) == 0):
            print "Sweet dreams ..."
            nightTime = 1    # data to be sent to ThingSpeak
            time.sleep(1)
            
            # keep trying this for as long as the data hasn't been sent
            while (successfulNight == False):
            
                # send data to thingSpeak to initiate REM detection
                BLUEconnection = urllib2.urlopen(nightURL + '&field1=%s' % (nightTime))
                print BLUEconnection.read()
                
                # if data sent successfully
                if (BLUEconnection.read() > 0):
                    BLUEconnection.close()    # close connection
                    successfulNight = True    # stop the while loop
                    
                time.sleep(1)
            
            
            # loop until morning
            while (YellowButtonNotPressed == 1):
            
                # watches ThingSpeak for notification of REM sleep -----------------------
            
                MOVEconnection = urllib2.urlopen("http://api.thingspeak.com/channels/%s/feeds/last.json?api_key=%s" % (movementChannel, movementAPI))
    
                response = MOVEconnection.read()
                print "http status code=%s" % (MOVEconnection.getcode())
                data = json.loads(response)
                print data['field1'], data['created_at']
                movement = int(data['field1'])
                
                MOVEconnection.close()
                
                # REM has been detected (movement > 20%), now play music!
                if (movement > 20):
                    REM = True
                    
                    # music will play while in REM ---------------------------------------
                    pygame.mixer.init()
                    pygame.mixer.music.load(random.choice(Music))
                    
                    pygame.mixer.music.play()
                    print "Music playing"
        
                    # let music play in it's entirety
                    while pygame.mixer.music.get_busy() == True:
                        continue
        
                    print "Music finished"
                    
                    # Pi --> ThingSpeak --> Photon ---------------------------------------
        
                    # notify thingSpeak it's time for alarm + LEDs
                    LEDconnection = urllib2.urlopen(ledURL + '&field1=%s' % (1))
                    print LEDconnection.read()
        
                    # if data sent successfully
                    #if (LEDconnection.read() > 0):
                    LEDconnection.close()    # close connection
                    
                    # allow time for photon to receive message
                    time.sleep(5)
                    
                    # Alarm sounds while photon LEDs light up ----------------------------
        
                    # start alarm sound
                    pygame.mixer.init()
                    pygame.mixer.music.load("ALARM.wav")
                    
                    pygame.mixer.music.play()
                    print "Alarm Sounding"
                    
                    # Alarm stops and dream recount begins -------------------------------
                    
                    # loop until alarm stops
                    while (pygame.mixer.music.get_busy() == True):
                        
                        # Alarm stops and recording begins -------------------------------

                        # when the green button is pressed
                        if (GPIO.input(GREEN) == 0):
                    
                            # stop the alarm
                            pygame.mixer.music.stop()
                            print "Alarm Stopped"
                            
                            # notify thingSpeak it's time for flashing LEDs
                            LEDconnection = urllib2.urlopen(ledURL + '&field1=%s' % (2))
                            print LEDconnection.read()
                            LEDconnection.close()    # close connection
                            
                            time.sleep(5)
                            
                            print "Initiating recording ..."
                            
                            # each new dream will be saved to a new file
                            filename += str(dreamNumber) + '.wav'
                    
                            # create pyaudio instantiation
                            audio = pyaudio.PyAudio()
        
                            # create pyaudio stream
                            stream = audio.open(format = form_1, rate = samp_rate, channels = chans, \
                                    input_device_index = dev_index, input = True, \
                                    frames_per_buffer = chunk)
                    
                            frames = []
                    
                            # until the red button is pressed, keep recording
                            while (stopRecording == False):
                        
                                # append audio chunks to frame array
                                data = stream.read(chunk, exception_on_overflow = False)
                                frames.append(data)
                    
                                # if the red button is pressed, stop the recording loop
                                if (GPIO.input(RED) == 0):
                                    stopRecording = True
                                    print "Cease recording " + filename
                            
                            time.sleep(1)
                            
                            # stop the stream, close it, and terminate the pyaudio instantiation
                            print "Closing stream"
                            stream.stop_stream()
                            stream.close()
                            audio.terminate()
        
                            # save the audio frames as .wav file
                            print "Saving audio as " + filename
                            wavefile = wave.open(filename, 'wb')
                            wavefile.setnchannels(chans)
                            wavefile.setsampwidth(audio.get_sample_size(form_1))
                            wavefile.setframerate(samp_rate)
                            wavefile.writeframes(b''.join(frames))
                            wavefile.close()
                            print filename + " saved"
                    
                            # notify thingSpeak it's time to turn LEDs off again
                            LEDconnection = urllib2.urlopen(ledURL + '&field1=%s' % (0))
                            print LEDconnection.read()
                            LEDconnection.close()    # close connection
                            
                            stopRecording = False
                            dreamNumber += 1
                        
                # Recording stops and program returns to listening for next REM ----------
                YellowButtonNotPressed = GPIO.input(YELLOW)
            
        # DAYTIME ------------------------------------------------------------------------
        
        # when the yellow button is pressed (to signal DAY)
        elif (GPIO.input(YELLOW) == 0):
            print "Good moring!"
            dayTime = 1    # data to be sent to ThingSpeak
            time.sleep(1)
            
            # keep trying this for as long as the data hasn't been sent
            while (successfulDay == False):
                    
                # send data to thingSpeak to cease REM detection
                YELconnection = urllib2.urlopen(dayURL + '&field1=%s' % (dayTime))
                print YELconnection.read()
                
                # if data sent successfully
                if (YELconnection.read() > 0):
                    YELconnection.close()    # close connection
                    successfulDay = True    # stop the while loop
                
                time.sleep(1)
        
        # --------------------------------------------------------------------------------

        # set variables back to false/0
        successfulDay = 0
        successfulNight = 0

# cleanup
except KeyboardInterrupt:
    GPIO.cleanup()

GPIO.cleanup()
